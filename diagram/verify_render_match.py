from pathlib import Path
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
if not CHROME.exists():
    CHROME = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

targets = [p.stem for p in sorted(ROOT.glob("*-diagram-*.html"))]

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=str(CHROME), headless=True)
    ctx = browser.new_context(viewport={"width":1280,"height":900}, device_scale_factor=2)
    page = ctx.new_page()
    for stem in targets:
        png = ROOT / f"{stem}.png"
        svg = ROOT / f"{stem}.svg"
        tmp = ROOT / f"_{stem}-svg-check.png"
        page.goto(svg.resolve().as_uri(), wait_until="load")
        try:
            page.wait_for_function("document.fonts.status === 'loaded'", timeout=10000)
        except Exception:
            pass
        page.locator("svg").screenshot(path=str(tmp), omit_background=True)
        a = Image.open(png).convert("RGBA")
        b = Image.open(tmp).convert("RGBA")
        diff = ImageChops.difference(a, b)
        bbox = diff.getbbox()
        print(stem, "MATCH" if bbox is None else "DIFF", bbox)
        if bbox is not None:
            diff.save(ROOT / f"_{stem}-diff.png")
        tmp.unlink(missing_ok=True)
    ctx.close()
    browser.close()
