from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SITE_URL = "https://onetapcreative.com"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, content: str) -> None:
    (ROOT / path).write_text(content, encoding="utf-8")


def must_replace(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"Missing replacement anchor: {label}")
    return text.replace(old, new, 1)


faq_items = [
    (
        "What does the advanced SEO foundation include?",
        "Every standard launch includes local keyword mapping, search-focused headings and page structure, title and description optimization, technical SEO, mobile and performance optimization, image optimization, canonical setup, structured data when appropriate, sitemap and indexing setup, Google Search Console, and local business information alignment. Ongoing blog writing, backlink campaigns, paid advertising, ecommerce SEO, multi-location campaigns, and guaranteed rankings are not included in the standard $149 plan and may require a separate proposal.",
    ),
    (
        "What is included in the $149 monthly plan?",
        "A custom mobile-first website, domain registration and renewal while active, hosting, SSL, basic backups, booking/contact/quote integration, Google Business Profile setup or optimization, an advanced SEO foundation, Google indexing, Search Console setup, reasonable content updates, maintenance, and ongoing support. Advanced functions, ecommerce, recurring content campaigns, backlink work, or additional pages may require a separate quote.",
    ),
    (
        "How does the three-month commitment work?",
        "The initial commitment is three monthly payments of $149, totaling $447. After the minimum term, the service continues month-to-month. Cancellation after the minimum requires 30 days’ notice according to the signed client agreement.",
    ),
    (
        "Can you guarantee I will rank first on Google?",
        "No ethical web or SEO provider can guarantee a specific ranking. We build a strong search foundation, connect the website and profile correctly, and help Google understand the business. Google controls verification, indexing, Maps placement, and search rankings.",
    ),
    (
        "Do you create the Google Business Profile?",
        "We can help create or optimize the client-owned profile, connect the website, add accurate categories, services, hours, photos, and guide verification. The client must provide truthful information and complete any identity or video verification requested by Google.",
    ),
    (
        "What counts as a reasonable website update?",
        "Examples include replacing photos, updating hours, editing existing text, adjusting services or pricing, and adding a promotion within the current layout. Major redesigns, new pages, custom software, ecommerce, or advanced integrations require a separate quote.",
    ),
    (
        "How long does launch take?",
        "Most projects can reach a first review in about one to two weeks after all required content is received. Final launch depends on approvals, domain access, integrations, and any Google verification steps.",
    ),
    (
        "Who is OneTap Creative best for?",
        "The standard plan is built for local service businesses that need a professional one-page website and one clear customer action, such as booking an appointment, requesting a quote, calling the business, or submitting a contact request.",
    ),
    (
        "What happens after I submit the request form?",
        "OneTap Creative reviews the business, goals, current online presence, and Google Business Profile status. A reply is normally sent within one business day. If the project is a fit, the next steps are a written scope, client agreement, first payment, and onboarding form.",
    ),
    (
        "Who manages the website and domain?",
        "OneTap Creative manages the website files, hosting, security, backups, and the agreed domain while the subscription is active. Ownership, transfer, buyout, cancellation, and offboarding terms are documented in the signed client agreement before work begins.",
    ),
]

business_schema = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "ProfessionalService",
            "@id": f"{SITE_URL}/#business",
            "name": "OneTap Creative",
            "url": f"{SITE_URL}/",
            "logo": f"{SITE_URL}/assets/images/onetap-logo-full-natural.png",
            "image": f"{SITE_URL}/assets/images/onetap-og-direction.jpg",
            "description": "OneTap Creative builds and manages complete online presences for local service businesses, including mobile-first websites, domain and hosting, Google Business Profile setup, an advanced SEO foundation, Search Console, updates, and ongoing support.",
            "priceRange": "$149 per month",
            "areaServed": [
                {"@type": "City", "name": "Stockton"},
                {"@type": "AdministrativeArea", "name": "San Joaquin County"},
                {"@type": "State", "name": "California"},
                {"@type": "Country", "name": "United States"},
            ],
            "knowsAbout": [
                "Mobile-first website design",
                "Local business websites",
                "Google Business Profile setup",
                "Advanced on-page SEO",
                "Technical SEO foundations",
                "Local SEO",
                "Google Search Console",
                "Booking websites",
                "Quote request websites",
            ],
            "hasOfferCatalog": {
                "@type": "OfferCatalog",
                "name": "OneTap Creative Services",
                "itemListElement": [
                    {
                        "@type": "Offer",
                        "price": "149",
                        "priceCurrency": "USD",
                        "url": f"{SITE_URL}/#pricing",
                        "category": "Website design and online presence management",
                        "itemOffered": {"@id": f"{SITE_URL}/#complete-online-presence"},
                    }
                ],
            },
        },
        {
            "@type": "WebSite",
            "@id": f"{SITE_URL}/#website",
            "url": f"{SITE_URL}/",
            "name": "OneTap Creative",
            "description": "Professional websites, Google visibility, and ongoing support for local service businesses.",
            "publisher": {"@id": f"{SITE_URL}/#business"},
            "inLanguage": "en-US",
        },
        {
            "@type": "Service",
            "@id": f"{SITE_URL}/#complete-online-presence",
            "name": "Complete Online Presence Plan",
            "serviceType": "Website design, local SEO foundation, Google Business Profile setup, hosting, and ongoing website care",
            "description": "A managed mobile-first website and Google visibility foundation for local service businesses, including domain, hosting, SSL, forms, advanced SEO foundation, Search Console, reasonable updates, maintenance, and support.",
            "provider": {"@id": f"{SITE_URL}/#business"},
            "areaServed": {"@type": "Country", "name": "United States"},
            "offers": {
                "@type": "Offer",
                "price": "149",
                "priceCurrency": "USD",
                "url": f"{SITE_URL}/#pricing",
                "description": "$149 per month with a three-month minimum, then month-to-month with 30 days’ notice after the minimum.",
            },
        },
        {
            "@type": "FAQPage",
            "@id": f"{SITE_URL}/#faq-schema",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": question,
                    "acceptedAnswer": {"@type": "Answer", "text": answer},
                }
                for question, answer in faq_items
            ],
        },
    ],
}

