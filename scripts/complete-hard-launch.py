from __future__ import annotations

import json
import subprocess
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPROVED_COMMIT = "71c483b3f939025eead2738354aa46ce235120c2"
FORM_EMAIL = "clarence.workflow@gmail.com"
PUBLIC_EMAIL = "hello@onetapcreative.com"


def git_show(path: str) -> str:
    return subprocess.check_output(
        ["git", "show", f"{APPROVED_COMMIT}:{path}"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    )


def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content.rstrip() + "\n", encoding="utf-8")


# Restore the reviewed $179 public launch files that were accidentally overwritten.
for restored_path in (
    "index.html",
    "styles.css",
    "script.js",
    "terms.html",
    "privacy.html",
    "thank-you.html",
):
    write(restored_path, git_show(restored_path))

# Remove unsupported demo rating claims, unify the lead inbox, and improve form follow-up.
index_path = ROOT / "index.html"
index = index_path.read_text(encoding="utf-8")
index = index.replace("https://formsubmit.co/codicta@gmail.com", f"https://formsubmit.co/{FORM_EMAIL}")
index = index.replace('<div class="stars">5.0 ★★★★★</div><p>Local Business</p>', '<div class="stars">Business profile preview</div><p>Example layout</p>')
index = index.replace("<span>★ 5.0 reviews</span>", "<span>Trust section</span>")
index = index.replace(
    '<input name="_template" type="hidden" value="table"/><input name="_captcha" type="hidden" value="true"/>',
    '<input name="_template" type="hidden" value="table"/><input name="_captcha" type="hidden" value="true"/><input id="lead-replyto" name="_replyto" type="hidden"/><input name="_autoresponse" type="hidden" value="Thank you for contacting OneTap Creative. Your project request was received and will normally be reviewed within one business day. No payment was collected. If the project is a fit, the next steps are a written scope, client agreement, first payment, and the mobile onboarding portal."/>',
)
index = index.replace(
    '<label>Email *<input autocomplete="email" name="Email" required type="email"/></label>',
    '<label>Email *<input autocomplete="email" id="lead-email" name="Email" required type="email"/></label>',
)
index = index.replace('styles.css?v=pricing-179', 'styles.css?v=hard-launch-1')
index = index.replace('script.js?v=pricing-179', 'script.js?v=hard-launch-1')
write("index.html", index)

# Improve attribution, FormSubmit reply routing, and analytics-ready lead events.
script_path = ROOT / "script.js"
script = script_path.read_text(encoding="utf-8")
script = script.replace(
    "const leadForm = document.querySelector('#lead-form');\n",
    "const leadForm = document.querySelector('#lead-form');\nconst leadEmail = document.querySelector('#lead-email');\nconst leadReplyTo = document.querySelector('#lead-replyto');\n",
)
script = script.replace(
    "if (formNextUrl) formNextUrl.value = new URL('thank-you.html', window.location.href).href;\n",
    "if (formNextUrl) formNextUrl.value = new URL('thank-you.html', window.location.href).href;\nconst syncLeadReplyTo = () => { if (leadReplyTo && leadEmail) leadReplyTo.value = leadEmail.value.trim(); };\nleadEmail?.addEventListener('input', syncLeadReplyTo);\nsyncLeadReplyTo();\n",
)
script = script.replace(
    "leadForm?.addEventListener('submit', () => {\n",
    "leadForm?.addEventListener('submit', () => {\n  syncLeadReplyTo();\n",
)
script = script.replace(
    "window.dataLayer.push({\n    event: 'onetap_lead_submit',",
    "window.dataLayer.push({ event: 'generate_lead', lead_type: 'website_project_request' });\n  if (typeof window.gtag === 'function') window.gtag('event', 'generate_lead', { lead_type: 'website_project_request' });\n  window.dataLayer.push({\n    event: 'onetap_lead_submit',",
)
write("script.js", script)

