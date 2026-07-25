from pathlib import Path
import json
import re

root = Path(__file__).resolve().parents[1]


def read(name):
    return (root / name).read_text(encoding="utf-8")


def write(name, text):
    (root / name).write_text(text, encoding="utf-8")


def replace_once(text, old, new, label):
    if old not in text:
        raise RuntimeError(f"Missing anchor: {label}")
    return text.replace(old, new, 1)


index = read("index.html")

# Global approved pricing changes.
index = index.replace("$149 per month", "$179 per month")
index = index.replace("$149/month", "$179/month")
index = index.replace("$149 a month", "$179 a month")
index = index.replace("$149", "$179")
index = index.replace("$447", "$537")

# Update structured-data numeric prices safely.
index = index.replace('"price":"149"', '"price":"179"')

# Clarify the approved standard scope in the pricing card.
old_pricing_list = '<ul><li>Custom mobile-friendly website</li><li>Domain registration, hosting, SSL, and backups</li><li>Google Business Profile setup or optimization</li><li>Advanced SEO foundation, Google indexing, and Search Console setup</li><li>Booking, contact, or quote-request form</li><li>Reasonable website updates and ongoing support</li><li>Month-to-month after the minimum; 30 days’ notice to cancel</li></ul>'
new_pricing_list = '<ul><li>Custom one-page mobile-friendly website with up to approximately 8–10 sections</li><li>One primary booking, contact, call, text, or quote-request action</li><li>Domain registration, hosting, SSL, and backups while active</li><li>Google Business Profile setup or optimization assistance</li><li>Advanced SEO foundation, Google indexing, and Search Console setup</li><li>Two organized revision rounds before launch</li><li>Up to 30 minutes of reasonable website updates each month</li><li>Technical maintenance and founder-led support</li><li>Month-to-month after the minimum; 30 days’ notice to cancel</li></ul>'
index = replace_once(index, old_pricing_list, new_pricing_list, "pricing list")

# Make the initial-payment rule visible near pricing.
old_small = '<small>No payment is collected here. Final scope and cancellation terms are confirmed in the client agreement.</small>'
new_small = '<small>No payment is collected here. The first monthly payment is collected before onboarding and starts the three-month commitment. Final scope and cancellation terms are confirmed in the client agreement.</small>'
index = replace_once(index, old_small, new_small, "pricing payment note")

# Update the pricing FAQ answers and add the finalized scope FAQ.
old_updates = '<details class="reveal"><summary>What counts as a reasonable website update?<span>+</span></summary><p>Examples include replacing photos, updating hours, editing existing text, adjusting services or pricing, and adding a promotion within the current layout. Major redesigns, new pages, custom software, ecommerce, or advanced integrations require a separate quote.</p></details>'
new_updates = '<details class="reveal"><summary>What counts as a reasonable website update?<span>+</span></summary><p>The plan includes up to 30 minutes of reasonable website updates per month. Examples include replacing a few photos, updating hours, editing existing text, adjusting services or pricing, and adding a promotion within the current layout. Unused time does not roll over. Major redesigns, new pages, custom software, ecommerce, or advanced integrations require a separate written scope.</p></details><details class="reveal"><summary>What website size and revisions are included?<span>+</span></summary><p>The standard plan includes one custom mobile-first page with up to approximately 8–10 sections, one primary customer action, and two organized revision rounds before launch. A revision round means one complete list of requested changes submitted together.</p></details>'
index = replace_once(index, old_updates, new_updates, "monthly updates FAQ")

# Refine timeline to approved target.
index = index.replace("Most projects can reach a first review in about one to two weeks after all required content is received.", "Most projects can reach a first review within approximately 7–10 business days after all required content and access are received.")

# Add first-payment protection to the onboarding path.
index = index.replace("After approval, the first payment and complete content intake open the production phase.", "After approval, the first monthly payment starts the three-month commitment, and the complete content intake opens the production phase.")

# Add visible scope protection to start points.
old_points = '<ul class="start-points"><li>No payment collected today</li><li>Typical reply within one business day</li><li>One clear plan with no separate standard setup fee</li><li>Personal onboarding and written scope</li></ul>'
new_points = '<ul class="start-points"><li>No payment collected today</li><li>Typical reply within one business day</li><li>First payment begins onboarding and the three-month commitment</li><li>Two prelaunch revision rounds and 30 minutes of monthly updates</li><li>Personal onboarding and written scope</li></ul>'
index = replace_once(index, old_points, new_points, "start points")