index = read("index.html")

head = f'''<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="description" content="OneTap Creative builds and manages complete online presences for local service businesses with a mobile-first website, advanced SEO foundation, Google Business Profile setup, domain, hosting, and ongoing support for $149 per month."/>
<meta name="keywords" content="OneTap Creative, local business website design, Stockton web designer, small business website, Google Business Profile setup, local SEO, mobile-first website, website maintenance"/>
<meta name="theme-color" content="#080808"/>
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"/>
<meta name="author" content="OneTap Creative"/>
<meta name="publisher" content="OneTap Creative"/>
<meta name="geo.region" content="US-CA"/>
<meta name="geo.placename" content="Stockton"/>
<meta name="format-detection" content="telephone=no"/>
<meta property="og:title" content="OneTap Creative | Websites, Advanced SEO &amp; Google Visibility"/>
<meta property="og:description" content="A complete online presence for local businesses: professional website, advanced SEO foundation, Google Business Profile setup, domain, hosting, and ongoing support."/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="OneTap Creative"/>
<meta property="og:locale" content="en_US"/>
<meta property="og:image" content="{SITE_URL}/assets/images/onetap-og-direction.jpg"/>
<meta property="og:image:alt" content="OneTap Creative complete online presence service for local businesses"/>
<meta property="og:url" content="{SITE_URL}/"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="OneTap Creative | Websites, Advanced SEO &amp; Google Visibility"/>
<meta name="twitter:description" content="Professional websites, Google visibility, and ongoing support for local service businesses."/>
<meta name="twitter:image" content="{SITE_URL}/assets/images/onetap-og-direction.jpg"/>
<link rel="canonical" href="{SITE_URL}/"/>
<link rel="icon" href="assets/images/onetap-icon-natural.png" type="image/png"/>
<link rel="apple-touch-icon" href="assets/images/onetap-icon-natural.png"/>
<link rel="manifest" href="manifest.webmanifest"/>
<link rel="stylesheet" href="styles.css?v=launch-100"/>
<title>OneTap Creative | Websites, Advanced SEO &amp; Google Visibility</title>
<script id="business-schema" type="application/ld+json">{json.dumps(business_schema, ensure_ascii=False, separators=(",", ":"))}</script>
</head>'''
index, count = re.subn(r"<head>.*?</head>", head, index, count=1, flags=re.S)
if count != 1:
    raise RuntimeError("Unable to replace index head")

new_nav = '''<nav class="main-nav" id="main-nav" aria-label="Main navigation">
      <a href="#services">What’s Included</a><a href="#work">Real Work</a><a href="#why">Why OneTap</a><a href="#process">Process</a><a href="#pricing">Pricing</a><a href="#faq">FAQ</a><a class="btn btn-small" href="#start">Get Started</a>
    </nav>'''
index, count = re.subn(r'<nav class="main-nav" id="main-nav" aria-label="Main navigation">.*?</nav>', new_nav, index, count=1, flags=re.S)
if count != 1:
    raise RuntimeError("Unable to replace navigation")

hero_price = '<div class="hero-price"><div><strong>$149</strong><span>/month</span></div><p><b>3-month minimum</b><br/>Then month-to-month · 30 days’ notice after minimum</p></div>'
hero_assurance = hero_price + '<div class="hero-assurance" aria-label="OneTap Creative service assurances"><span>No setup fee</span><span>Founder-led support</span><span>Reply within one business day</span></div>'
index = must_replace(index, hero_price, hero_assurance, "hero assurance")