# Record lead completion on the confirmation page using the recommended event name when analytics is connected.
thank_path = ROOT / "thank-you.html"
thank = thank_path.read_text(encoding="utf-8")
thank = thank.replace(
    "window.dataLayer=window.dataLayer||[];window.dataLayer.push({event:'onetap_lead_complete'});",
    "window.dataLayer=window.dataLayer||[];window.dataLayer.push({event:'onetap_lead_complete'});window.dataLayer.push({event:'generate_lead',lead_type:'website_project_request_complete'});if(typeof window.gtag==='function'){window.gtag('event','generate_lead',{lead_type:'website_project_request_complete'});}",
)
thank = thank.replace('styles.css?v=pricing-179', 'styles.css?v=hard-launch-1')
write("thank-you.html", thank)

# Keep policy pages on the reviewed scope and current stylesheet version.
for page in ("terms.html", "privacy.html"):
    page_path = ROOT / page
    page_text = page_path.read_text(encoding="utf-8")
    page_text = page_text.replace('styles.css?v=pricing-179', 'styles.css?v=hard-launch-1')
    page_text = page_text.replace('styles.css?v=launch-100', 'styles.css?v=hard-launch-1')
    write(page, page_text)

# Unify the private onboarding form with the same verified internal inbox.
onboarding_path = ROOT / "onboarding/index.html"
onboarding = onboarding_path.read_text(encoding="utf-8")
onboarding = onboarding.replace("https://formsubmit.co/codicta@gmail.com", f"https://formsubmit.co/{FORM_EMAIL}")
onboarding = onboarding.replace(
    '<input type="hidden" name="_captcha" value="false" />',
    '<input type="hidden" name="_captcha" value="false" />\n      <input type="hidden" id="onboarding-replyto" name="_replyto" />\n      <input type="hidden" name="_autoresponse" value="OneTap Creative received your completed onboarding form. Your business information and uploaded files will be reviewed. You will be contacted if anything is missing before production begins." />',
)
onboarding = onboarding.replace('onboarding.css?v=1', 'onboarding.css?v=hard-launch-1')
write("onboarding/index.html", onboarding)

onboarding_js_path = ROOT / "onboarding/onboarding.js"
onboarding_js = onboarding_js_path.read_text(encoding="utf-8")
onboarding_js = onboarding_js.replace(
    "const SYSTEM_FIELDS = new Set(['_subject', '_template', '_captcha', '_next', '_honey', 'Plan', 'Portal Version', 'Onboarding Summary', 'Uploaded File Names']);",
    "const SYSTEM_FIELDS = new Set(['_subject', '_template', '_captcha', '_next', '_honey', '_replyto', '_autoresponse', 'Plan', 'Portal Version', 'Onboarding Summary', 'Uploaded File Names']);",
)
onboarding_js = onboarding_js.replace(
    "const imagePreview = document.querySelector('#image-preview');\n",
    "const imagePreview = document.querySelector('#image-preview');\n  const replyToField = document.querySelector('#onboarding-replyto');\n  const clientEmailField = document.querySelector('#client-email');\n",
)
onboarding_js = onboarding_js.replace(
    "if (formNext) formNext.value = new URL('success.html', window.location.href).href;\n",
    "if (formNext) formNext.value = new URL('success.html', window.location.href).href;\n  const syncReplyTo = () => { if (replyToField && clientEmailField) replyToField.value = clientEmailField.value.trim(); };\n  clientEmailField?.addEventListener('input', syncReplyTo);\n",
)
onboarding_js = onboarding_js.replace(
    "form.addEventListener('submit', event => {\n",
    "form.addEventListener('submit', event => {\n    syncReplyTo();\n",
)
onboarding_js = onboarding_js.replace(
    "restoreDraft();\n  syncConditionals();",
    "restoreDraft();\n  syncReplyTo();\n  syncConditionals();",
)
write("onboarding/onboarding.js", onboarding_js)

readme_path = ROOT / "onboarding/README.md"
if readme_path.exists():
    readme = readme_path.read_text(encoding="utf-8")
    readme = readme.replace("`codicta@gmail.com`", f"`{FORM_EMAIL}`")
    readme = readme.replace("After a professional OneTap mailbox is activated and tested, update the form action in `onboarding/index.html`.", f"The current verified internal delivery inbox is `{FORM_EMAIL}`. After `{PUBLIC_EMAIL}` is activated and tested, update both public and onboarding form actions together.")
    write("onboarding/README.md", readme)

