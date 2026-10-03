from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
if not CHROME.exists():
    CHROME = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

CHECK_JS = r"""
() => {
  const svg = document.querySelector("svg");
  const svgRect = svg.getBoundingClientRect();
  const texts = [...svg.querySelectorAll('text[data-role="text"]')];
  const nodes = [...svg.querySelectorAll('[data-role="node"]')];
  const masks = [...svg.querySelectorAll('[data-role="label-mask"]')];
  const connectors = [...svg.querySelectorAll('[data-role="connector"]')];

  const rect = (el) => {
    const r = el.getBoundingClientRect();
    return {x:r.x, y:r.y, right:r.right, bottom:r.bottom, width:r.width, height:r.height};
  };
  const overlap = (a,b,pad=0) => {
    const left = Math.max(a.x+pad,b.x+pad);
    const right = Math.min(a.right-pad,b.right-pad);
    const top = Math.max(a.y+pad,b.y+pad);
    const bottom = Math.min(a.bottom-pad,b.bottom-pad);
    return {w:right-left,h:bottom-top,hit:right-left>0 && bottom-top>0};
  };
  const label = (el) => (el.textContent || el.getAttribute('data-role') || el.tagName).trim();

  const issues = [];

  // Text must not collide with other text. Small antialiasing/contact tolerances are ignored.
  const trects = texts.map(el => ({el, r:rect(el), label:label(el)}));
  for (let i=0; i<trects.length; i++) {
    for (let j=i+1; j<trects.length; j++) {
      const o = overlap(trects[i].r, trects[j].r, 0.75);
      if (o.hit && o.w > 2 && o.h > 2) {
        issues.push({
          kind:"text-overlap",
          a:trects[i].label,
          b:trects[j].label,
          width:+o.w.toFixed(1),
          height:+o.h.toFixed(1)
        });
      }
    }
  }

  // Label masks may cover connectors but never a node.
  const nrects = nodes.map(el => ({el, r:rect(el)}));
  for (const mask of masks) {
    const mr = rect(mask);
    for (const n of nrects) {
      const o = overlap(mr, n.r, 2);
      if (o.hit && o.w > 2 && o.h > 2) {
        issues.push({kind:"label-mask-node-overlap", mask:mr, node:n.r});
      }
    }
  }

  // No connector may pass through the interior of a node.
  const inside = (p, r, inset=4) =>
    p.x > r.x + inset && p.x < r.right - inset &&
    p.y > r.y + inset && p.y < r.bottom - inset;

  for (const conn of connectors) {
    if (!(conn instanceof SVGGeometryElement)) continue;
    const total = conn.getTotalLength();
    const ctm = conn.getScreenCTM();
    if (!ctm || !Number.isFinite(total) || total <= 0) continue;
    const steps = Math.max(8, Math.min(400, Math.ceil(total / 4)));
    let bad = null;
    for (let i=0; i<=steps && !bad; i++) {
      const p = conn.getPointAtLength(total * i / steps);
      const sp = new DOMPoint(p.x,p.y).matrixTransform(ctm);
      for (const n of nrects) {
        if (inside(sp,n.r,4)) {
          bad = {x:+sp.x.toFixed(1), y:+sp.y.toFixed(1), node:n.r};
          break;
        }
      }
    }
    if (bad) issues.push({kind:"connector-through-node", point:bad});
  }

  // Important rendered content stays inside the SVG viewport.
  const watched = [...texts, ...nodes, ...masks, ...connectors];
  for (const el of watched) {
    const r = rect(el);
    if (r.x < svgRect.x-1 || r.y < svgRect.y-1 ||
        r.right > svgRect.right+1 || r.bottom > svgRect.bottom+1) {
      issues.push({kind:"outside-viewbox", element:label(el), rect:r});
    }
  }

  return {
    issues,
    counts: {
      text:texts.length,
      nodes:nodes.length,
      masks:masks.length,
      connectors:connectors.length
    }
  };
}
"""

def main():
    files = sorted(ROOT.glob("*-diagram-*.html"))
    failed = False
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=str(CHROME), headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()
        for path in files:
            page.goto(path.resolve().as_uri(), wait_until="load")
            try:
                page.wait_for_function("document.fonts.status === 'loaded'", timeout=10000)
            except Exception:
                pass
            result = page.evaluate(CHECK_JS)
            issues = result["issues"]
            counts = result["counts"]
            if issues:
                failed = True
                print(f"{path.name} FAIL {counts}")
                for issue in issues:
                    print("  ", issue)
            else:
                print(f"{path.name} PASS {counts}")
        context.close()
        browser.close()
    raise SystemExit(1 if failed else 0)

if __name__ == "__main__":
    main()