real_work = '''<div class="real-work-grid">
<article aria-labelledby="dj-case-title" class="case-study reveal">
  <div class="case-study-copy">
    <p class="eyebrow"><span></span> Launched client website</p>
    <div class="verified-work">Live custom-domain project</div>
    <h3 id="dj-case-title">DJ JRV / Romero Vision</h3>
    <p>A mobile-first DJ website built to explain services, establish trust, and turn event visitors into personalized quote requests.</p>
    <ul><li>Custom domain and secure Vercel hosting</li><li>Phone and quote-request conversion paths</li><li>Advanced local SEO foundation</li><li>Business schema, sitemap, and crawler setup</li><li>Ongoing website maintenance</li></ul>
    <a class="btn" href="https://www.dj-jrv.com/" rel="noopener" target="_blank">View DJ JRV Live <span aria-hidden="true">↗</span></a>
  </div>
  <div class="case-study-live" aria-label="Live preview of the DJ JRV website">
    <div class="live-site-bar"><i></i><i></i><i></i><span>dj-jrv.com</span></div>
    <div class="live-site-viewport"><iframe class="live-site-frame" data-src="https://www.dj-jrv.com/" loading="lazy" tabindex="-1" title="Live preview of the DJ JRV client website"></iframe></div>
    <a href="https://www.dj-jrv.com/" rel="noopener" target="_blank">Open the live website ↗</a>
  </div>
</article>
<article aria-labelledby="freda-case-title" class="case-study reveal">
  <div class="case-study-copy">
    <p class="eyebrow"><span></span> Live barber project</p>
    <div class="verified-work">Real business website build</div>
    <h3 id="freda-case-title">Freda the Barber</h3>
    <p>A modern Manteca barber website that makes services, pricing, work samples, location details, and appointment requests easy to find on mobile.</p>
    <ul><li>Service pricing and weekly hours</li><li>Portfolio gallery and location details</li><li>Appointment-by-text workflow</li><li>Advanced Manteca-focused SEO foundation</li><li>Accessible mobile navigation and forms</li></ul>
    <a class="btn" href="https://freda-modern-barber-website.vercel.app/" rel="noopener" target="_blank">View Freda’s Website <span aria-hidden="true">↗</span></a>
  </div>
  <div class="case-study-live" aria-label="Live preview of Freda the Barber website">
    <div class="live-site-bar"><i></i><i></i><i></i><span>Freda the Barber</span></div>
    <div class="live-site-viewport"><iframe class="live-site-frame" data-src="https://freda-modern-barber-website.vercel.app/" loading="lazy" tabindex="-1" title="Live preview of Freda the Barber website"></iframe></div>
    <a href="https://freda-modern-barber-website.vercel.app/" rel="noopener" target="_blank">Open the live website ↗</a>
  </div>
</article>
</div>'''
index, count = re.subn(r'<article aria-labelledby="dj-case-title" class="case-study reveal">.*?</article>', real_work, index, count=1, flags=re.S)
if count != 1:
    raise RuntimeError("Unable to replace DJ case study")

why_section = '''
<section class="section-pad why-section" id="why">
  <div class="container why-grid">
    <div class="why-story reveal">
      <p class="eyebrow"><span></span> Why OneTap Creative</p>
      <h2>A founder-led partner for your <em>complete online presence.</em></h2>
      <p class="why-lead">OneTap Creative was built around a simple idea: local business owners should not have to coordinate a designer, hosting company, SEO provider, and Google setup on their own.</p>
      <p>You work directly with OneTap Creative from the first request through launch and monthly care. Every decision is focused on making the business easier to find, easier to trust, and easier to contact.</p>
      <div class="founder-note"><img src="assets/images/onetap-icon-natural.png" alt=""/><div><span>Founder-led agency</span><strong>Direct communication. Hands-on support.</strong><p>No call-center handoffs and no disappearing after launch.</p></div></div>
    </div>
    <div class="why-card-grid">
      <article class="why-card reveal"><b>01</b><h3>One clear plan</h3><p>The website, domain, hosting, Google setup, SEO foundation, maintenance, and support are managed together.</p></article>
      <article class="why-card reveal"><b>02</b><h3>Built for action</h3><p>Every site is designed around one primary customer action: book, call, request a quote, or submit an inquiry.</p></article>
      <article class="why-card reveal"><b>03</b><h3>Google-ready foundation</h3><p>Search structure, metadata, schema, sitemap, indexing, Search Console, and Business Profile alignment are included.</p></article>
      <article class="why-card reveal"><b>04</b><h3>Supported after launch</h3><p>Reasonable updates, hosting, backups, security, and technical help continue while the plan stays active.</p></article>
    </div>
  </div>
</section>
'''
index = must_replace(index, '<section class="section-pad process-section direction-process" id="process">', why_section + '<section class="section-pad process-section direction-process" id="process">', "why section")

new_process = '''<section class="section-pad process-section direction-process" id="process"><div class="container"><div class="section-heading reveal"><p class="eyebrow"><span></span> From request to ongoing care</p><h2>A clear path from first conversation to <em>public launch.</em></h2><p>You always know what happens next, what OneTap needs from you, and what is being handled behind the scenes.</p></div><ol class="process-cards four-step"><li class="reveal"><span>01</span><div class="step-icon">DISCOVER</div><h3>Tell us about the business</h3><p>Submit the request form with your services, goals, current online presence, and preferred customer action.</p></li><li class="reveal"><span>02</span><div class="step-icon">PLAN</div><h3>We confirm the scope</h3><p>We review fit, explain the plan, confirm content and access needs, and provide the written agreement.</p></li><li class="reveal"><span>03</span><div class="step-icon">BUILD</div><h3>We build and launch</h3><p>We design the site, connect the domain and forms, implement SEO and Google setup, test, review, and publish.</p></li><li class="reveal"><span>04</span><div class="step-icon">CARE</div><h3>We maintain the presence</h3><p>We handle reasonable updates, technical maintenance, backups, support, and ongoing search-health checks.</p></li></ol></div></section>'''
index, count = re.subn(r'<section class="section-pad process-section direction-process" id="process">.*?</section>', new_process, index, count=1, flags=re.S)
if count != 1:
    raise RuntimeError("Unable to replace process")