# Harden crawler handling for private workflow pages.
robots_path = ROOT / "robots.txt"
robots = robots_path.read_text(encoding="utf-8")
if "Disallow: /onboarding/" not in robots:
    robots = robots.replace("Disallow: /thank-you.html", "Disallow: /thank-you.html\nDisallow: /onboarding/")
write("robots.txt", robots)

# Refresh sitemap dates while retaining only public indexable pages.
write(
    "sitemap.xml",
    """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  <url>
    <loc>https://onetapcreative.com/</loc>
    <lastmod>2026-07-30</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
    <image:image><image:loc>https://onetapcreative.com/assets/images/onetap-og-direction.jpg</image:loc><image:title>OneTap Creative complete online presence service</image:title></image:image>
  </url>
  <url><loc>https://onetapcreative.com/terms.html</loc><lastmod>2026-07-30</lastmod><changefreq>yearly</changefreq><priority>0.3</priority></url>
  <url><loc>https://onetapcreative.com/privacy.html</loc><lastmod>2026-07-30</lastmod><changefreq>yearly</changefreq><priority>0.3</priority></url>
</urlset>""",
)

# One source of truth for the public offer and operational cutover items.
write(
    "launch-config.json",
    json.dumps(
        {
            "brand": "OneTap Creative",
            "productionDomain": "https://onetapcreative.com/",
            "monthlyPrice": 179,
            "minimumMonths": 3,
            "initialCommitmentTotal": 537,
            "setupFee": 0,
            "postMinimumNoticeDays": 30,
            "prelaunchRevisionRounds": 2,
            "monthlyUpdateMinutes": 30,
            "firstReviewTargetBusinessDays": "7-10",
            "leadResponseTarget": "within one business day",
            "seoScope": "advanced SEO foundation",
            "verifiedInternalFormInbox": FORM_EMAIL,
            "plannedProfessionalMailbox": PUBLIC_EMAIL,
            "paymentProvider": "Square",
            "publicPaymentCollection": False,
            "onboardingRoute": "/onboarding/",
        },
        indent=2,
    ),
)

