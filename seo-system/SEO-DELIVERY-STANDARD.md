# OneTap Creative SEO Delivery Standard

## Purpose

Every OneTap client website receives the same advanced SEO foundation at launch. The system is designed to make each website crawlable, understandable, locally relevant, trustworthy, mobile-friendly, and measurable without promising a specific ranking.

## Phase 1 — Approved business truth

Before SEO work begins, confirm in writing:

- exact public business name
- primary contact and client authorization
- client-owned Google Business Profile status
- public phone and email
- storefront address or service-area model
- service cities and realistic travel radius
- business hours
- services, prices, payment methods, and policies
- owner/team information
- licenses, certifications, years of experience, awards, and other claims
- image ownership or marketing-use permission
- official social profiles

No claim may be added because it “sounds good.” Reviews, ratings, years in business, licenses, customer counts, and service areas must be supported by client-approved facts.

## Phase 2 — Search intent and keyword map

For every indexable page record:

- one primary search intent
- one primary phrase
- supporting phrases
- target customer
- target location
- primary conversion
- page title
- meta description
- H1
- sections required to answer the query
- internal links
- structured-data type

Rules:

- Do not create near-duplicate city pages solely to rank in neighboring cities.
- Do not repeat a keyword unnaturally.
- Do not target a service the client does not actually provide.
- Do not target a city outside the real service area.
- Prefer clear customer language over SEO jargon.
- A one-page client website must still cover services, trust, location/service area, FAQs, and the primary action.

## Phase 3 — Page implementation

Every public homepage must include:

- HTTPS production URL
- one clear H1
- logical H2/H3 structure
- unique title and meta description
- self-referencing canonical
- index/follow robots directive
- Open Graph and large-image Twitter card
- visible business name, phone, location/service area, hours, and service information
- descriptive image names and alt text
- explicit image dimensions when practical
- compressed modern image formats
- LocalBusiness subtype, WebSite, Service, and OfferCatalog JSON-LD
- FAQPage only when the same questions and answers are visibly present
- no unverified AggregateRating
- robots.txt
- sitemap.xml containing canonical indexable URLs only
- manifest and icons
- accessible mobile navigation and forms
- tested primary conversion

## Phase 4 — Automated launch gate

Run:

```bash
python seo-system/scripts/build_seo.py --config client-seo.config.json --output seo-output --production

python seo-system/scripts/audit_seo.py --config client-seo.config.json --site-dir . --production --report seo-output/prelaunch-audit.md
```

The website is blocked from launch when:

- a critical error exists
- the score is below 90
- approvals are incomplete
- production contains noindex
- canonical, sitemap, or schema uses the wrong domain
- another client’s name or content remains
- placeholders remain
- structured data contains invented ratings
- the homepage has zero or multiple H1 elements
- the final form or primary action fails

## Phase 5 — Manual validation

Automated tests do not replace human review. Complete:

- mobile phone review
- desktop review
- keyboard navigation
- form delivery
- thank-you page
- phone/text/booking links
- Google Rich Results Test
- PageSpeed Insights
- final source review for canonical and JSON-LD
- legal and privacy review
- client review and launch approval

## Phase 6 — Search Console and Google Business Profile

- Verify the final domain property.
- Submit the final sitemap.
- Inspect the homepage.
- Request indexing after final launch.
- Record indexed-page baseline.
- Confirm the client owns the Business Profile.
- Add OneTap as manager only.
- Align name, phone, address/service area, category, hours, services, and website URL.
- Guide the client through Google verification.
- Never guarantee approval or ranking.

## Phase 7 — Monthly care

Each month:

- run the live SEO health check
- inspect Search Console performance and indexing
- inspect Core Web Vitals
- inspect Google Business Profile status
- test the primary lead action
- confirm business facts remain accurate
- correct technical issues
- document changes and recommendations

## Phase 8 — Quarterly strategy review

Every quarter:

- compare performance by query and page
- identify high-impression/low-CTR opportunities
- identify service questions not answered on the site
- refresh titles or content only when supported by data
- review competitors without copying them
- review new Google Search documentation
- update the OneTap SEO system when standards change
- preserve a backup before system changes

## Handoff record

Each client folder must contain:

- approved `client-seo.config.json`
- keyword map
- prelaunch audit markdown and JSON
- generated SEO package
- Search Console launch record
- Business Profile status
- PageSpeed baseline
- client approval
- monthly reports
