#!/usr/bin/env python3
"""Render an HTML file to PNG or PDF and lint the layout.

Usage:
  python render.py page.html out.png [--selector .page] [--scale 2] [--viewport 1400]
  python render.py page.html out.pdf                        # paginated PDF (paper: viewport wide, 1:1.414)
  python render.py page.html out_dir/ --split section       # one PNG per <section> (multi-page explainers)

Setup (once):  pip install playwright && playwright install chromium

Prints warnings for text clipped inside its box, elements poking outside the page
container, nowrap text overflowing its parent, failed images, and tiny SVG text.
Fix every warning, re-render, then run a look pass on the image before delivering.
"""
import argparse, pathlib
from playwright.sync_api import sync_playwright

LINT_JS = """
(sel) => {
  const root = document.querySelector(sel) || document.body;
  const rb = root.getBoundingClientRect(); const out = [];
  root.querySelectorAll('*').forEach(el => {
    const r = el.getBoundingClientRect(); if (!r.width || !r.height) return;
    const tag = el.tagName.toLowerCase();
    const cls = (typeof el.className === 'string' && el.className) ? '.' + el.className.split(' ')[0] : '';
    const id = tag + cls;
    const txt = (el.textContent || '').trim().slice(0, 40);
    const cs = getComputedStyle(el);
    if (r.right > rb.right + 1 || r.left < rb.left - 1) out.push(`outside page horizontally: <${id}> "${txt}"`);
    if (el.children.length === 0 && txt && el.scrollWidth > el.clientWidth + 1 && cs.overflow !== 'visible')
      out.push(`clipped text: <${id}> "${txt}"`);
    if (el.children.length === 0 && txt && cs.whiteSpace === 'nowrap' && el.parentElement && el.scrollWidth > el.parentElement.clientWidth + 1)
      out.push(`nowrap text overflows parent: <${id}> "${txt}"`);
    if (tag === 'img' && !el.naturalWidth) out.push('image failed to load: ' + el.src.slice(0, 60));
    if (tag === 'text' || tag === 'tspan') {
      const fs = parseFloat(cs.fontSize); if (fs < 11) out.push(`tiny svg text (${fs}px): "${txt}"`);
    }
  });
  return out;
}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("out")
    ap.add_argument("--selector", default=".page")
    ap.add_argument("--scale", type=float, default=2)
    ap.add_argument("--viewport", type=int, default=1400)
    ap.add_argument("--split", default=None, help="CSS selector; screenshot each match separately")
    a = ap.parse_args()
    url = pathlib.Path(a.html).resolve().as_uri()
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": a.viewport, "height": 900}, device_scale_factor=a.scale)
        pg.goto(url)
        pg.wait_for_load_state("networkidle")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(500)  # let Mermaid / chart libs finish drawing
        warnings = pg.evaluate(LINT_JS, a.selector)
        if str(a.out).endswith(".pdf"):
            pg.pdf(path=str(a.out), print_background=True,
                   width=f"{a.viewport}px", height=f"{round(a.viewport * 1.414)}px")
            print("wrote", a.out)
        elif a.split:
            d = pathlib.Path(a.out)
            d.mkdir(parents=True, exist_ok=True)
            els = pg.query_selector_all(a.split)
            for i, el in enumerate(els, 1):
                el.screenshot(path=str(d / f"{i:02d}.png"))
            print(f"wrote {len(els)} images to {d}")
        else:
            el = pg.query_selector(a.selector) or pg.query_selector("body")
            el.screenshot(path=a.out)
            print("wrote", a.out)
        b.close()
    for w in sorted(set(warnings)):
        print("WARN:", w)
    if not warnings:
        print("lint: clean")


if __name__ == "__main__":
    main()