# Regression audit: public pricing, scope, trust, forms, crawl files, and operational kit.
write(
    "scripts/audit-public-launch.py",
    r'''from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
config = json.loads((ROOT / "launch-config.json").read_text(encoding="utf-8"))
files = {
    "index": (ROOT / "index.html").read_text(encoding="utf-8"),
    "terms": (ROOT / "terms.html").read_text(encoding="utf-8"),
    "privacy": (ROOT / "privacy.html").read_text(encoding="utf-8"),
    "thank": (ROOT / "thank-you.html").read_text(encoding="utf-8"),
    "script": (ROOT / "script.js").read_text(encoding="utf-8"),
    "onboarding": (ROOT / "onboarding/index.html").read_text(encoding="utf-8"),
    "robots": (ROOT / "robots.txt").read_text(encoding="utf-8"),
    "sitemap": (ROOT / "sitemap.xml").read_text(encoding="utf-8"),
}
combined = "\n".join(files.values())
errors = []

def require(condition, message):
    if not condition:
        errors.append(message)

require("$179" in files["index"], "Homepage is missing the approved $179 price")
require("$537" in files["index"], "Homepage is missing the $537 initial commitment")
require("advanced SEO foundation" in files["index"], "Homepage is missing the advanced SEO foundation")
require("Two organized revision rounds" in files["index"], "Homepage is missing two prelaunch revision rounds")
require("30 minutes" in files["index"], "Homepage is missing the monthly update allowance")
require("$149" not in combined and "$447" not in combined, "Old $149/$447 pricing remains")
require("Basic local SEO" not in combined and "basic local SEO" not in combined, "Old basic SEO language remains")
require("codicta@gmail.com" not in combined, "Old onboarding inbox remains")
require(files["index"].count("https://formsubmit.co/clarence.workflow@gmail.com") == 1, "Public form inbox is not the verified inbox")
require(files["onboarding"].count("https://formsubmit.co/clarence.workflow@gmail.com") == 1, "Onboarding form inbox is not the verified inbox")
require("_autoresponse" in files["index"] and "_autoresponse" in files["onboarding"], "Confirmation email fields are missing")
require("_replyto" in files["index"] and "_replyto" in files["onboarding"], "Reply-To routing is missing")
require("★ 5.0 reviews" not in files["index"] and "5.0 ★★★★★" not in files["index"], "Unsupported demo review claims remain")
require('<link rel="canonical" href="https://onetapcreative.com/"' in files["index"], "Static production canonical is missing")
require("generate_lead" in files["script"] and "generate_lead" in files["thank"], "Lead analytics events are missing")
require("Disallow: /onboarding/" in files["robots"], "Private onboarding route is not blocked in robots.txt")
require("https://onetapcreative.com/" in files["sitemap"], "Production homepage is missing from sitemap")
require("attorney review" not in files["terms"].lower(), "Internal attorney reminder is visible in public terms")
require("mailto:" not in files["index"], "A personal email is publicly exposed on the homepage")
for required in (
    "client-operations/CLIENT-SERVICE-AGREEMENT-TEMPLATE.md",
    "client-operations/SCOPE-OF-WORK-TEMPLATE.md",
    "client-operations/GBP-MANAGER-AUTHORIZATION.md",
    "client-operations/DISCOVERY-CALL-SCRIPT.md",
    "client-operations/PROPOSAL-AND-FOLLOW-UP-TEMPLATES.md",
    "client-operations/MONTHLY-CARE-SUMMARY-TEMPLATE.md",
    "client-operations/LEAD-TRACKER.csv",
    "launch/HARD-LAUNCH-RUNBOOK.md",
    "launch/SQUARE-PAYMENT-SETUP.md",
    "launch/PROFESSIONAL-EMAIL-CUTOVER.md",
    "launch/ANALYTICS-ACTIVATION.md",
    "launch/MOCK-CLIENT-TEST.md",
):
    require((ROOT / required).exists(), f"Missing launch asset: {required}")

if errors:
    print("OneTap public launch audit: BLOCKED")
    for item in errors:
        print(f"- {item}")
    sys.exit(1)
print("OneTap public launch audit: PASS")
print(f"Offer: ${config['monthlyPrice']}/month, {config['minimumMonths']}-month minimum, ${config['initialCommitmentTotal']} initial commitment")
''',
)

write(
    ".github/workflows/validate-public-launch.yml",
    """name: Validate OneTap Public Launch

on:
  pull_request:
    paths:
      - "index.html"
      - "styles.css"
      - "script.js"
      - "terms.html"
      - "privacy.html"
      - "thank-you.html"
      - "robots.txt"
      - "sitemap.xml"
      - "onboarding/**"
      - "launch-config.json"
      - "launch/**"
      - "client-operations/**"
      - "scripts/audit-public-launch.py"
      - ".github/workflows/validate-public-launch.yml"
  push:
    branches: [main]
    paths:
      - "index.html"
      - "terms.html"
      - "thank-you.html"
      - "onboarding/**"
      - "launch-config.json"

permissions:
  contents: read

jobs:
  public-launch-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python scripts/audit-public-launch.py
""",
)

# Client-facing and internal operating templates.
write(
    "client-operations/README.md",
    """# OneTap Creative Client Operations Kit

Use this folder after a qualified lead responds positively.

Required order:

1. Complete the discovery call.
2. Personalize the scope attachment.
3. Send the client service agreement and scope for signature.
4. Send the secure Square recurring-payment link.
5. Confirm the first $179 payment.
6. Send the private onboarding link.
7. Review onboarding and identify missing information.
8. Build, review, approve, launch, and begin monthly care.

Do not send the onboarding portal before agreement and first payment. Do not request passwords. The client owns the Google Business Profile and OneTap receives manager access only.
""",
)