response_section = '''
<section class="response-section" aria-labelledby="response-title">
  <div class="container response-shell reveal">
    <div class="response-heading"><p class="eyebrow"><span></span> What happens after you submit</p><h2 id="response-title">A real response—not an automated sales maze.</h2><p>Submitting the form starts a fit review. It does not charge you or lock you into the service.</p></div>
    <div class="response-grid"><div><b>01</b><strong>Request received</strong><span>Your business details and goals arrive in one organized request.</span></div><div><b>02</b><strong>Reply within one business day</strong><span>OneTap follows up with questions, fit feedback, or the recommended next step.</span></div><div><b>03</b><strong>Written scope and agreement</strong><span>Pricing, responsibilities, timeline, ownership, and cancellation terms are confirmed before work starts.</span></div><div><b>04</b><strong>Payment and onboarding</strong><span>After approval, the first payment and complete content intake open the production phase.</span></div></div>
  </div>
</section>
'''
index = must_replace(index, '<section class="section-pad start-section" id="start">', response_section + '<section class="section-pad start-section" id="start">', "response expectations")

old_points = '<ul class="start-points"><li>No payment collected today</li><li>One clear plan with no separate standard setup fee</li><li>Personal onboarding and written scope</li></ul>'
new_points = '<ul class="start-points"><li>No payment collected today</li><li>Typical reply within one business day</li><li>One clear plan with no separate standard setup fee</li><li>Personal onboarding and written scope</li></ul>'
index = must_replace(index, old_points, new_points, "start points")

honey = '<input aria-hidden="true" autocomplete="off" class="form-honeypot" name="_honey" tabindex="-1" type="text"/>'
hidden_tracking = '<input id="utm-source" name="UTM Source" type="hidden"/><input id="utm-medium" name="UTM Medium" type="hidden"/><input id="utm-campaign" name="UTM Campaign" type="hidden"/><input id="utm-content" name="UTM Content" type="hidden"/><input id="landing-page" name="Landing Page" type="hidden"/>' + honey
index = must_replace(index, honey, hidden_tracking, "tracking fields")

index = index.replace('<option>Landscaper / Lawn Care</option><option>Other service that needs quotes</option>', '<option>Landscaper / Lawn Care</option><option>DJ / Event Service</option><option>Cleaning Service</option><option>Contractor / Home Service</option><option>Restaurant / Food Service</option><option>Other service that needs bookings or quotes</option>', 1)

social_field = '<label>Current website or social profile<input name="Current Website or Social" placeholder="Website link, Instagram handle, Facebook page, or none" type="text"/></label>'
qualification_fields = social_field + '<div class="form-two"><label>Preferred launch timing<select name="Preferred Launch Timing"><option selected>Not sure yet</option><option>As soon as possible</option><option>Within 2–4 weeks</option><option>Within 1–2 months</option><option>More than 2 months away</option></select></label><label>How did you hear about OneTap?<select id="lead-source" name="Lead Source"><option selected>Select one</option><option>Referral</option><option>Google Search</option><option>Facebook or Instagram</option><option>Saw a OneTap client website</option><option>Direct outreach from OneTap</option><option>Other</option></select></label></div>'
index = must_replace(index, social_field, qualification_fields, "lead qualification")
index = index.replace('<p class="form-note">You will not be charged by submitting this form.</p>', '<p class="form-note">Typical response: within one business day. You will not be charged by submitting this form.</p>', 1)

last_faq = '<details class="reveal"><summary>How long does launch take?<span>+</span></summary><p>Most projects can reach a first review in about one to two weeks after all required content is received. Final launch depends on approvals, domain access, integrations, and any Google verification steps.</p></details>'
extra_faqs = last_faq + '<details class="reveal"><summary>Who is OneTap Creative best for?<span>+</span></summary><p>The standard plan is built for local service businesses that need a professional one-page website and one clear customer action, such as booking an appointment, requesting a quote, calling the business, or submitting a contact request.</p></details><details class="reveal"><summary>What happens after I submit the request form?<span>+</span></summary><p>OneTap Creative reviews the business, goals, current online presence, and Google Business Profile status. A reply is normally sent within one business day. If the project is a fit, the next steps are a written scope, client agreement, first payment, and onboarding form.</p></details><details class="reveal"><summary>Who manages the website and domain?<span>+</span></summary><p>OneTap Creative manages the website files, hosting, security, backups, and the agreed domain while the subscription is active. Ownership, transfer, buyout, cancellation, and offboarding terms are documented in the signed client agreement before work begins.</p></details>'
index = must_replace(index, last_faq, extra_faqs, "additional FAQs")

