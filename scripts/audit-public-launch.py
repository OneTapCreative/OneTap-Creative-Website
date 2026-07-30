from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
config = json.loads((ROOT / 'launch-config.json').read_text(encoding='utf-8'))
index = (ROOT / 'index.html').read_text(encoding='utf-8')
terms = (ROOT / 'terms.html').read_text(encoding='utf-8')
thank = (ROOT / 'thank-you.html').read_text(encoding='utf-8')
onboarding = (ROOT / 'onboarding/index.html').read_text(encoding='utf-8')
public_patch = (ROOT / 'script.js').read_text(encoding='utf-8')
onboarding_patch = (ROOT / 'onboarding/onboarding.js').read_text(encoding='utf-8')
robots = (ROOT / 'robots.txt').read_text(encoding='utf-8')
sitemap = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
combined_public = '\n'.join((index, terms, thank, onboarding))
errors = []

def require(condition, message):
    if not condition:
        errors.append(message)

require('$179' in index and '$537' in index, 'Approved pricing is missing from the homepage')
require('Advanced SEO foundation' in index or 'advanced SEO foundation' in index, 'Advanced SEO foundation is missing')
require('Two organized revision rounds' in index, 'Revision scope is missing')
require('30 minutes' in index, 'Monthly update allowance is missing')
require('$149' not in combined_public and '$447' not in combined_public, 'Old pricing remains in client-facing files')
require('basic local SEO' not in combined_public.lower(), 'Old basic SEO wording remains')
require('https://formsubmit.co/clarence.workflow@gmail.com' in index, 'Public form static route is not unified')
require("FORM_EMAIL = 'clarence.workflow@gmail.com'" in public_patch and 'https://formsubmit.co/${FORM_EMAIL}' in public_patch, 'Public form runtime fallback is not unified')
require('https://formsubmit.co/clarence.workflow@gmail.com' in onboarding, 'Onboarding static route is not unified')
require('https://formsubmit.co/clarence.workflow@gmail.com' in onboarding_patch, 'Onboarding runtime fallback is not unified')
require('_autoresponse' in index and '_replyto' in index, 'Public static confirmation/reply routing is missing')
require('_autoresponse' in public_patch and '_replyto' in public_patch, 'Public runtime confirmation/reply fallback is missing')
require('_autoresponse' in onboarding and '_replyto' in onboarding, 'Onboarding static confirmation/reply routing is missing')
require('_autoresponse' in onboarding_patch and '_replyto' in onboarding_patch, 'Onboarding runtime confirmation/reply fallback is missing')
require('★ 5.0 reviews' not in index and '5.0 ★★★★★' not in index, 'Unsupported demo rating claims remain in static HTML')
require('Trust section' in index and 'Business profile preview' in index, 'Neutral demo trust labels are missing from static HTML')
require('<link rel="canonical" href="https://onetapcreative.com/"' in index, 'Static production canonical is missing')
require('generate_lead' in public_patch, 'Lead analytics event is missing')
require('Disallow: /onboarding/' in robots, 'Private onboarding route is not blocked')
require('https://onetapcreative.com/' in sitemap, 'Homepage is missing from sitemap')
require('attorney review' not in terms.lower(), 'Internal legal reminder is visible')
require('mailto:' not in index, 'A personal email is publicly exposed')
for path in ('client-operations/CLIENT-OPERATIONS-KIT.md','client-operations/LEAD-TRACKER.csv','launch/HARD-LAUNCH-RUNBOOK.md','launch/EXTERNAL-ACTIVATION.md','launch/MOCK-CLIENT-TEST.md'):
    require((ROOT / path).exists(), f'Missing launch asset: {path}')

if errors:
    print('OneTap public launch audit: BLOCKED')
    for error in errors:
        print(f'- {error}')
    sys.exit(1)

print('OneTap public launch audit: PASS')
print(f"Offer: ${config['monthlyPrice']}/month, {config['minimumMonths']}-month minimum, ${config['initialCommitmentTotal']} initial commitment")
