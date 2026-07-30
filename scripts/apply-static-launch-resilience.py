from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"Expected {label} was not found")
    return text.replace(old, new, 1)

index_path = ROOT / "index.html"
index = index_path.read_text(encoding="utf-8")
index = index.replace("https://formsubmit.co/codicta@gmail.com", "https://formsubmit.co/clarence.workflow@gmail.com")
index = index.replace("<span>★ 5.0 reviews</span>", "<span>Trust section</span>")
index = index.replace('<div class="stars">5.0 ★★★★★</div><p>Local Business</p>', '<div class="stars">Business profile preview</div><p>Example layout</p>')
index = replace_once(
    index,
    '<input name="_template" type="hidden" value="table"/><input name="_captcha" type="hidden" value="true"/>',
    '<input name="_template" type="hidden" value="table"/><input name="_captcha" type="hidden" value="true"/><input id="lead-replyto" name="_replyto" type="hidden"/><input name="_autoresponse" type="hidden" value="Thank you for contacting OneTap Creative. Your project request was received and will normally be reviewed within one business day. No payment was collected. If the project is a fit, the next steps are a written scope, client agreement, first payment, and the mobile onboarding portal."/>',
    "public FormSubmit hidden fields",
)
index = replace_once(
    index,
    '<label>Email *<input autocomplete="email" name="Email" required type="email"/></label>',
    '<label>Email *<input autocomplete="email" id="lead-email" name="Email" required type="email"/></label>',
    "public lead email field",
)
index_path.write_text(index, encoding="utf-8")

onboarding_path = ROOT / "onboarding/index.html"
onboarding = onboarding_path.read_text(encoding="utf-8")
onboarding = onboarding.replace("https://formsubmit.co/codicta@gmail.com", "https://formsubmit.co/clarence.workflow@gmail.com")
if 'id="onboarding-replyto"' not in onboarding:
    onboarding = replace_once(
        onboarding,
        '<input type="hidden" name="_captcha" value="false" />',
        '<input type="hidden" name="_captcha" value="false" />\n      <input type="hidden" id="onboarding-replyto" name="_replyto" />\n      <input type="hidden" name="_autoresponse" value="OneTap Creative received your completed onboarding form. Your business information and uploaded files will be reviewed. You will be contacted if anything is missing before production begins." />',
        "onboarding FormSubmit hidden fields",
    )
onboarding_path.write_text(onboarding, encoding="utf-8")

# Tighten the regression audit so future releases cannot rely on runtime correction alone.
audit_path = ROOT / "scripts/audit-public-launch.py"
audit = audit_path.read_text(encoding="utf-8")
audit = audit.replace(
    "require(\"FORM_EMAIL = 'clarence.workflow@gmail.com'\" in public_patch and 'https://formsubmit.co/${FORM_EMAIL}' in public_patch, 'Public form runtime route is not unified')",
    "require('https://formsubmit.co/clarence.workflow@gmail.com' in index, 'Public form static route is not unified')\nrequire(\"FORM_EMAIL = 'clarence.workflow@gmail.com'\" in public_patch and 'https://formsubmit.co/${FORM_EMAIL}' in public_patch, 'Public form runtime fallback is not unified')",
)
audit = audit.replace(
    "require('https://formsubmit.co/clarence.workflow@gmail.com' in onboarding_patch, 'Onboarding runtime route is not unified')",
    "require('https://formsubmit.co/clarence.workflow@gmail.com' in onboarding, 'Onboarding static route is not unified')\nrequire('https://formsubmit.co/clarence.workflow@gmail.com' in onboarding_patch, 'Onboarding runtime fallback is not unified')",
)
audit = audit.replace(
    "require('Trust section' in public_patch and 'Business profile preview' in public_patch, 'Unsupported demo rating replacement is missing')",
    "require('★ 5.0 reviews' not in index and '5.0 ★★★★★' not in index, 'Unsupported demo rating claims remain in static HTML')\nrequire('Trust section' in index and 'Business profile preview' in index, 'Neutral demo trust labels are missing from static HTML')",
)
audit = audit.replace(
    "require('_autoresponse' in public_patch and '_replyto' in public_patch, 'Public confirmation/reply routing is missing')",
    "require('_autoresponse' in index and '_replyto' in index, 'Public static confirmation/reply routing is missing')\nrequire('_autoresponse' in public_patch and '_replyto' in public_patch, 'Public runtime confirmation/reply fallback is missing')",
)
audit = audit.replace(
    "require('_autoresponse' in onboarding_patch and '_replyto' in onboarding_patch, 'Onboarding confirmation/reply routing is missing')",
    "require('_autoresponse' in onboarding and '_replyto' in onboarding, 'Onboarding static confirmation/reply routing is missing')\nrequire('_autoresponse' in onboarding_patch and '_replyto' in onboarding_patch, 'Onboarding runtime confirmation/reply fallback is missing')",
)
audit_path.write_text(audit, encoding="utf-8")

print("Static hard-launch resilience applied.")
