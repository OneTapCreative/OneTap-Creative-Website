from pathlib import Path

root = Path(__file__).resolve().parents[1]
index_path = root / "index.html"
styles_path = root / "styles.css"

index = index_path.read_text(encoding="utf-8")
old_iframe = 'class="live-site-frame" data-src='
new_iframe = 'class="live-site-frame" scrolling="no" data-src='
count = index.count(old_iframe)
if count != 2:
    raise RuntimeError(f"Expected 2 project preview iframes, found {count}")
index = index.replace(old_iframe, new_iframe)
index_path.write_text(index, encoding="utf-8")

styles = styles_path.read_text(encoding="utf-8")
old_css = '.live-site-viewport{height:540px;overflow:hidden;border-radius:7px 7px 19px 19px;background:#fff}.live-site-frame{width:100%;height:100%;border:0;background:#fff;pointer-events:none}'
new_css = '.live-site-viewport{position:relative;height:540px;overflow:hidden;border-radius:7px 7px 19px 19px;background:#fff}.live-site-frame{display:block;width:calc(100% + 24px);max-width:none;height:100%;margin-right:-24px;border:0;background:#fff;pointer-events:none;overflow:hidden;scrollbar-width:none}'
if old_css not in styles:
    raise RuntimeError("Project preview CSS anchor not found")
styles = styles.replace(old_css, new_css, 1)
styles_path.write_text(styles, encoding="utf-8")

print("Hidden scrollbars on both live project previews")
