#!/usr/bin/env python3
"""Run a lightweight live SEO health check for a launched OneTap client site."""

from __future__ import annotations

import argparse
import json
import ssl
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


class LiveParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.h1 = 0
        self.meta: dict[str, str] = {}
        self.canonical = ""
        self.jsonld = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key.lower(): value or "" for key, value in attrs}
        tag = tag.lower()
        if tag == "h1":
            self.h1 += 1
        elif tag == "meta":
            key = (data.get("name") or data.get("property") or "").lower()
            if key:
                self.meta[key] = data.get("content", "")
        elif tag == "link" and "canonical" in data.get("rel", "").lower().split():
            self.canonical = data.get("href", "")
        elif tag == "script" and data.get("type", "").lower() == "application/ld+json":
            self.jsonld += 1


def load(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Unable to load {path}: {exc}") from exc


def fetch(url: str, timeout: int = 20) -> tuple[int, str, str]:
    request = Request(url, headers={"User-Agent": "OneTap-SEO-Health/1.0"})
    try:
        with urlopen(request, timeout=timeout, context=ssl.create_default_context()) as response:
            body = response.read().decode("utf-8", errors="replace")
            return int(response.status), response.geturl(), body
    except HTTPError as exc:
        return int(exc.code), url, exc.read().decode("utf-8", errors="replace")
    except URLError as exc:
        return 0, url, str(exc)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--report", type=Path, default=Path("seo-reports/monthly-live-check.md"))
    args = parser.parse_args()
    config = load(args.config)
    base = config["business"]["website"].rstrip("/")
    home_url = base + "/"
    checks: list[tuple[str, bool, str]] = []

    home_status, final_url, home = fetch(home_url)
    checks.append(("Homepage returns HTTP 200", home_status == 200, f"status={home_status}; final={final_url}"))
    checks.append(("Homepage remains on HTTPS", final_url.startswith("https://"), final_url))

    page = LiveParser()
    if home_status == 200:
        page.feed(home)
        checks.append(("Canonical matches production homepage", page.canonical == home_url, page.canonical or "missing"))
        checks.append(("Homepage is indexable", "noindex" not in page.meta.get("robots", "").lower(), page.meta.get("robots", "missing")))
        checks.append(("Homepage has exactly one H1", page.h1 == 1, f"found={page.h1}"))
        checks.append(("Meta description is present", len(page.meta.get("description", "")) >= 70, page.meta.get("description", "missing")))
        checks.append(("Social sharing image is present", bool(page.meta.get("og:image")), page.meta.get("og:image", "missing")))
        checks.append(("JSON-LD remains installed", page.jsonld > 0, f"blocks={page.jsonld}"))

    for filename in ("robots.txt", "sitemap.xml"):
        status, _, body = fetch(urljoin(home_url, filename))
        checks.append((f"{filename} returns HTTP 200", status == 200, f"status={status}"))
        if filename == "robots.txt" and status == 200:
            checks.append(("robots.txt references the sitemap", f"{base}/sitemap.xml" in body, "sitemap reference"))
        if filename == "sitemap.xml" and status == 200:
            checks.append(("Sitemap includes the canonical homepage", home_url in body, home_url))

    passed = sum(1 for _, ok, _ in checks if ok)
    failed = len(checks) - passed
    status = "PASS" if failed == 0 else "REVIEW REQUIRED"
    lines = [
        "# OneTap Monthly SEO Health Check",
        "",
        f"Client: **{config['business']['name']}**",
        f"Website: **{home_url}**",
        f"Checked: **{datetime.now(timezone.utc).isoformat()}**",
        f"Status: **{status}**",
        f"Checks passed: **{passed}/{len(checks)}**",
        "",
        "## Live checks",
        "",
    ]
    for label, ok, detail in checks:
        lines.append(f"- {'✅' if ok else '❌'} **{label}** — {detail}")
    lines.extend([
        "",
        "## Manual monthly review still required",
        "",
        "- Search Console clicks, impressions, CTR, queries, pages, indexing, and Core Web Vitals",
        "- Client-owned Google Business Profile status, hours, services, photos, and website link",
        "- Primary contact/booking/quote action",
        "- Business facts, pricing, service area, promotions, and content accuracy",
        "",
        "Google controls crawling, indexing, local placement, and rankings. This check does not guarantee a ranking or result.",
        "",
    ])
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text("\n".join(lines), encoding="utf-8")
    print(f"Monthly SEO health check: {status} ({passed}/{len(checks)})")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
