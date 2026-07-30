#!/usr/bin/env python3
"""Generate OneTap metadata, schema, crawl files, and launch records from one approved config."""

from __future__ import annotations

import argparse
import html
import json
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse
from xml.sax.saxutils import escape as xml_escape

APPROVALS = (
    "businessFactsApproved",
    "serviceClaimsApproved",
    "pricesApproved",
    "hoursApproved",
    "serviceAreaApproved",
    "imageRightsConfirmed",
    "googleBusinessProfileClientOwned",
    "noInventedReviewsOrRatings",
)


def load(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Configuration not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def base_url(config: dict[str, Any]) -> str:
    value = str(config["business"]["website"]).strip().rstrip("/")
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise SystemExit("business.website must be a complete HTTP(S) URL")
    return value


def absolute(base: str, value: str) -> str:
    if not value:
        return ""
    parsed = urlparse(value)
    return value if parsed.scheme and parsed.netloc else urljoin(base + "/", value.lstrip("/"))


def required(config: dict[str, Any], production: bool) -> None:
    business = config.get("business", {})
    for key in ("name", "industryKey", "schemaType", "description", "phone", "displayPhone", "email", "website", "logo"):
        if not business.get(key):
            raise SystemExit(f"Missing required value: business.{key}")
    if not config.get("services") or not config.get("pages"):
        raise SystemExit("At least one service and one page are required")
    if production:
        missing = [key for key in APPROVALS if not config.get("approvals", {}).get(key)]
        if missing:
            raise SystemExit("Production generation blocked; missing approvals: " + ", ".join(missing))
        if not config["approvals"].get("approvedBy") or not config["approvals"].get("approvedDate"):
            raise SystemExit("Production generation requires approvedBy and approvedDate")
        if not base_url(config).startswith("https://"):
            raise SystemExit("Production website must use HTTPS")


def area_nodes(config: dict[str, Any]) -> list[dict[str, str]]:
    return [{"@type": "City", "name": item.strip()} for item in config["location"].get("serviceAreas", []) if item.strip()]


def address_node(config: dict[str, Any]) -> dict[str, str] | None:
    address = config["location"].get("address", {})
    if not address.get("addressLocality") or not address.get("addressRegion"):
        return None
    node = {
        "@type": "PostalAddress",
        "addressLocality": address["addressLocality"],
        "addressRegion": address["addressRegion"],
        "addressCountry": address.get("addressCountry", "US"),
    }
    if config["location"].get("publicAddress"):
        if address.get("streetAddress"):
            node["streetAddress"] = address["streetAddress"]
        if address.get("postalCode"):
            node["postalCode"] = address["postalCode"]
    return node


def opening_hours(config: dict[str, Any]) -> list[dict[str, Any]]:
    output = []
    for item in config.get("hours", []):
        if item.get("days") and item.get("opens") and item.get("closes"):
            output.append({
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": [f"https://schema.org/{day}" for day in item["days"]],
                "opens": item["opens"],
                "closes": item["closes"],
            })
    return output


def offer_catalog(config: dict[str, Any], base: str) -> dict[str, Any]:
    offers = []
    for service in config["services"]:
        offered = {
            "@type": "Service",
            "name": service.get("name", ""),
            "description": service.get("description", ""),
            "provider": {"@id": f"{base}/#business"},
        }
        offer: dict[str, Any] = {
            "@type": "Offer",
            "url": absolute(base, service.get("urlPath", "/#services")),
            "itemOffered": offered,
        }
        if str(service.get("price", "")).strip():
            offer["priceSpecification"] = {
                "@type": "PriceSpecification",
                "price": str(service["price"]),
                "priceCurrency": service.get("priceCurrency", "USD"),
            }
        offers.append(offer)
    return {"@type": "OfferCatalog", "name": f"{config['business']['name']} services", "itemListElement": offers}


def schema_graph(config: dict[str, Any]) -> dict[str, Any]:
    business = config["business"]
    seo = config["seo"]
    content = config["content"]
    base = base_url(config)
    business_id = f"{base}/#business"
    website_id = f"{base}/#website"
    node: dict[str, Any] = {
        "@type": business["schemaType"],
        "@id": business_id,
        "name": business["name"],
        "url": f"{base}/",
        "logo": absolute(base, business["logo"]),
        "image": absolute(base, seo["socialImage"]),
        "description": business["description"],
        "telephone": business["phone"],
        "email": business["email"],
        "priceRange": business.get("priceRange", ""),
        "currenciesAccepted": business.get("currenciesAccepted", "USD"),
        "paymentAccepted": business.get("paymentAccepted", []),
        "areaServed": area_nodes(config),
        "openingHoursSpecification": opening_hours(config),
    }
    for key in ("legalName", "slogan", "foundingDate"):
        if business.get(key):
            node[key] = business[key]
    if business.get("socialProfiles"):
        node["sameAs"] = business["socialProfiles"]
    address = address_node(config)
    if address:
        node["address"] = address
    lat, lng = str(config["location"].get("latitude", "")).strip(), str(config["location"].get("longitude", "")).strip()
    if lat and lng:
        node["geo"] = {"@type": "GeoCoordinates", "latitude": lat, "longitude": lng}
    if seo.get("includeServiceCatalog", True):
        node["hasOfferCatalog"] = offer_catalog(config, base)

    graph: list[dict[str, Any]] = [
        node,
        {
            "@type": "WebSite",
            "@id": website_id,
            "url": f"{base}/",
            "name": business["name"],
            "description": business["description"],
            "publisher": {"@id": business_id},
            "inLanguage": seo.get("language", "en-US"),
        },
        {
            "@type": "Service",
            "@id": f"{base}/#primary-service",
            "name": content.get("primaryConversion", "Local service"),
            "serviceType": content["primaryKeyword"],
            "description": business["description"],
            "provider": {"@id": business_id},
            "areaServed": area_nodes(config),
            "url": f"{base}/#services",
        },
    ]
    faq = content.get("faq", [])
    if seo.get("includeFaqSchema") and faq:
        graph.append({
            "@type": "FAQPage",
            "@id": f"{base}/#faq",
            "mainEntity": [
                {"@type": "Question", "name": item["question"], "acceptedAnswer": {"@type": "Answer", "text": item["answer"]}}
                for item in faq
            ],
        })
    verified = content.get("verifiedReviews", {})
    if verified.get("enabled"):
        if not verified.get("ratingValue") or not verified.get("reviewCount") or not verified.get("source"):
            raise SystemExit("Verified review schema requires ratingValue, reviewCount, and source")
        node["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": str(verified["ratingValue"]),
            "reviewCount": str(verified["reviewCount"]),
        }
    return {"@context": "https://schema.org", "@graph": graph}


def head_markup(config: dict[str, Any], graph: dict[str, Any]) -> str:
    base = base_url(config)
    home = next((page for page in config["pages"] if page.get("path") == "/"), config["pages"][0])
    seo, business = config["seo"], config["business"]
    title, description = html.escape(home["title"], quote=True), html.escape(home["metaDescription"], quote=True)
    image = absolute(base, seo["socialImage"])
    verification = f'<meta name="google-site-verification" content="{html.escape(seo["searchConsoleVerification"], quote=True)}" />\n' if seo.get("searchConsoleVerification") else ""
    return f'''<title>{title}</title>
<meta name="description" content="{description}" />
<meta name="robots" content="{html.escape(seo.get('defaultRobots', 'index,follow,max-image-preview:large'), quote=True)}" />
<meta name="author" content="{html.escape(business['name'], quote=True)}" />
<link rel="canonical" href="{base}/" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="{html.escape(business['name'], quote=True)}" />
<meta property="og:locale" content="{html.escape(seo.get('locale', 'en_US'), quote=True)}" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{description}" />
<meta property="og:url" content="{base}/" />
<meta property="og:image" content="{html.escape(image, quote=True)}" />
<meta property="og:image:alt" content="{html.escape(seo['socialImageAlt'], quote=True)}" />
<meta name="twitter:card" content="{html.escape(seo.get('twitterCard', 'summary_large_image'), quote=True)}" />
<meta name="twitter:title" content="{title}" />
<meta name="twitter:description" content="{description}" />
<meta name="twitter:image" content="{html.escape(image, quote=True)}" />
{verification}<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False, separators=(',', ':'))}</script>
'''


def robots(config: dict[str, Any]) -> str:
    base = base_url(config)
    lines = ["User-agent: *", "Allow: /"]
    lines.extend(f"Disallow: {path}" for path in config["seo"].get("privatePaths", []))
    lines.extend(["", f"Sitemap: {base}/sitemap.xml", f"Host: {urlparse(base).netloc}", ""])
    return "\n".join(lines)


def sitemap(config: dict[str, Any]) -> str:
    base = base_url(config)
    entries = []
    for page in config["pages"]:
        if not page.get("index", True):
            continue
        loc = f"{base}/" if page["path"] == "/" else absolute(base, page["path"])
        entries.append(
            "  <url>\n"
            f"    <loc>{xml_escape(loc)}</loc>\n"
            f"    <lastmod>{xml_escape(page.get('lastModified') or date.today().isoformat())}</lastmod>\n"
            f"    <changefreq>{xml_escape(page.get('changeFrequency', 'monthly'))}</changefreq>\n"
            f"    <priority>{xml_escape(str(page.get('priority', '0.5')))}</priority>\n"
            "  </url>"
        )
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(entries) + "\n</urlset>\n"


def manifest(config: dict[str, Any]) -> dict[str, Any]:
    business, base = config["business"], base_url(config)
    return {
        "name": business["name"],
        "short_name": business["name"][:24],
        "description": business["description"],
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#111111",
        "icons": [{"src": absolute(base, business["logo"]), "sizes": "512x512", "type": "image/png"}],
    }


def launch_record(config: dict[str, Any]) -> str:
    base, name = base_url(config), config["business"]["name"]
    return f"""# Search Console and Google Business Launch Record

Client: **{name}**  
Production URL: **{base}/**

- [ ] Verify the client-owned Search Console domain property
- [ ] Submit `{base}/sitemap.xml`
- [ ] Inspect `{base}/` and request indexing after final approval
- [ ] Validate structured data and record PageSpeed baseline
- [ ] Confirm the client owns the Google Business Profile
- [ ] Add OneTap Creative as manager only
- [ ] Match business name, phone, website, hours, services, and address/service area
- [ ] Record profile verification status

Google controls crawling, indexing, profile verification, local placement, and rankings. OneTap Creative does not guarantee a particular ranking or result.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("seo-output"))
    parser.add_argument("--production", action="store_true")
    args = parser.parse_args()
    config = load(args.config)
    required(config, args.production)
    args.output.mkdir(parents=True, exist_ok=True)
    graph = schema_graph(config)
    base = base_url(config)
    files = {
        "head-seo.html": head_markup(config, graph),
        "schema-graph.json": json.dumps(graph, ensure_ascii=False, indent=2) + "\n",
        "robots.txt": robots(config),
        "sitemap.xml": sitemap(config),
        "manifest.webmanifest": json.dumps(manifest(config), ensure_ascii=False, indent=2) + "\n",
        "search-console-launch.md": launch_record(config),
        "seo-baseline.json": json.dumps({
            "systemVersion": config["systemVersion"],
            "clientId": config["project"]["clientId"],
            "businessName": config["business"]["name"],
            "productionUrl": f"{base}/",
            "primaryKeyword": config["content"]["primaryKeyword"],
            "schemaType": config["business"]["schemaType"],
            "serviceAreas": config["location"].get("serviceAreas", []),
            "generatedDate": date.today().isoformat(),
            "minimumLaunchScore": config.get("quality", {}).get("minimumLaunchScore", 90),
        }, ensure_ascii=False, indent=2) + "\n",
    }
    for name, content in files.items():
        (args.output / name).write_text(content, encoding="utf-8")
    print(f"Generated OneTap SEO package for {config['business']['name']} in {args.output}")


if __name__ == "__main__":
    main()