footer = '''<footer class="site-footer"><div class="container footer-grid"><div class="footer-brand"><img src="assets/images/onetap-logo-full-natural.png" alt="OneTap Creative"/><p>Founder-led websites, Google visibility, and ongoing support for local service businesses.</p></div><div><h3>Explore</h3><a href="#services">What’s Included</a><a href="#work">Real Work</a><a href="#why">Why OneTap</a><a href="#process">Process</a><a href="#pricing">Pricing</a></div><div><h3>Start a Project</h3><a href="#start">Submit a project request</a><p>Typical reply within one business day.<br/>Serving Stockton, surrounding communities, and remote clients.</p></div><div><h3>Legal</h3><a href="terms.html">Terms of Service</a><a href="privacy.html">Privacy Policy</a></div></div><div class="container footer-bottom"><span>© <span id="year"></span> OneTap Creative. All rights reserved.</span><span>Founder-led · Stockton, California</span><a href="#top">Back to top ↑</a></div></footer>'''
index, count = re.subn(r'<footer class="site-footer">.*?</footer>', footer, index, count=1, flags=re.S)
if count != 1:
    raise RuntimeError("Unable to replace footer")

index = index.replace('<script src="script.js?v=get-found-3"></script>', '<script src="script.js?v=launch-100"></script>', 1)
write("index.html", index)

styles = read("styles.css")
marker = "/* === FINAL LAUNCH POLISH — 100% PUBLIC WEBSITE === */"
if marker not in styles:
    styles += r'''

/* === FINAL LAUNCH POLISH — 100% PUBLIC WEBSITE === */
.hero-assurance{display:flex;flex-wrap:wrap;gap:8px;margin-top:13px;max-width:620px}.hero-assurance span{display:inline-flex;align-items:center;gap:7px;padding:8px 11px;border:1px solid var(--line);border-radius:999px;background:rgba(255,255,255,.025);color:#cbc6bb;font-size:.72rem;font-weight:800}.hero-assurance span::before{content:"✓";color:var(--gold)}
.real-work-grid{display:grid;gap:24px;margin-top:34px}.case-study{display:grid;gap:28px;padding:24px;border:1px solid rgba(214,173,60,.2);border-radius:28px;background:linear-gradient(145deg,rgba(255,255,255,.055),rgba(255,255,255,.018));overflow:hidden}.case-study-copy{align-self:center}.case-study-copy h3{font-size:clamp(2rem,6vw,3.4rem);margin:12px 0 15px}.case-study-copy>p:not(.eyebrow){color:var(--muted)}.case-study-copy ul{display:grid;gap:8px;padding:0;margin:22px 0 28px;list-style:none;color:#d3cfc5}.case-study-copy li::before{content:"✓";color:var(--gold);font-weight:900;margin-right:9px}.verified-work{display:inline-flex;padding:7px 10px;border:1px solid rgba(214,173,60,.35);border-radius:999px;color:var(--gold-light);font-size:.68rem;font-weight:900;text-transform:uppercase;letter-spacing:.09em}.case-study-live{width:min(100%,380px);justify-self:center;align-self:center;border:1px solid rgba(255,255,255,.14);border-radius:28px;background:#0b0d10;padding:8px;box-shadow:0 28px 70px rgba(0,0,0,.45)}.live-site-bar{height:31px;display:flex;align-items:center;gap:6px;padding:0 10px;background:#171a1e;border-radius:20px 20px 7px 7px;color:#8d929a;font-size:.64rem}.live-site-bar i{width:7px;height:7px;border-radius:50%;background:#565b62}.live-site-bar i:first-child{background:var(--gold)}.live-site-bar span{margin-left:6px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.live-site-viewport{height:540px;overflow:hidden;border-radius:7px 7px 19px 19px;background:#fff}.live-site-frame{width:100%;height:100%;border:0;background:#fff;pointer-events:none}.case-study-live>a{display:flex;justify-content:center;padding:12px 8px 5px;color:var(--gold-light);font-size:.76rem;font-weight:900}
.why-section{background:#efe8da;color:#151515}.why-section .eyebrow{color:#755918}.why-section .eyebrow span{background:#755918}.why-section em{color:#7f5f14}.why-grid{display:grid;gap:40px}.why-story>p:not(.eyebrow){color:#5d584e}.why-lead{font-size:1.1rem;font-weight:750}.founder-note{display:grid;grid-template-columns:58px 1fr;gap:15px;align-items:center;margin-top:28px;padding:18px;border:1px solid rgba(0,0,0,.13);border-radius:18px;background:rgba(255,255,255,.45)}.founder-note img{width:58px;height:58px;object-fit:contain}.founder-note span,.founder-note strong{display:block}.founder-note span{color:#7b5b12;font-size:.67rem;font-weight:900;text-transform:uppercase;letter-spacing:.12em}.founder-note strong{margin:3px 0;font-size:1rem}.founder-note p{margin:0;color:#625d53;font-size:.83rem}.why-card-grid{display:grid;gap:13px}.why-card{padding:23px;border:1px solid rgba(0,0,0,.13);border-radius:20px;background:rgba(255,255,255,.45)}.why-card b{color:#8a6717;font-size:.72rem}.why-card h3{margin:24px 0 9px}.why-card p{margin:0;color:#615b50;font-size:.9rem}
.four-step{grid-template-columns:1fr}.four-step li{min-height:0}.four-step .step-icon{display:grid;place-items:center;width:76px;height:76px;margin:22px 0;border:2px solid var(--gold);border-radius:50%;font-size:.58rem;color:var(--gold-light);font-weight:900;letter-spacing:.08em}.four-step h3{margin:0 0 11px}
.response-section{padding:72px 0;background:linear-gradient(145deg,#090b0d,#11151a);border-block:1px solid rgba(214,173,60,.19)}.response-shell{display:grid;gap:30px}.response-heading{max-width:760px}.response-heading h2{font-size:clamp(2.25rem,7vw,4.3rem)}.response-heading>p:last-child{color:var(--muted)}.response-grid{display:grid;gap:11px}.response-grid>div{display:grid;grid-template-columns:42px 1fr;column-gap:12px;padding:18px;border:1px solid var(--line);border-radius:17px;background:rgba(255,255,255,.025)}.response-grid b{grid-row:1/3;color:var(--gold);font-size:.7rem}.response-grid strong{display:block}.response-grid span{color:var(--muted);font-size:.82rem;margin-top:3px}.form-honeypot{position:absolute!important;left:-9999px!important;width:1px!important;height:1px!important;overflow:hidden!important}.submit-btn[disabled]{opacity:.72;cursor:wait;transform:none}.footer-bottom{gap:12px;flex-wrap:wrap}
@media(min-width:680px){.real-work-grid{gap:30px}.case-study{grid-template-columns:minmax(0,1fr) minmax(280px,.72fr);padding:32px}.why-card-grid{grid-template-columns:repeat(2,1fr)}.response-grid{grid-template-columns:repeat(2,1fr)}.four-step{grid-template-columns:repeat(2,1fr)}.form-two{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(min-width:960px){.why-grid{grid-template-columns:.9fr 1.1fr;gap:70px;align-items:center}.case-study{padding:42px}.four-step{grid-template-columns:repeat(4,1fr)}.four-step li{min-height:365px}.response-shell{grid-template-columns:.72fr 1.28fr;gap:54px;align-items:start}.response-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:679px){.case-study{padding:20px}.live-site-viewport{height:480px}.hero-assurance{gap:6px}.hero-assurance span{font-size:.66rem}.founder-note{grid-template-columns:48px 1fr}.founder-note img{width:48px;height:48px}}
'''
write("styles.css", styles)

