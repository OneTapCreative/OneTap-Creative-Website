from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
config = json.loads((ROOT / 'launch-config.json').read_text(encoding='utf-8'))

read = lambda path: (ROOT / path).read_text(encoding='utf-8')
index = read('index.html')
terms = read('terms.html')
privacy = read('privacy.html')
thank = read('thank-you.html')
onboarding = read('onboarding/index.html')
agreement = read('agreement.html')
agreement_received = read('agreement-received.html')
agreement_js = read('agreement.js')
public_patch = read('script.js')
onboarding_patch = read('onboarding/onboarding.js')
robots = read('robots.txt')
sitemap = read('sitemap.xml')
readme = read('README.md')
client_ops = read('client-operations/CLIENT-OPERATIONS-KIT.md')
gbp_fast_track = read('client-operations/GBP-FAST-TRACK.md')
combined_public = '\n'.join((index, terms, privacy, thank, onboarding, agreement, agreement_received, public_patch, onboarding_patch, agreement_js))
errors = []


def require(condition, message):
    if not condition:
        errors.append(message)


start = config['plans']['start']
grow = config['plans']['grow']
form_recipient = config['formSubmitRecipient']
production_domain = config['productionDomain']
secure_form_action = f'https://formsubmit.co/{form_recipient}'

require(start['name'] == 'OneTap Start', 'Start plan name is incorrect')
require(start['monthlyPrice'] == 99 and start['initialCommitmentTotal'] == 297, 'Start plan config is incorrect')
require(start['monthlyUpdateMinutes'] == 15, 'Start update allowance is incorrect')
require(grow['name'] == 'OneTap Grow', 'Grow plan name is incorrect')
require(grow['monthlyPrice'] == 149 and grow['initialCommitmentTotal'] == 447, 'Grow plan config is incorrect')
require(grow['monthlyUpdateMinutes'] == 30, 'Grow update allowance is incorrect')

for label, plan in (('Start', start), ('Grow', grow)):
    require(f"${plan['monthlyPrice']}" in index and f"${plan['initialCommitmentTotal']}" in index, f'{label} pricing is missing from the homepage')
    require(f"${plan['monthlyPrice']}" in terms and f"${plan['initialCommitmentTotal']}" in terms, f'{label} pricing is missing from Terms')
    require(f"${plan['monthlyPrice']}" in readme and f"${plan['initialCommitmentTotal']}" in readme, f'{label} pricing is missing from README')

require('OneTap Start' in index and 'OneTap Grow' in index, 'Both public plans must be present')
require('You built the business.' in index and 'look like one.' in index.lower(), 'Emotion-led hero positioning is missing')
require('local service businesses' in index.lower(), 'Target local-service-business positioning is missing')
require('advanced seo' in index.lower(), 'Grow advanced SEO scope is missing')
require('15 minutes' in index and '30 minutes' in index, 'Plan update allowances are missing')
require('two organized revision rounds' in index.lower(), 'Revision scope is missing')
require('$179' not in combined_public and '$537' not in combined_public, 'Retired pricing remains in client-facing files')
require('basic local seo' not in combined_public.lower(), 'Old basic SEO wording remains')

require(secure_form_action in index, 'Public static form does not use the secure FormSubmit route')
require(secure_form_action in onboarding, 'Onboarding static form does not use the secure FormSubmit route')
require(f"const FORM_RECIPIENT = '{form_recipient}'" in public_patch, 'Public runtime form recipient is out of sync')
require(f"const FORM_RECIPIENT = '{form_recipient}'" in onboarding_patch, 'Onboarding runtime form recipient is out of sync')
require('FORM_AJAX_ACTION' in public_patch and 'formsubmit.co/ajax/' in public_patch, 'Public AJAX form route is missing')
require('_captcha' in index and 'value="false"' in index, 'Public static form CAPTCHA setting is inconsistent')
require('_captcha' in onboarding and 'value="false"' in onboarding, 'Onboarding static form CAPTCHA setting is inconsistent')
require('_honey' in index, 'Public form honeypot is missing')
require('_autoresponse' in index and '_replyto' in index, 'Public static confirmation/reply routing is missing')
require('_autoresponse' in public_patch and '_replyto' in public_patch, 'Public runtime confirmation/reply fallback is missing')
require('_autoresponse' in onboarding and '_replyto' in onboarding, 'Onboarding static confirmation/reply routing is missing')
require('_autoresponse' in onboarding_patch and '_replyto' in onboarding_patch, 'Onboarding runtime confirmation/reply fallback is missing')
require('clarence.workflow@gmail.com' not in '\n'.join((index, terms, privacy, thank, onboarding, public_patch, onboarding_patch)), 'Personal inbox is exposed on a public-facing page')