write(
    "client-operations/CLIENT-SERVICE-AGREEMENT-TEMPLATE.md",
    """# OneTap Creative Client Service Agreement — Template

> Draft business template. Personalize for each client and obtain qualified legal review before relying on it as the final agreement.

## Parties and effective date

This agreement is between **OneTap Creative** (Service Provider) and **[CLIENT LEGAL NAME / BUSINESS NAME]** (Client), effective **[DATE]**.

## Service

OneTap will provide the Complete Online Presence Plan described in the attached Scope of Work. The standard plan is $179 per month with no standard setup fee and an initial three-month minimum commitment totaling $537.

## Payment and term

- The first $179 payment is due before onboarding and begins the three-month commitment.
- Monthly billing continues on the agreed billing date.
- After the first three months, service continues month-to-month.
- Cancellation after the minimum requires 30 days’ written notice.
- Payments covering an active billing period are not partially refunded.
- A failed payment may receive a seven-day grace period.
- OneTap may suspend hosting, support, and related services after 14 days of nonpayment following written notice.
- The agreed monthly price is protected for the first 12 months of continuous service. Future changes require advance written notice.

## Included website scope

Unless the attached scope states otherwise, the plan includes one custom mobile-first page with approximately 8–10 sections, one primary conversion action, domain registration and renewal while active, hosting, SSL, basic backups, an advanced SEO foundation, Search Console setup, Google Business Profile assistance, two organized prelaunch revision rounds, up to 30 minutes of reasonable monthly updates, maintenance, and technical support.

## Client responsibilities

The Client will provide accurate business facts, authorized content and images, timely feedback, approvals, and any required verification. The Client will not send passwords through public forms or email. Client delays may delay delivery without pausing the initial commitment.

## Reviews and approvals

OneTap will provide a review link. Each included revision round must be submitted as one organized list. Written approval authorizes launch. Approval includes business information, services, pricing, hours, service area, images, claims, forms, and primary conversion path.

## Domain, website, and offboarding

OneTap provides and connects the agreed domain and manages the website files, hosting, SSL, backups, and technical system while the plan is active. Domain registration, ownership, transfer, website-file transfer, buyout, cancellation, and offboarding will follow the personalized Scope of Work. Accounts must be current before transfer or offboarding assistance.

## Google Business Profile and SEO

The Client owns the Google Business Profile. OneTap receives manager access only. Google controls verification, approval, suspension, indexing, Maps placement, and search rankings. OneTap does not guarantee rankings, traffic, leads, bookings, sales, or profile approval.

## Content authorization

The Client confirms that submitted text, logos, photos, videos, testimonials, reviews, licenses, awards, and business claims are accurate and authorized for marketing use. The Client is responsible for obtaining third-party permissions.

## Additional work

Major redesigns, additional pages, ecommerce, custom applications, complex integrations, recurring content production, backlink campaigns, paid advertising, or work beyond the approved scope requires a separate written scope.

## Limitation and interruption

OneTap will use reasonable care but cannot guarantee uninterrupted third-party hosting, domain, email, form, payment, Google, or internet services. Neither party is liable for indirect or consequential damages to the extent allowed by law.

## Acceptance

Client name: __________________________

Client signature: ______________________   Date: __________

OneTap Creative: ______________________   Date: __________
""",
)