script = read("script.js")
new_tail = r'''

// Final launch form routing, attribution, conversion events, and lazy project previews.
const formNextUrl = document.querySelector('#form-next-url');
const leadForm = document.querySelector('#lead-form');
if (formNextUrl) formNextUrl.value = new URL('thank-you.html', window.location.href).href;

const query = new URLSearchParams(window.location.search);
const trackingValues = {
  '#utm-source': query.get('utm_source') || '',
  '#utm-medium': query.get('utm_medium') || '',
  '#utm-campaign': query.get('utm_campaign') || '',
  '#utm-content': query.get('utm_content') || '',
  '#landing-page': window.location.href
};
Object.entries(trackingValues).forEach(([selector, value]) => {
  const field = document.querySelector(selector);
  if (field) field.value = value;
});

window.dataLayer = window.dataLayer || [];
document.querySelectorAll('a[href="#start"]').forEach(link => link.addEventListener('click', () => {
  window.dataLayer.push({ event: 'onetap_cta_click', cta_text: link.textContent.trim() });
}));
document.querySelectorAll('.case-study a[target="_blank"]').forEach(link => link.addEventListener('click', () => {
  window.dataLayer.push({ event: 'onetap_portfolio_click', destination: link.href });
}));
leadForm?.addEventListener('submit', () => {
  const submitButton = leadForm.querySelector('button[type="submit"]');
  if (submitButton) {
    submitButton.disabled = true;
    submitButton.innerHTML = 'Sending Request <span aria-hidden="true">…</span>';
  }
  window.dataLayer.push({
    event: 'onetap_lead_submit',
    lead_source: document.querySelector('#lead-source')?.value || 'Not provided',
    utm_source: query.get('utm_source') || 'direct'
  });
});

const liveFrames = [...document.querySelectorAll('.live-site-frame[data-src]')];
const loadFrame = frame => {
  if (!frame.src || frame.src === 'about:blank') frame.src = frame.dataset.src;
};
if ('IntersectionObserver' in window && !prefersReducedMotion) {
  const frameObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      loadFrame(entry.target);
      frameObserver.unobserve(entry.target);
    });
  }, { rootMargin: '500px 0px', threshold: 0.01 });
  liveFrames.forEach(frame => frameObserver.observe(frame));
} else {
  liveFrames.forEach(loadFrame);
}
'''
script, count = re.subn(r'\n// Keep the public offer aligned with OneTap Creative.*\Z', new_tail, script, count=1, flags=re.S)
if count != 1:
    raise RuntimeError("Unable to replace script tail")
write("script.js", script)