require('★ 5.0 reviews' not in index and '5.0 ★★★★★' not in index, 'Unsupported demo rating claims remain in static HTML')
require('DJ JRV / Romero Vision' in index and 'Freda the Barber' in index, 'Real client proof is missing from the homepage')
require('<iframe' not in index, 'Homepage portfolio should not rely on iframe previews')
require('hero-client-preview' in index and 'portfolio-project-preview' in index, 'Real-client visual previews are missing')
require('id="services"' not in index and 'id="why"' not in index, 'Removed long-form homepage sections returned unexpectedly')
require('compact-benefits' in index and 'process-timeline' in index, 'Simplified homepage structure is missing')
require(f'<link rel="canonical" href="{production_domain}"' in index, 'Static production canonical is missing')
require('generate_lead' in public_patch, 'Lead analytics event is missing')
require('Disallow: /onboarding/' in robots, 'Private onboarding route is not blocked')
require('Disallow: /thank-you.html' in robots, 'Thank-you route is not blocked')
require(production_domain in sitemap, 'Homepage is missing from sitemap')
require('mailto:hello@onetapcreative.com' in index, 'Official business email is missing from the homepage')
require('gmail.com' not in index.lower(), 'A personal Gmail address is publicly exposed on the homepage')
require('Website measurement' in privacy, 'Privacy policy does not disclose website measurement')
require('Agreement and client records' in privacy, 'Privacy policy does not cover agreement records')
require(config.get('agreementProvider') == 'Square Contracts', 'Square Contracts is not configured as the agreement provider')
require(config.get('websiteAgreementCollection') is False, 'Website agreement collection must remain disabled')
require(config.get('paymentFlow') == 'Square recurring payment links', 'Square payment-link flow is not configured')
require(config.get('paymentLinks', {}).get('startRedirect') == '/onboarding/?plan=start', 'Start payment redirect is incorrect')
require(config.get('paymentLinks', {}).get('growRedirect') == '/onboarding/?plan=grow', 'Grow payment redirect is incorrect')
require("Payment Redirect Plan" in onboarding_patch and "URLSearchParams" in onboarding_patch, 'Onboarding does not preselect the paid plan from Square redirect')
require('noindex,nofollow,noarchive' in agreement, 'Agreement page must remain private/noindex')
require('noindex,nofollow,noarchive' in agreement_received, 'Agreement receipt page must remain private/noindex')
require('Disallow: /agreement.html' in robots and 'Disallow: /agreement-received.html' in robots, 'Retired agreement routes are not blocked in robots.txt')
require('<form' not in agreement, 'Retired agreement page must not collect signatures')
require('Square Contracts' in agreement, 'Retired agreement page must direct clients to Square Contracts')
require((ROOT / 'client-operations/SQUARE-CONTRACT-SOP.md').exists(), 'Missing Square Contracts SOP')

require('never blocks an otherwise-ready website launch' in client_ops.lower(), 'Client operations do not clearly enforce nonblocking GBP launch')
require('OneTap Start' in client_ops and 'OneTap Grow' in client_ops, 'Client operations do not define both plans')
require('pride, confidence, trust, relief, and growth' in client_ops.lower(), 'Emotion-led discovery guidance is missing')
require('must **not delay a website launch**' in gbp_fast_track, 'GBP fast-track does not define the nonblocking launch rule')
require('client remains the business owner' in gbp_fast_track.lower(), 'GBP ownership policy is missing')
require('manager' in gbp_fast_track.lower(), 'GBP manager-access workflow is missing')
require('verification pending' in gbp_fast_track.lower(), 'GBP pending-verification status is missing')

for path in (
    '404.html',
    'client-operations/CLIENT-OPERATIONS-KIT.md',
    'client-operations/GBP-FAST-TRACK.md',
    'client-operations/LEAD-TRACKER.csv',
    'launch/HARD-LAUNCH-RUNBOOK.md',
    'launch/EXTERNAL-ACTIVATION.md',
    'launch/MOCK-CLIENT-TEST.md',
    'launch/OWNER-CHECKLIST.md',
    'vercel.json',
):
    require((ROOT / path).exists(), f'Missing launch asset: {path}')

if errors:
    print('OneTap public launch audit: BLOCKED')
    for error in errors:
        print(f'- {error}')
    sys.exit(1)

print('OneTap public launch audit: PASS')
print(
    f"Offers: Start ${start['monthlyPrice']}/month (${start['initialCommitmentTotal']} minimum total); "
    f"Grow ${grow['monthlyPrice']}/month (${grow['initialCommitmentTotal']} minimum total)"
)
print('Two-plan pricing, emotion-led positioning, secure forms, SEO controls, privacy checks, GBP launch policy, and launch assets are aligned.')
