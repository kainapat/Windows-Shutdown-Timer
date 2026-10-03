from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
if not CHROME.exists():
    CHROME = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

def export_one(page, src: Path, out: Path):
    page.goto(src.resolve().as_uri(), wait_until="load")
    try:
        page.wait_for_function("document.fonts.status === 'loaded'", timeout=10000)
    except Exception:
        pass
    page.locator("svg").first.screenshot(path=str(out), omit_background=True)

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=str(CHROME), headless=True)
    context = browser.new_context(
        viewport={"width": 1280, "height": 900},
        device_scale_factor=2,
    )
    page = context.new_page()
    for src in sorted(ROOT.glob("*-diagram-*.html")):
        out = src.with_suffix(".png")
        export_one(page, src, out)
        print(f"{src.name} -> {out.name}")
    context.close()
    browser.close()