# Rebuild structured data so visible FAQ and schema remain aligned.
schema_match = re.search(r'<script id="business-schema" type="application/ld\+json">(.*?)</script>', index)
if not schema_match:
    raise RuntimeError("Business schema not found")
schema = json.loads(schema_match.group(1))
for node in schema.get("@graph", []):
    if node.get("@type") == "ProfessionalService":
        node["priceRange"] = "$179 per month"
        offers = node.get("hasOfferCatalog", {}).get("itemListElement", [])
        for offer in offers:
            offer["price"] = "179"
    if node.get("@type") == "Service":
        offer = node.get("offers", {})
        offer["price"] = "179"
        offer["description"] = "$179 per month with no standard setup fee and a three-month minimum totaling $537, then month-to-month with 30 days’ notice after the minimum."
    if node.get("@type") == "FAQPage":
        entities = node.get("mainEntity", [])
        for item in entities:
            q = item.get("name", "")
            answer = item.get("acceptedAnswer", {})
            text = answer.get("text", "")
            text = text.replace("$149", "$179").replace("$447", "$537")
            if q == "What counts as a reasonable website update?":
                text = "The plan includes up to 30 minutes of reasonable website updates per month. Examples include replacing a few photos, updating hours, editing existing text, adjusting services or pricing, and adding a promotion within the current layout. Unused time does not roll over. Major redesigns, new pages, custom software, ecommerce, or advanced integrations require a separate written scope."
            if q == "How long does launch take?":
                text = "Most projects can reach a first review within approximately 7–10 business days after all required content and access are received. Final launch depends on approvals, domain access, integrations, and any Google verification steps."
            answer["text"] = text
        entities.append({
            "@type": "Question",
            "name": "What website size and revisions are included?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "The standard plan includes one custom mobile-first page with up to approximately 8–10 sections, one primary customer action, and two organized revision rounds before launch. A revision round means one complete list of requested changes submitted together."
            }
        })
new_schema = json.dumps(schema, ensure_ascii=False, separators=(",", ":"))
index = index[:schema_match.start(1)] + new_schema + index[schema_match.end(1):]

# Cache-bust public assets after pricing update.
index = index.replace('styles.css?v=launch-100', 'styles.css?v=pricing-179')
index = index.replace('script.js?v=launch-100', 'script.js?v=pricing-179')
write("index.html", index)