thank_you = '''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><meta name="robots" content="noindex,follow"/><meta name="description" content="OneTap Creative has received your online presence request."/><title>Request Received | OneTap Creative</title><link rel="icon" href="assets/images/onetap-icon-natural.png"/><link rel="stylesheet" href="styles.css?v=launch-100"/></head><body><main class="section-pad"><div class="container"><article class="thank-you-card"><a class="brand" href="index.html" aria-label="OneTap Creative home"><img alt="" class="brand-mark" src="assets/images/onetap-icon-natural.png"/><span class="brand-lockup"><strong><span>One</span><em>Tap</em></strong><small>CREATIVE</small></span></a><p class="eyebrow" style="justify-content:center;margin-top:35px"><span></span>Request received</p><h1>Your business is now in the OneTap review queue.</h1><p>Thank you for sharing your goals. OneTap Creative will review your business, current online presence, Google Business Profile status, and requested customer action. A reply is normally sent within one business day. No payment has been collected.</p><div class="next-steps"><div><b>1. Fit review</b><br/><span>We review your services, customers, current website or social presence, and what the new site needs to accomplish.</span></div><div><b>2. Personal follow-up</b><br/><span>You receive questions, fit feedback, or the recommended next step—normally within one business day.</span></div><div><b>3. Written scope</b><br/><span>If the project is a fit, pricing, responsibilities, timeline, ownership, and cancellation terms are confirmed in writing.</span></div><div><b>4. Payment and onboarding</b><br/><span>After approval, the first payment and full content intake begin the production process.</span></div></div><div style="display:flex;flex-wrap:wrap;gap:12px;justify-content:center"><a class="btn" href="index.html">Return to OneTap Creative</a><a class="btn btn-ghost" href="index.html#work">View Recent Work</a></div></article></div></main><script>window.dataLayer=window.dataLayer||[];window.dataLayer.push({event:'onetap_lead_complete'});</script></body></html>'''
write("thank-you.html", thank_you)

privacy = '''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/><meta name="description" content="Review how OneTap Creative collects and uses information submitted through its website."/><title>Privacy Policy | OneTap Creative</title><link href="assets/images/onetap-icon-natural.png" rel="icon"/><link href="styles.css?v=launch-100" rel="stylesheet"/></head><body><main class="section-pad"><article class="container" style="max-width:820px"><a class="brand" href="index.html"><img alt="" class="brand-mark" src="assets/images/onetap-icon-natural.png"/><span class="brand-lockup"><strong><span>One</span><em>Tap</em></strong><small>CREATIVE</small></span></a><p class="eyebrow" style="margin-top:55px"><span></span>Privacy</p><h1 style="font-size:clamp(2.7rem,8vw,5rem)">Privacy Policy</h1><p style="color:#aaa">Last updated July 25, 2026</p><section style="color:#c9c6be"><h2 style="font-size:1.8rem">Information collected</h2><p>When you submit a project request, OneTap Creative may collect your name, business name, email address, phone number, business type, website or social link, project goals, launch timing, lead source, Google Business Profile status, and other details you choose to provide. The form may also record the landing page and campaign parameters used to reach the website.</p><h2 style="font-size:1.8rem">How information is used</h2><p>Information is used to respond to inquiries, review project fit, prepare a written scope, support onboarding, provide contracted services, maintain client websites, and improve the inquiry experience.</p><h2 style="font-size:1.8rem">Website measurement</h2><p>The website may use hosting, performance, or analytics tools to understand page visits, referral sources, device performance, and interactions such as project-request submissions. OneTap Creative does not sell personal inquiry information.</p><h2 style="font-size:1.8rem">Form processing and service providers</h2><p>The project-request form may use a third-party form-delivery provider to send submissions to OneTap Creative. Hosting, domain, analytics, email, and other providers may process limited information as reasonably necessary to operate the website and deliver services. Do not submit passwords, payment-card details, government identification, medical information, or other sensitive information through the public request form.</p><h2 style="font-size:1.8rem">Retention and security</h2><p>Inquiry and client information may be retained as needed for communication, recordkeeping, service delivery, legal obligations, and dispute prevention. Reasonable safeguards are used, but no internet transmission or storage system can be guaranteed completely secure.</p><h2 style="font-size:1.8rem">Your choices</h2><p>You may request correction or deletion of inquiry information when reasonably possible and subject to legal or business recordkeeping requirements.</p><h2 style="font-size:1.8rem">Contact</h2><p>For a privacy question or request, use the <a href="index.html#start" style="color:#f0cf6a">OneTap Creative project-request form</a> and identify the request as a privacy matter.</p></section><a class="btn" href="index.html" style="margin-top:30px">Return Home</a></article></main></body></html>'''
write("privacy.html", privacy)

