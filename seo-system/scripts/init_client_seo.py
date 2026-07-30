#!/usr/bin/env python3
"""Create or update a OneTap client SEO config through a guided terminal prompt."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


def ask(label: str, default: str = "", required: bool = False) -> str:
    suffix = f" [{default}]" if default else ""
    while True:
        value = input(f"{label}{suffix}: ").strip()
        if value:
            return value
        if default:
            return default
        if not required:
            return ""
        print("This value is required.")


def yes_no(label: str, default: bool = False) -> bool:
    marker = "Y/n" if default else "y/N"
    while True:
        value = input(f"{label} [{marker}]: ").strip().lower()
        if not value:
            return default
        if value in {"y", "yes"}:
            return True
        if value in {"n", "no"}:
            return False
        print("Enter yes or no.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument(
        "--example",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "client-seo.config.example.json",
    )
    args = parser.parse_args()

    if args.config.exists():
        config = json.loads(args.config.read_text(encoding="utf-8"))
    else:
        config = json.loads(args.example.read_text(encoding="utf-8"))

    business = config["business"]
    location = config["location"]
    content = config["content"]
    pages = config["pages"]
    approvals = config["approvals"]

    business["name"] = ask("Public business name", business.get("name", ""), True)
    business["ownerName"] = ask("Owner or primary contact", business.get("ownerName", ""))
    business["industryKey"] = ask("Industry key", business.get("industryKey", "general-local-service"), True)
    business["schemaType"] = ask("Schema.org business type", business.get("schemaType", "ProfessionalService"), True)
    business["description"] = ask("Approved business description", business.get("description", ""), True)
    business["displayPhone"] = ask("Public phone", business.get("displayPhone", ""), True)
    business["phone"] = ask("Schema phone in +1 format", business.get("phone", ""), True)
    business["email"] = ask("Public email", business.get("email", ""), True)
    business["website"] = ask("Final HTTPS website", business.get("website", ""), True).rstrip("/")
    parsed = urlparse(business["website"])
    if parsed.scheme != "https" or not parsed.netloc:
        raise SystemExit("The final website must be a complete HTTPS URL.")
    business["logo"] = ask("Absolute logo URL", business.get("logo", ""), True)

    location["mode"] = ask("Location mode: storefront or service-area", location.get("mode", "service-area"), True)
    location["publicAddress"] = location["mode"] == "storefront"
    address = location["address"]
    if location["publicAddress"]:
        address["streetAddress"] = ask("Public street address", address.get("streetAddress", ""), True)
        address["postalCode"] = ask("ZIP code", address.get("postalCode", ""), True)
    else:
        address["streetAddress"] = ""
        address["postalCode"] = ""
    address["addressLocality"] = ask("Primary city", address.get("addressLocality", ""), True)
    address["addressRegion"] = ask("State abbreviation", address.get("addressRegion", "CA"), True)
    areas = ask("Service areas, comma separated", ", ".join(location.get("serviceAreas", [])), True)
    location["serviceAreas"] = [item.strip() for item in areas.split(",") if item.strip()]

    content["primaryKeyword"] = ask("Primary search phrase", content.get("primaryKeyword", ""), True)
    content["primaryConversion"] = ask("Primary customer action", content.get("primaryConversion", "Request a quote"), True)
    social_image = ask("Absolute social sharing image URL", config["seo"].get("socialImage", ""), True)
    config["seo"]["socialImage"] = social_image
    config["seo"]["socialImageAlt"] = ask("Social image description", config["seo"].get("socialImageAlt", ""), True)

    home = next((page for page in pages if page.get("path") == "/"), pages[0])
    home["title"] = ask("Homepage title", home.get("title", ""), True)
    home["metaDescription"] = ask("Homepage meta description", home.get("metaDescription", ""), True)
    home["primaryKeyword"] = content["primaryKeyword"]
    home["lastModified"] = date.today().isoformat()

    config["project"]["clientId"] = ask(
        "Client ID (lowercase slug)",
        config["project"].get("clientId", business["name"].lower().replace(" ", "-")),
        True,
    )
    config["project"]["status"] = "production-ready" if yes_no("Mark configuration production-ready?") else "draft"
    config["project"]["lastUpdated"] = date.today().isoformat()

    if config["project"]["status"] == "production-ready":
        print("\nConfirm client approvals:")
        for key in list(approvals):
            if isinstance(approvals[key], bool):
                approvals[key] = yes_no(key.replace("_", " "), approvals[key])
        approvals["approvedBy"] = ask("Approved by", approvals.get("approvedBy", ""), True)
        approvals["approvedDate"] = ask("Approval date", date.today().isoformat(), True)

    args.config.parent.mkdir(parents=True, exist_ok=True)
    args.config.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {args.config}")


if __name__ == "__main__":
    main()