write(
    "client-operations/SCOPE-OF-WORK-TEMPLATE.md",
    """# OneTap Creative Scope of Work — Template

## Client

- Business: [BUSINESS NAME]
- Primary contact: [NAME]
- Public phone: [PHONE]
- Public email: [EMAIL]
- Primary city/service area: [LOCATION]
- Primary website action: [BOOK / CALL / TEXT / QUOTE / CONTACT]

## Included deliverables

- One custom mobile-first website page
- Approximately 8–10 approved sections
- One primary customer action
- Domain registration and connection while active
- Vercel hosting, SSL, backups, and maintenance
- Contact, quote, booking, call, or text integration
- Advanced SEO foundation
- Sitemap, robots, canonical, metadata, structured data, and Search Console setup
- Google Business Profile creation or optimization assistance; client-owned profile
- Two organized revision rounds before launch
- Up to 30 minutes of reasonable monthly updates
- First-review target: 7–10 business days after all required content and access are received

## Approved section order

1. [HERO]
2. [SERVICES]
3. [TRUST / PROOF]
4. [ABOUT]
5. [GALLERY / WORK]
6. [PROCESS]
7. [SERVICE AREA / HOURS]
8. [FAQ]
9. [PRIMARY CTA / FORM]
10. [FOOTER]

## Client-provided items

- Approved logo and brand direction
- Accurate services and prices
- Hours and service area
- Authorized photos and content
- Public contact information
- Google verification participation
- Timely feedback and written approval

## Exclusions

Ecommerce, custom software, large databases, memberships, advanced booking development, unlimited revisions, campaign-level SEO, recurring blog production, backlink campaigns, paid advertising, and additional pages unless specifically listed above.

## Commercial terms

$179 per month. Three-month minimum totaling $537. First payment begins onboarding and the commitment. Then month-to-month with 30 days’ written notice after the minimum.

Client approval: _______________________   Date: __________
""",
)

write(
    "client-operations/GBP-MANAGER-AUTHORIZATION.md",
    """# Google Business Profile Manager Authorization

Business name: ______________________________

Profile owner email: _________________________

The Client confirms that the Google Business Profile belongs to the Client’s business. The Client authorizes OneTap Creative to be added as a **Manager** for setup, optimization, website connection, services, hours, photos, service-area alignment, and ongoing maintenance within the signed scope.

The Client will:

- remain Primary Owner
- provide truthful business information
- complete any identity, phone, email, postcard, or video verification requested by Google
- never send Google passwords or verification codes through the OneTap forms
- notify OneTap of changes to hours, location, services, ownership, or eligibility

OneTap Creative does not guarantee profile approval, reinstatement, Maps placement, ranking, traffic, calls, or leads.

Client authorization: ________________________   Date: __________
""",
)

write(
    "client-operations/DISCOVERY-CALL-SCRIPT.md",
    """# OneTap Creative Discovery Call Script

Target length: 15–20 minutes.

## Opening

“Thank you for taking the time. I want to understand your business, how customers currently find you, and the one action the website should make easiest. I’ll also explain the $179 Complete Online Presence Plan and tell you honestly whether it is a fit.”

## Questions

1. What services produce the best customers or revenue?
2. Which city or realistic service area do you serve?
3. What should a visitor do first: book, call, text, request a quote, visit, or contact you?
4. How do customers find you today?
5. Do you have a client-owned Google Business Profile?
6. What proof can we show: work photos, experience, reviews, licenses, awards, before/after examples?
7. What information do customers ask before contacting you?
8. Do you have current pricing, hours, policies, logo, and original photos?
9. What would make the website successful in the first 90 days?
10. Is there a preferred launch window?

## Fit explanation

“The standard plan is $179 per month with no standard setup fee and a three-month minimum totaling $537. It includes one mobile-first website page, domain and hosting, an advanced SEO foundation, Google Business Profile assistance, two prelaunch revision rounds, 30 minutes of reasonable monthly updates, maintenance, and ongoing support.”

## Close

“If this is a fit, I’ll send the written scope and agreement. After signature, the first $179 payment starts onboarding and the three-month commitment. Then I send the mobile onboarding portal for your business information and photos.”
""",
)