terms = '''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><meta name="robots" content="index,follow"/><meta name="description" content="Review the OneTap Creative Complete Online Presence Plan terms, including pricing, advanced SEO foundation, Google Business Profile assistance, monthly service, and scope boundaries."/><title>Terms of Service | OneTap Creative</title><link rel="icon" href="assets/images/onetap-icon-natural.png"/><link rel="stylesheet" href="styles.css?v=launch-100"/></head><body><main class="section-pad"><article class="container" style="max-width:820px"><a class="brand" href="index.html"><img alt="" class="brand-mark" src="assets/images/onetap-icon-natural.png"/><span class="brand-lockup"><strong><span>One</span><em>Tap</em></strong><small>CREATIVE</small></span></a><p class="eyebrow" style="margin-top:55px"><span></span>Service terms</p><h1 style="font-size:clamp(2.7rem,8vw,5rem)">Terms of Service</h1><p style="color:#aaa">Last updated July 25, 2026</p><section style="color:#c9c6be"><h2 style="font-size:1.8rem">Website inquiries</h2><p>Submitting the public request form does not create a client relationship, reserve a production date, or authorize a charge. A project begins only after OneTap Creative and the client approve a written scope or client agreement and the required payment is received.</p><h2 style="font-size:1.8rem">Complete Online Presence Plan</h2><p>OneTap Creative offers a standard Complete Online Presence Plan for $149 per month. The standard service may include a custom mobile-first one-page website, domain registration and renewal, hosting, SSL, basic backups, booking/contact/quote integration, an advanced SEO foundation, Google Search Console setup, Google Business Profile setup or optimization assistance, reasonable updates, maintenance, and ongoing technical support, subject to the signed client agreement.</p><h2 style="font-size:1.8rem">Advanced SEO foundation</h2><p>The standard launch foundation may include local keyword mapping, search-focused headings and page structure, title and meta-description optimization, technical SEO, canonical setup, mobile and performance optimization, image optimization, structured data when appropriate, sitemap and indexing setup, Google Search Console configuration, and alignment of core local business information.</p><p>The standard $149 plan does not include unlimited SEO consulting, guaranteed rankings, recurring blog or landing-page production, backlink campaigns, paid advertising, ecommerce SEO, multi-location SEO campaigns, citation cleanup across third-party directories, or other campaign-level work unless included in a separate written scope.</p><h2 style="font-size:1.8rem">Subscription, minimum term, and cancellation</h2><p>The service is $149 per month with an initial three-month minimum commitment, totaling $447 for the first three months. No separate setup fee applies to the standard included scope. After the minimum term, service continues month-to-month. Cancellation after the minimum requires at least 30 days’ written notice unless the signed client agreement states otherwise.</p><h2 style="font-size:1.8rem">Domain, hosting, and website management</h2><p>OneTap Creative manages the website files, hosting, SSL, backups, and the agreed business domain while the subscription is active. Domain registration and renewal are included during the active subscription. Transfer, buyout, cancellation, ownership, and early-termination terms are governed by the signed client agreement.</p><h2 style="font-size:1.8rem">Google Business Profile and search services</h2><p>Google Business Profile assistance may include accurate business information, categories, services, hours, photos, service areas, website connection, and verification guidance. Google controls verification, approval, suspension, indexing, Maps placement, and search rankings. OneTap Creative does not guarantee profile approval, first-page placement, rankings, traffic, leads, bookings, or sales.</p><h2 style="font-size:1.8rem">Client responsibilities</h2><p>Clients must provide accurate business information, lawful content, authorized images, domain or account access when required, Google verification materials, timely feedback, and approvals. Delays in content, access, verification, payment, or approval may affect the launch schedule.</p><h2 style="font-size:1.8rem">Reasonable updates and additional work</h2><p>Reasonable updates may include replacing photos, editing existing text, changing hours, services, pricing, contact details, or promotions within the approved layout. Major redesigns, additional pages, ecommerce, custom software, recurring content creation, new brand development, advanced integrations, or campaign-level SEO may require a separate quote.</p><h2 style="font-size:1.8rem">Response and timeline expectations</h2><p>OneTap aims to respond to new project requests within one business day and provide a first website review within the estimated project window after all required content and access are received. Response and delivery estimates are targets, not guarantees, and may change based on scope, client delays, integrations, verification, or circumstances outside OneTap Creative’s control.</p><h2 style="font-size:1.8rem">No guaranteed results</h2><p>OneTap Creative does not guarantee a specific number of visitors, leads, sales, bookings, quote requests, profile views, or search rankings.</p><h2 style="font-size:1.8rem">Controlling agreement</h2><p>This page is a general public summary. The signed client service agreement and written scope control the actual project, payment, ownership, transfer, cancellation, and service terms.</p><h2 style="font-size:1.8rem">Contact</h2><p>Questions may be submitted through the <a href="index.html#start" style="color:#f0cf6a">OneTap Creative project-request form</a>.</p></section><a class="btn" href="index.html" style="margin-top:30px">Return Home</a></article></main></body></html>'''
write("terms.html", terms)

manifest = {
    "name": "OneTap Creative",
    "short_name": "OneTap",
    "description": "Professional websites, Google visibility, and ongoing support for local service businesses.",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#080808",
    "theme_color": "#080808",
    "icons": [
        {
            "src": "/assets/images/onetap-icon-natural.png",
            "sizes": "512x512",
            "type": "image/png",
        }
    ],
}
write("manifest.webmanifest", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")

sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  <url><loc>https://onetapcreative.com/</loc><lastmod>2026-07-25</lastmod><changefreq>monthly</changefreq><priority>1.0</priority><image:image><image:loc>https://onetapcreative.com/assets/images/onetap-og-direction.jpg</image:loc><image:title>OneTap Creative complete online presence service</image:title></image:image></url>
  <url><loc>https://onetapcreative.com/terms.html</loc><lastmod>2026-07-25</lastmod><changefreq>yearly</changefreq><priority>0.3</priority></url>
  <url><loc>https://onetapcreative.com/privacy.html</loc><lastmod>2026-07-25</lastmod><changefreq>yearly</changefreq><priority>0.3</priority></url>
</urlset>
'''
write("sitemap.xml", sitemap)

print("Applied OneTap Creative final launch polish")