terms = read("terms.html")
terms = terms.replace("$149", "$179").replace("$447", "$537")
terms = terms.replace('styles.css?v=launch-100', 'styles.css?v=pricing-179')
terms = replace_once(
    terms,
    '<h2 style="font-size:1.8rem">Complete Online Presence Plan</h2><p>OneTap Creative offers a standard Complete Online Presence Plan for $179 per month. The standard service may include a custom mobile-first one-page website, domain registration and renewal, hosting, SSL, basic backups, booking/contact/quote integration, an advanced SEO foundation, Google Search Console setup, Google Business Profile setup or optimization assistance, reasonable updates, maintenance, and ongoing technical support, subject to the signed client agreement.</p>',
    '<h2 style="font-size:1.8rem">Complete Online Presence Plan</h2><p>OneTap Creative offers a standard Complete Online Presence Plan for $179 per month with no separate standard setup fee. The included scope is generally one custom mobile-first page with up to approximately 8–10 sections, one primary customer action, standard domain registration and renewal while active, hosting, SSL, basic backups, one booking/contact/call/text/quote integration, an advanced SEO foundation, Google Search Console setup, Google Business Profile setup or optimization assistance, two organized prelaunch revision rounds, up to 30 minutes of reasonable monthly updates, maintenance, and ongoing technical support, subject to the signed client agreement.</p>',
    "terms plan scope"
)
terms = replace_once(
    terms,
    '<h2 style="font-size:1.8rem">Subscription, minimum term, and cancellation</h2><p>The service is $179 per month with an initial three-month minimum commitment, totaling $537 for the first three months. No separate setup fee applies to the standard included scope. After the minimum term, service continues month-to-month. Cancellation after the minimum requires at least 30 days’ written notice unless the signed client agreement states otherwise.</p>',
    '<h2 style="font-size:1.8rem">Subscription, minimum term, and cancellation</h2><p>The service is $179 per month with an initial three-month minimum commitment, totaling $537 for the first three months. The first monthly payment is collected before onboarding begins and starts the three-month commitment, even if launch is delayed by missing content, access, feedback, approval, or third-party verification. After the minimum term, service continues month-to-month. Cancellation after the minimum requires at least 30 days’ written notice unless the signed client agreement states otherwise. Payments already earned or covering an active billing period are not partially refunded.</p>',
    "terms commitment"
)
terms = replace_once(
    terms,
    '<h2 style="font-size:1.8rem">Domain, hosting, and website management</h2><p>OneTap Creative manages the website files, hosting, SSL, backups, and the agreed business domain while the subscription is active. Domain registration and renewal are included during the active subscription. Transfer, buyout, cancellation, ownership, and early-termination terms are governed by the signed client agreement.</p>',
    '<h2 style="font-size:1.8rem">Domain, hosting, and website management</h2><p>The business domain should be registered to the client whenever practical, while OneTap Creative receives the access needed to manage DNS and website connections. Standard domain registration or renewal is included while the subscription remains active, subject to normal registration cost and availability. OneTap Creative manages the website files, hosting, SSL, backups, and technical system during the active service. Website-file transfer, hosting transfer, buyout, cancellation, and offboarding terms are governed by the signed client agreement.</p>',
    "terms domain ownership"
)
terms = replace_once(
    terms,
    '<h2 style="font-size:1.8rem">Reasonable updates and additional work</h2><p>Reasonable updates may include replacing photos, editing existing text, changing hours, services, pricing, contact details, or promotions within the approved layout. Major redesigns, additional pages, ecommerce, custom software, recurring content creation, new brand development, advanced integrations, or campaign-level SEO may require a separate quote.</p>',
    '<h2 style="font-size:1.8rem">Revisions, reasonable updates, and additional work</h2><p>The standard build includes two organized revision rounds before launch. Each revision round must be submitted as one complete list of requested changes. After launch, the plan includes up to 30 minutes of reasonable website updates per month, such as replacing a few photos, editing existing text, changing hours, services, pricing, contact details, or promotions within the approved layout. Unused update time does not roll over. Major redesigns, additional pages, ecommerce, custom software, recurring content creation, new brand development, advanced integrations, or campaign-level SEO require a separate written scope.</p>',
    "terms updates"
)
terms = terms.replace(
    '<h2 style="font-size:1.8rem">Response and timeline expectations</h2><p>OneTap aims to respond to new project requests within one business day and provide a first website review within the estimated project window after all required content and access are received.',
    '<h2 style="font-size:1.8rem">Response and timeline expectations</h2><p>OneTap aims to respond to new project requests within one business day and provide a first website review within approximately 7–10 business days after all required content and access are received.'
)
insert_anchor = '<h2 style="font-size:1.8rem">No guaranteed results</h2>'
late_payment = '<h2 style="font-size:1.8rem">Billing, failed payments, and suspension</h2><p>Monthly payments are intended to process automatically on the agreed billing date. A failed payment may receive a seven-day grace period. OneTap Creative may suspend the website, hosting, support, or related services after 14 days of nonpayment following reasonable written notice. Service may resume after outstanding balances are paid. Repeated or extended nonpayment may result in cancellation under the signed client agreement.</p><h2 style="font-size:1.8rem">Price protection</h2><p>The agreed monthly price is intended to remain unchanged for the client’s first 12 months of continuous service. After that period, OneTap Creative may adjust future pricing with advance written notice, subject to the signed client agreement.</p>'
terms = replace_once(terms, insert_anchor, late_payment + insert_anchor, "billing and rate protection")
write("terms.html", terms)

thank = read("thank-you.html")
thank = thank.replace('styles.css?v=launch-100', 'styles.css?v=pricing-179')
thank = thank.replace("After approval, the first payment and full content intake begin the production process.", "After approval, the first $179 monthly payment starts the three-month commitment, and the full content intake begins the production process.")
write("thank-you.html", thank)

print("Applied final $179 pricing and scope rules")