write(
    "client-operations/PROPOSAL-AND-FOLLOW-UP-TEMPLATES.md",
    """# Proposal and Follow-Up Templates

## Qualified proposal email

Subject: Your OneTap Creative website plan for [BUSINESS NAME]

Hi [NAME],

Thank you for sharing what [BUSINESS NAME] needs. Based on our conversation, the website should focus on [PRIMARY ACTION] and clearly present [TOP SERVICES] for customers in [SERVICE AREA].

The recommended Complete Online Presence Plan is $179 per month with no standard setup fee and a three-month minimum totaling $537. The attached scope covers the website, domain, hosting, advanced SEO foundation, Google Business Profile assistance, two prelaunch revision rounds, 30 minutes of reasonable monthly updates, maintenance, and support.

Next steps:
1. Review and sign the agreement and scope.
2. Complete the first $179 payment.
3. Complete the mobile onboarding portal.

I’m available for questions before you approve anything.

OneTap Creative

## Follow-up after two business days

Subject: Any questions about the [BUSINESS NAME] website plan?

Hi [NAME],

I wanted to make sure the scope and next steps were clear. The most important goal we discussed was [PRIMARY GOAL]. I can clarify the website scope, timeline, Google setup, or monthly plan before you decide.

## Final follow-up after seven days

Subject: Closing the loop on [BUSINESS NAME]

Hi [NAME],

I’m closing the loop on the website plan for now. I still believe the project is a good fit if [PRIMARY GOAL] remains a priority. Reply when the timing is right and I’ll confirm availability and whether the original scope still applies.
""",
)

write(
    "client-operations/MONTHLY-CARE-SUMMARY-TEMPLATE.md",
    """# OneTap Creative Monthly Client Care Summary

Client: [BUSINESS NAME]
Month: [MONTH YEAR]

## Website health

- Production homepage: [PASS / ACTION]
- HTTPS and domain: [PASS / ACTION]
- Contact/booking/quote action: [PASS / ACTION]
- Mobile navigation and forms: [PASS / ACTION]
- Broken links or missing assets: [PASS / ACTION]
- Backup/hosting status: [PASS / ACTION]

## Search foundation

- Search Console coverage: [SUMMARY]
- Clicks and impressions: [SUMMARY]
- Top search queries: [SUMMARY]
- Sitemap and indexing: [SUMMARY]
- Core Web Vitals: [SUMMARY]
- Google Business Profile status: [SUMMARY]

## Updates completed

- [UPDATE]
- [UPDATE]

Monthly update time used: [MINUTES] of 30 minutes

## Recommended next action

[ONE CLEAR RECOMMENDATION]
""",
)

write(
    "client-operations/LEAD-TRACKER.csv",
    "Date Added,Business,Contact Name,Email,Phone,Industry,City,Lead Source,Website/GBP Status,Primary Goal,First Contact Date,Follow-Up Date,Discovery Call,Proposal Sent,Agreement Signed,First Payment,Onboarding Complete,Status,Monthly Value,Notes\n",
)

write(
    "launch/HARD-LAUNCH-RUNBOOK.md",
    f"""# OneTap Creative Hard-Launch Runbook

## Website release completed in code

- Approved $179/month offer and $537 initial commitment
- Advanced SEO foundation language
- Two revision rounds and 30-minute monthly update allowance
- Static canonical and social metadata
- DJ JRV and Freda live proof
- Founder-led trust section
- One-business-day response expectation
- Consistent public Terms, Privacy, thank-you page, and onboarding plan
- Unified verified internal form delivery to `{FORM_EMAIL}`
- Automatic client confirmation emails and Reply-To routing
- Unsupported demo rating claims removed
- UTM capture and analytics-ready `generate_lead` events
- Public launch regression audit

## Required client workflow

Lead request → reply within one business day → discovery call → personalized scope → signed agreement → first $179 payment → onboarding → content review → build → two revision rounds → approval → launch → monthly care.

## External account actions before paid advertising

1. Activate `{PUBLIC_EMAIL}` and test sending and receiving.
2. Create the Square recurring $179 payment link or recurring invoice workflow.
3. Enable Vercel Web Analytics or connect GA4 and verify `generate_lead` reporting.
4. Verify the OneTap Search Console domain property and submit the sitemap.
5. Determine whether OneTap qualifies for a Google Business Profile before creating one.
6. Run the mock-client test in this folder.

The website can accept controlled organic and referral leads using the verified internal form inbox before the professional-mailbox cutover. Do not run broad paid advertising until the external actions above pass end to end.
""",
)

