#!/usr/bin/env python3
"""Audit a OneTap client website against the agency's 100-point SEO launch gate."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from xml.etree import ElementTree


@dataclass
class Finding:
    severity: str
    category: str
    message: str
    points: int = 0


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.in_title = False
        self.h1 = 0
        self.headings: list[tuple[str, str]] = []
        self.current_heading: str | None = None
        self.heading_text: list[str] = []
        self.meta: dict[str, str] = {}
        self.links: list[dict[str, str]] = []
        self.images: list[dict[str, str]] = []
        self.scripts: list[dict[str, str]] = []
        self.jsonld_text: list[str] = []
        self.in_jsonld = False
        self.visible_text: list[str] = []
        self.skip_text = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key.lower(): value or "" for key, value in attrs}
        tag = tag.lower()
        if tag == "title":
            self.in_title = True
        if tag in {"script", "style", "noscript"}:
            self.skip_text += 1
        if tag == "script":
            self.scripts.append(data)
            if data.get("type", "").lower() == "application/ld+json":
                self.in_jsonld = True
        if tag == "meta":
            key = (data.get("name") or data.get("property") or "").lower()
            if key:
                self.meta[key] = data.get("content", "")
        if tag == "link":
            self.links.append(data)
        if tag == "img":
            self.images.append(data)
        if re.fullmatch(r"h[1-6]", tag):
            if tag == "h1":
                self.h1 += 1
            self.current_heading = tag
            self.heading_text = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self.in_title = False
        if tag == "script":
            if self.in_jsonld:
                self.in_jsonld = False
            self.skip_text = max(0, self.skip_text - 1)
        elif tag in {"style", "noscript"}:
            self.skip_text = max(0, self.skip_text - 1)
        if self.current_heading == tag:
            self.headings.append((tag, " ".join(self.heading_text).strip()))
            self.current_heading = None
            self.heading_text = []

    def handle_data(self, data: str) -> None:
        clean = " ".join(data.split())
        if not clean:
            return
        if self.in_title:
            self.title += clean
        if self.in_jsonld:
            self.jsonld_text.append(data)
        elif self.skip_text == 0:
            self.visible_text.append(clean)
        if self.current_heading:
            self.heading_text.append(clean)


def load(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Unable to load {path}: {exc}") from exc


def find_home(site_dir: Path) -> Path:
    for candidate in (site_dir / "index.html", site_dir / "site" / "index.html", site_dir / "out" / "index.html"):
        if candidate.exists():
            return candidate
    raise SystemExit(f"Homepage not found below {site_dir}")


def canonical(parser: PageParser) -> str:
    return next((item.get("href", "") for item in parser.links if "canonical" in item.get("rel", "").lower().split()), "")


def graph_nodes(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, dict):
        if isinstance(value.get("@graph"), list):
            return [item for item in value["@graph"] if isinstance(item, dict)]
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    return []


def schema_types(nodes: list[dict[str, Any]]) -> set[str]:
    output: set[str] = set()
    for node in nodes:
        value = node.get("@type")
        if isinstance(value, str):
            output.add(value)
        elif isinstance(value, list):
            output.update(str(item) for item in value)
    return output


def add(findings: list[Finding], severity: str, category: str, message: str, points: int = 0) -> None:
    findings.append(Finding(severity, category, message, points))


def exists_asset(site_dir: Path, value: str) -> bool:
    if not value or value.startswith(("http://", "https://", "data:", "mailto:", "tel:", "sms:", "#")):
        return True
    clean = value.split("?", 1)[0].split("#", 1)[0].lstrip("/")
    return (site_dir / clean).exists()


def audit(config: dict[str, Any], site_dir: Path, production: bool) -> tuple[int, list[Finding], dict[str, Any]]:
    findings: list[Finding] = []
    homepage = find_home(site_dir)
    source = homepage.read_text(encoding="utf-8", errors="replace")
    parser = PageParser()
    parser.feed(source)
    visible = " ".join(parser.visible_text)
    lower_source, lower_visible = source.lower(), visible.lower()
    business, seo, quality = config["business"], config["seo"], config.get("quality", {})
    base = business["website"].rstrip("/")
    expected_home = base + "/"

    # Approved truth: 15 points.
    approvals = config.get("approvals", {})
    required_approvals = [
        "businessFactsApproved", "serviceClaimsApproved", "pricesApproved", "hoursApproved",
        "serviceAreaApproved", "imageRightsConfirmed", "googleBusinessProfileClientOwned",
        "noInventedReviewsOrRatings",
    ]
    incomplete = [key for key in required_approvals if not approvals.get(key)]
    if production and incomplete:
        add(findings, "critical", "Approved business truth", "Incomplete approvals: " + ", ".join(incomplete), 15)
    if business["name"].lower() not in lower_visible:
        add(findings, "critical", "Approved business truth", "Approved business name is not visible on the homepage", 7)
    if business["displayPhone"].lower() not in lower_visible and business["phone"].lower() not in lower_source:
        add(findings, "critical", "Approved business truth", "Approved phone number is missing", 4)
    city = config["location"].get("address", {}).get("addressLocality", "")
    if city and city.lower() not in lower_visible:
        add(findings, "warning", "Approved business truth", f"Primary city {city!r} is not visible", 2)
    for term in quality.get("forbiddenLegacyTerms", []):
        if term and term.lower() in lower_source and term.lower() != business["name"].lower():
            add(findings, "critical", "Approved business truth", f"Previous-client or forbidden term found: {term}", 15)
    placeholders = re.findall(r"\[(?:BUSINESS|CITY|SERVICE|DOMAIN|PHONE|EMAIL)[^\]]*\]|\b(?:lorem ipsum|your business|example\.com|replace me|todo)\b", source, flags=re.I)
    if placeholders:
        add(findings, "critical", "Approved business truth", "Unfinished placeholders remain: " + ", ".join(sorted(set(placeholders))[:8]), 15)

    # Search intent and content: 20 points.
    if parser.h1 != 1:
        add(findings, "critical", "Search intent and content", f"Homepage must have exactly one H1; found {parser.h1}", 7)
    primary = config.get("content", {}).get("primaryKeyword", "")
    if primary and primary.lower() not in lower_source:
        words = [word for word in re.findall(r"[a-z0-9]+", primary.lower()) if len(word) > 2]
        if words and sum(word in lower_visible for word in words) < max(2, len(words) // 2):
            add(findings, "warning", "Search intent and content", "Primary search intent is weakly represented in visible content", 5)
    if not any(tag == "h2" for tag, _ in parser.headings):
        add(findings, "warning", "Search intent and content", "No H2 headings were found", 3)
    for service in config.get("services", []):
        if service.get("name") and service["name"].lower() not in lower_visible:
            add(findings, "warning", "Search intent and content", f"Approved service is not visible: {service['name']}", 2)

    # Metadata and indexability: 15 points.
    if not parser.title or len(parser.title.strip()) < 15:
        add(findings, "critical", "Metadata and indexability", "Missing or unhelpful title", 3)
    description = parser.meta.get("description", "")
    if len(description.strip()) < 70:
        add(findings, "critical", "Metadata and indexability", "Missing or short meta description", 3)
    found_canonical = canonical(parser)
    if found_canonical != expected_home:
        add(findings, "critical", "Metadata and indexability", f"Canonical must be {expected_home}; found {found_canonical or 'missing'}", 4)
    robots_meta = parser.meta.get("robots", "").lower()
    if production and "noindex" in robots_meta:
        add(findings, "critical", "Metadata and indexability", "Production homepage contains noindex", 5)
    for key in ("og:title", "og:description", "og:url", "og:image", "og:image:alt", "twitter:card"):
        if not parser.meta.get(key):
            add(findings, "warning", "Metadata and indexability", f"Missing social metadata: {key}", 1)
    if parser.meta.get("og:url") and parser.meta["og:url"] != expected_home:
        add(findings, "critical", "Metadata and indexability", "Open Graph URL does not match the canonical", 2)

    # Structured data: 10 points.
    nodes: list[dict[str, Any]] = []
    json_errors = 0
    for raw in parser.jsonld_text:
        try:
            nodes.extend(graph_nodes(json.loads(raw)))
        except json.JSONDecodeError:
            json_errors += 1
    if json_errors:
        add(findings, "critical", "Structured data", "Invalid JSON-LD was found", 5)
    types = schema_types(nodes)
    for needed in (business["schemaType"], "WebSite", "Service"):
        if needed not in types:
            add(findings, "critical", "Structured data", f"Required schema type is missing: {needed}", 3)
    has_rating = any("aggregateRating" in json.dumps(node) or node.get("@type") == "AggregateRating" for node in nodes)
    verified = config.get("content", {}).get("verifiedReviews", {})
    if has_rating and not verified.get("enabled"):
        add(findings, "critical", "Structured data", "AggregateRating is present without approved verified-review data", 10)
    if "FAQPage" in types:
        for item in config.get("content", {}).get("faq", []):
            if item.get("question", "").lower() not in lower_visible or item.get("answer", "").lower() not in lower_visible:
                add(findings, "critical", "Structured data", "FAQ schema does not match visible FAQ content", 5)
                break

    # Crawl and discovery: 10 points.
    robots_path, sitemap_path = site_dir / "robots.txt", site_dir / "sitemap.xml"
    if not robots_path.exists():
        add(findings, "critical", "Crawl and discovery", "robots.txt is missing", 4)
    else:
        robots_text = robots_path.read_text(encoding="utf-8", errors="replace")
        if production and re.search(r"(?im)^\s*disallow:\s*/\s*$", robots_text):
            add(findings, "critical", "Crawl and discovery", "robots.txt blocks the entire production site", 5)
        if f"{base}/sitemap.xml" not in robots_text:
            add(findings, "warning", "Crawl and discovery", "robots.txt does not reference the canonical sitemap", 2)
    if not sitemap_path.exists():
        add(findings, "critical", "Crawl and discovery", "sitemap.xml is missing", 4)
    else:
        try:
            sitemap_text = sitemap_path.read_text(encoding="utf-8", errors="replace")
            sitemap_root = ElementTree.fromstring(sitemap_text)
            sitemap_locations = [
                (element.text or "").strip()
                for element in sitemap_root.iter()
                if element.tag.rsplit("}", 1)[-1] == "loc" and (element.text or "").strip()
            ]
            if expected_home not in sitemap_locations:
                add(findings, "critical", "Crawl and discovery", "Canonical homepage is missing from the sitemap", 4)
            wrong_hosts = {
                urlparse(location).netloc
                for location in sitemap_locations
                if urlparse(location).netloc != urlparse(base).netloc
            }
            if wrong_hosts:
                add(findings, "critical", "Crawl and discovery", "Sitemap contains another host: " + ", ".join(sorted(wrong_hosts)), 5)
        except ElementTree.ParseError:
            add(findings, "critical", "Crawl and discovery", "sitemap.xml is invalid XML", 4)

    # Mobile, performance, accessibility: 15 points.
    if "name=\"viewport\"" not in lower_source and "name='viewport'" not in lower_source:
        add(findings, "critical", "Mobile, performance, and accessibility", "Viewport metadata is missing", 4)
    for image in parser.images:
        src = image.get("src", "")
        if "alt" not in image:
            add(findings, "warning", "Mobile, performance, and accessibility", f"Image is missing alt text: {src or 'unknown'}", 2)
        if src and not exists_asset(site_dir, src):
            add(findings, "critical", "Mobile, performance, and accessibility", f"Image asset is missing: {src}", 3)
        if src and not src.startswith(("http://", "https://", "data:")):
            path = site_dir / src.split("?", 1)[0].lstrip("/")
            if path.exists() and path.stat().st_size > int(quality.get("maximumImageBytes", 1572864)):
                add(findings, "warning", "Mobile, performance, and accessibility", f"Large image exceeds limit: {src}", 2)
        if src and not image.get("width") and not image.get("height"):
            add(findings, "warning", "Mobile, performance, and accessibility", f"Image dimensions are not declared: {src}", 1)
    if "<form" in lower_source and "<label" not in lower_source:
        add(findings, "critical", "Mobile, performance, and accessibility", "Form fields do not have visible labels", 4)

    # Conversion and trust: 5 points.
    conversion_tokens = ("<form", "tel:", "sms:", "book", "quote", "contact")
    if not any(token in lower_source for token in conversion_tokens):
        add(findings, "critical", "Conversion and trust", "No clear primary conversion path was detected", 5)
    for item in parser.links:
        href = item.get("href", "")
        if href and not exists_asset(site_dir, href):
            add(findings, "warning", "Conversion and trust", f"Local link target may be missing: {href}", 1)

    # Search Console / GBP and monitoring are evidence-based categories.
    if production and not approvals.get("googleBusinessProfileClientOwned"):
        add(findings, "critical", "Search Console and Business Profile", "Client-owned Google Business Profile approval is incomplete", 5)
    if not (site_dir / "manifest.webmanifest").exists():
        add(findings, "warning", "Monitoring and records", "Web manifest is missing", 1)

    deductions = sum(item.points for item in findings)
    score = max(0, 100 - deductions)
    critical = [item for item in findings if item.severity == "critical"]
    warning = [item for item in findings if item.severity == "warning"]
    details = {
        "score": score,
        "minimumScore": int(quality.get("minimumLaunchScore", 90)),
        "criticalCount": len(critical),
        "warningCount": len(warning),
        "homepage": str(homepage),
        "canonical": found_canonical,
        "schemaTypes": sorted(types),
        "findings": [item.__dict__ for item in findings],
    }
    return score, findings, details


def write_report(path: Path, config: dict[str, Any], details: dict[str, Any]) -> None:
    status = "PASS" if details["score"] >= details["minimumScore"] and details["criticalCount"] == 0 else "BLOCKED"
    lines = [
        "# OneTap Prelaunch SEO Audit",
        "",
        f"Client: **{config['business']['name']}**",
        f"Score: **{details['score']}/100**",
        f"Launch status: **{status}**",
        f"Critical findings: **{details['criticalCount']}**",
        f"Warnings: **{details['warningCount']}**",
        "",
        "## Findings",
        "",
    ]
    if not details["findings"]:
        lines.append("- No findings. The automated gate passed.")
    else:
        for item in details["findings"]:
            lines.append(f"- **{item['severity'].upper()} — {item['category']}**: {item['message']} (-{item['points']})")
    lines.extend(["", "Automated checks do not replace mobile, Rich Results, PageSpeed, form-delivery, and client-approval reviews.", ""])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    path.with_suffix(".json").write_text(json.dumps(details, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--site-dir", type=Path, required=True)
    parser.add_argument("--production", action="store_true")
    parser.add_argument("--report", type=Path, default=Path("seo-output/prelaunch-audit.md"))
    args = parser.parse_args()
    config = load(args.config)
    score, findings, details = audit(config, args.site_dir, args.production)
    write_report(args.report, config, details)
    status = "PASS" if score >= details["minimumScore"] and not any(item.severity == "critical" for item in findings) else "BLOCKED"
    print(f"OneTap SEO audit: {score}/100 — {status}")
    if status != "PASS":
        sys.exit(1)


if __name__ == "__main__":
    main()
