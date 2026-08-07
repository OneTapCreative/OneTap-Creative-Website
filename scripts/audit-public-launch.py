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
public_patch = read('script.js')
onboarding_patch = read('onboarding/onboarding.js')
robots = read('robots.txt')
sitemap = read('sitemap.xml')
readme = read('README.md')
combined_public = '\n'.join((index, terms, privacy, thank, onboarding, public_patch, onboarding_patch))
errors = []


def require(condition, message):
    if not condition:
        errors.append(message)


approved_price = config['monthlyPrice']
approved_total = config['initialCommitmentTotal']
form_id = config['formSubmitId']
secure_form_action = f'https://formsubmit.co/{form_id}'
secure_ajax_action = f'https://formsubmit.co/ajax/{form_id}'

require(approved_price == 179 and approved_total == 537, 'Launch config does not match the approved commercial offer')
require(f'${approved_price}' in index and f'${approved_total}' in index, 'Approved pricing is missing from the homepage')
require(f'${approved_price}' in terms and f'${approved_total}' in terms, 'Approved pricing is missing from Terms')
require(f'${approved_price}' in readme and f'${approved_total}' in readme, 'README pricing is out of sync')
require('Advanced SEO foundation' in index or 'advanced SEO foundation' in index, 'Advanced SEO foundation is missing')
require('Two organized revision rounds' in index, 'Revision scope is missing')
require('30 minutes' in index, 'Monthly update allowance is missing')
require('$149' not in combined_public and '$447' not in combined_public, 'Old pricing remains in client-facing files')
require('basic local seo' not in combined_public.lower(), 'Old basic SEO wording remains')

require(secure_form_action in index, 'Public static form does not use the secure FormSubmit route')
require(secure_form_action in onboarding, 'Onboarding static form does not use the secure FormSubmit route')
require(f"const FORM_ID = '{form_id}'" in public_patch, 'Public runtime form ID is out of sync')
require(f"const FORM_ID = '{form_id}'" in onboarding_patch, 'Onboarding runtime form ID is out of sync')
require('FORM_AJAX_ACTION' in public_patch and 'formsubmit.co/ajax/' in public_patch, 'Public AJAX form route is missing')
require('_captcha' in index and 'value="false"' in index, 'Public static form CAPTCHA setting is inconsistent')
require('_captcha' in onboarding and 'value="false"' in onboarding, 'Onboarding static form CAPTCHA setting is inconsistent')
require('_honey' in index, 'Public form honeypot is missing')
require('_autoresponse' in index and '_replyto' in index, 'Public static confirmation/reply routing is missing')
require('_autoresponse' in public_patch and '_replyto' in public_patch, 'Public runtime confirmation/reply fallback is missing')
require('_autoresponse' in onboarding and '_replyto' in onboarding, 'Onboarding static confirmation/reply routing is missing')
require('_autoresponse' in onboarding_patch and '_replyto' in onboarding_patch, 'Onboarding runtime confirmation/reply fallback is missing')
require('clarence.workflow@gmail.com' not in combined_public, 'Personal inbox is exposed in client-facing files')

require('★ 5.0 reviews' not in index and '5.0 ★★★★★' not in index, 'Unsupported demo rating claims remain in static HTML')
require('Trust section' in index and 'Business profile preview' in index, 'Neutral demo trust labels are missing from static HTML')
require('<link rel="canonical" href="https://onetapcreative.com/"' in index, 'Static production canonical is missing')
require('generate_lead' in public_patch, 'Lead analytics event is missing')
require('Disallow: /onboarding/' in robots, 'Private onboarding route is not blocked')
require('Disallow: /thank-you.html' in robots, 'Thank-you route is not blocked')
require('https://onetapcreative.com/' in sitemap, 'Homepage is missing from sitemap')
require('mailto:' not in index, 'A personal email is publicly exposed on the homepage')
require('Website measurement' in privacy, 'Privacy policy does not disclose website measurement')

for path in (
    '404.html',
    'client-operations/CLIENT-OPERATIONS-KIT.md',
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
    f"Offer: ${approved_price}/month, {config['minimumMonths']}-month minimum, "
    f"${approved_total} initial commitment"
)
print('Secure forms, SEO controls, privacy checks, and launch assets are aligned.')
