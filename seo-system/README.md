# OneTap Creative Client SEO System v1.0

This folder is the agency-wide SEO operating system for every OneTap Creative client website.

It turns the OneTap **advanced SEO foundation** into a repeatable production workflow with:

- one approved source of business facts
- industry-aware LocalBusiness structured data
- generated metadata, canonical, robots, sitemap, manifest, and JSON-LD
- automated prelaunch checks that block another client's information and unfinished placeholders
- a 100-point launch scorecard
- Search Console and Google Business Profile launch procedures
- monthly and quarterly health checks
- GitHub Actions templates for continuous quality control

## Non-negotiable rule

A client website must not launch unless:

1. `client-seo.config.json` is complete and approved.
2. `build_seo.py` generates the SEO package without errors.
3. `audit_seo.py` reports no critical errors.
4. The launch score is at least **90/100**.
5. The client-approved business name, phone, location/service area, hours, services, prices, claims, and images match the public website.
6. Search Console, sitemap submission, and client-owned Google Business Profile steps are recorded.
7. No ranking, traffic, lead, review, or performance claim is invented.

## Quick start

```bash
cp seo-system/client-seo.config.example.json client-seo.config.json
python seo-system/scripts/init_client_seo.py --config client-seo.config.json
python seo-system/scripts/build_seo.py \
  --config client-seo.config.json \
  --output seo-output

python seo-system/scripts/audit_seo.py \
  --config client-seo.config.json \
  --site-dir . \
  --production \
  --report seo-output/prelaunch-audit.md
```

Generated files:

```text
seo-output/
├── head-seo.html
├── schema-graph.json
├── robots.txt
├── sitemap.xml
├── manifest.webmanifest
├── seo-baseline.json
└── search-console-launch.md
```

Copy or integrate the generated files into the client website, then run the audit again against the final production build.

## Recommended repository layout

```text
client-site/
├── client-seo.config.json
├── index.html
├── images/
├── robots.txt
├── sitemap.xml
├── manifest.webmanifest
├── seo-system/
└── seo-output/
```

## What the standard foundation includes

- client-approved business identity and local information
- local keyword and search-intent mapping
- one clear H1 and logical heading structure
- unique title and meta description
- canonical URL and production indexability
- Open Graph and large-image social sharing
- appropriate LocalBusiness subtype
- connected LocalBusiness, WebSite, Service, OfferCatalog, and optional visible FAQ schema
- image names, alt text, dimensions, compression, and lazy-loading checks
- robots.txt, XML sitemap, and web manifest
- mobile, accessibility, conversion, and technical checks
- Search Console verification, sitemap submission, URL inspection, and baseline recording
- client-owned Google Business Profile alignment
- monthly crawl/indexing/website checks and quarterly strategy review

## What the standard foundation does not promise

- first-place or first-page rankings
- a specific number of visitors, calls, bookings, leads, or sales
- guaranteed Google Business Profile approval
- ongoing blog production
- backlink campaigns
- paid advertising
- multi-location doorway pages
- large-scale directory cleanup
- campaign-level SEO outside the signed scope

## Agency workflow

1. **Truth intake** — Confirm the client's exact public business facts and authorization.
2. **Keyword map** — Assign one primary search intent to each indexable page.
3. **Build** — Generate and integrate the technical SEO package.
4. **Content review** — Verify that page copy answers the target customer's real questions.
5. **Automated audit** — Resolve all critical errors and reach at least 90/100.
6. **Manual validation** — Rich Results Test, PageSpeed Insights, mobile and form tests.
7. **Launch** — Connect the final domain, Search Console, sitemap, and Business Profile.
8. **Baseline** — Record indexed pages, Core Web Vitals, clicks, impressions, ranking queries, and profile status.
9. **Monthly care** — Run the website health check and review Search Console.
10. **Quarterly review** — Refresh content and priorities using real performance data.

## Official reference standard

The system is aligned to current Google Search Central, web.dev, and Schema.org guidance. Recheck these sources during quarterly system reviews:

- https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- https://developers.google.com/search/docs/fundamentals/get-started-developers
- https://developers.google.com/search/docs/appearance/structured-data/local-business
- https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- https://web.dev/articles/vitals
- https://schema.org/LocalBusiness
- https://schema.org/Service

## Files in this system

- `client-seo.config.example.json` — approved client facts and SEO decisions
- `client-seo.config.schema.json` — configuration contract
- `industry-schema-map.json` — industry defaults
- `SEO-DELIVERY-STANDARD.md` — scope and production standard
- `SEO-SCORECARD.md` — launch scoring model
- `scripts/init_client_seo.py` — guided configuration creator
- `scripts/build_seo.py` — generated SEO assets
- `scripts/audit_seo.py` — prelaunch quality gate
- `scripts/monthly_seo_check.py` — live production health report
- `workflows/seo-quality-gate.yml` — PR/push validation template
- `workflows/monthly-seo-watch.yml` — scheduled production check template
- `checklists/` — launch, Search Console/GBP, and monthly/quarterly procedures
- `examples/sample-site/` — working validation fixture