write(
    "launch/SQUARE-PAYMENT-SETUP.md",
    """# Square Recurring Payment Setup

Use Square Dashboard. The signed agreement—not the payment link alone—defines the three-month minimum.

1. Create an item named **OneTap Creative Complete Online Presence Plan**.
2. Set the price to **$179**.
3. Create a monthly subscription plan or a payment link with recurring monthly frequency.
4. Description: “Managed mobile-first website, domain and hosting, advanced SEO foundation, Google Business Profile assistance, maintenance, and support. Three-month minimum under signed agreement.”
5. Disable optional tipping.
6. Collect the client’s name, business name, and email.
7. Set the post-checkout redirect to the personalized onboarding URL, or manually send the onboarding URL after payment is confirmed.
8. Confirm the billing date and automatic receipt.
9. Test the link before sending it to a client.
10. Record the payment date because it begins onboarding and the three-month commitment.

Never place the payment link on the public homepage. Send it only after the scope and agreement are approved.
""",
)

write(
    "launch/PROFESSIONAL-EMAIL-CUTOVER.md",
    f"""# Professional Email Cutover

Planned mailbox: `{PUBLIC_EMAIL}`
Current verified internal form inbox: `{FORM_EMAIL}`

## Activate

1. Create and verify the mailbox with the chosen provider.
2. Configure required DNS records at the domain registrar.
3. Add SPF, DKIM, and DMARC according to the provider’s current instructions.
4. Send test messages to Gmail and Outlook.
5. Reply from `{PUBLIC_EMAIL}` and confirm delivery does not go to spam.

## Cut over the website

After the mailbox passes testing:

- replace the public lead form action with `https://formsubmit.co/{PUBLIC_EMAIL}`
- replace the onboarding form action with the same address or an approved project mailbox
- complete FormSubmit activation for each route
- submit one public lead test and one attachment onboarding test
- update `launch-config.json`
- keep the public footer form-based unless a visible email is intentionally approved

Do not change the forms to an unverified mailbox before testing.
""",
)

write(
    "launch/ANALYTICS-ACTIVATION.md",
    """# Analytics Activation

The website already records UTM source, medium, campaign, content, landing page, CTA clicks, portfolio clicks, form submit attempts, and the recommended `generate_lead` event. A production analytics collector still requires account activation.

## Vercel Web Analytics path

1. Open the OneTap Creative project in Vercel.
2. Enable Web Analytics.
3. Follow the current Vercel static-site integration instructions.
4. Redeploy and promote the deployment to production.
5. Confirm a production page view appears.

## GA4 path

1. Create or select the OneTap Creative GA4 property and web data stream.
2. Add the production Measurement ID through the approved tag implementation.
3. Verify page views and `generate_lead` in DebugView/Realtime.
4. Mark the completed lead event as a key event after validation.
5. Exclude internal testing traffic where practical.

## Launch dashboard minimum

Track sessions, source/medium, landing page, CTA clicks, portfolio clicks, completed leads, lead-to-call rate, proposal rate, signed-client rate, and cancellations.
""",
)

write(
    "launch/MOCK-CLIENT-TEST.md",
    """# Mock Client End-to-End Test

Use a fictional business and a separate test email.

- [ ] Submit the public lead form from a phone
- [ ] Confirm OneTap receives the request
- [ ] Confirm the prospect receives the automatic response
- [ ] Confirm Reply-To opens the prospect’s address
- [ ] Record UTM and lead-source fields
- [ ] Conduct the discovery call using the script
- [ ] Personalize and send agreement and scope
- [ ] Complete a test Square payment workflow
- [ ] Send the personalized onboarding URL
- [ ] Complete all onboarding steps on a phone
- [ ] Upload small test images and a PDF
- [ ] Confirm onboarding email and attachments arrive
- [ ] Confirm the onboarding success page loads
- [ ] Confirm local saved answers clear after success
- [ ] Create the project folder and production checklist
- [ ] Run the SEO generator and 90+/zero-critical audit
- [ ] Test mobile, desktop, form delivery, links, canonical, sitemap, robots, and 404
- [ ] Record client approval and launch
- [ ] Complete the first monthly care summary

Do not begin broad paid promotion until every item passes.
""",
)

print("Hard-launch completion files generated.")
