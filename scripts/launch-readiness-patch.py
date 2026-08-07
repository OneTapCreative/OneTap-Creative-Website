from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
FORM_ID = "3770cd21b709b2fc75672c99acb98256"
OLD_ACTION = "https://formsubmit.co/clarence.workflow@gmail.com"
NEW_ACTION = f"https://formsubmit.co/{FORM_ID}"

for relative_path in ("index.html", "onboarding/index.html"):
    path = ROOT / relative_path
    text = path.read_text(encoding="utf-8")
    if OLD_ACTION not in text:
        raise SystemExit(f"Expected legacy static form route not found in {relative_path}")
    text = text.replace(OLD_ACTION, NEW_ACTION)
    text = re.sub(
        r'(<input(?=[^>]*name="_captcha")[^>]*\bvalue=")true(")',
        r'\1false\2',
        text,
    )
    if OLD_ACTION in text:
        raise SystemExit(f"Legacy personal-email form route remains in {relative_path}")
    path.write_text(text, encoding="utf-8")

print("Static public and onboarding form fallbacks now use the secure FormSubmit route.")
