# Visual toolkit

## 1. SVG figures

Rules, palette, shape vocabulary, and the full node/arrow/group snippet live in [`diagrams.md`](diagrams.md). Stay in geometry: LLMs draw geometry well and illustration badly.

## 2. Step-by-step small multiples (best way to teach a mechanism)

Three or four panels, same frame, state changing left to right. Build with a CSS grid of identical `<svg>`s plus a one-line caption each:

```html
<div class="grid g3">
  <figure class="fig"><svg viewBox="0 0 200 120">…state 1…</svg><figcaption>1. Tokens arrive</figcaption></figure>
  <figure class="fig"><svg viewBox="0 0 200 120">…state 2…</svg><figcaption>2. Each token scores the others</figcaption></figure>
  <figure class="fig"><svg viewBox="0 0 200 120">…state 3…</svg><figcaption>3. Scores become weights</figcaption></figure>
</div>
```

Keep geometry and positions identical across panels and change only what the step changes (highlight with the accent color). Viewers read the diff.

## 3. Charts

- **A few bars or points:** generate inline SVG or div bars directly from the numbers (see `.bar-row` in base.css). Zero-based axis unless you say otherwise in the caption. Label values on the bars; skip gridlines.
- **Lines, many series, scatter:** Vega-Lite is the most LLM-friendly (a JSON spec) and renders via `vega-embed`; Chart.js is the simple alternative. Both load as `<script>` tags. For pages that must work offline or on locked-down hosts, pre-render to SVG with Python (matplotlib/Altair → `svg`) and inline it.
- **Annotate the takeaway:** a highlighted bar plus a one-line label ("+4.2 points over baseline") beats a legend and a paragraph.
- **Reproduce paper tables as HTML tables** with the best result in bold. Cite "Table 3" in the caption. A number you hold only approximately belongs in a table with the source cited, not in a re-plotted chart.

## 4. Math

- Show an equation only if a reader needs the exact form. Always follow it with a "symbol → meaning" list or color-coded annotation.
- Easiest dependable path: **pre-render with KaTeX to MathML** and paste the result, so no fonts or extra CSS are needed:
  ```bash
  npm i katex
  node -e "console.log(require('katex').renderToString(String.raw\`\\frac{QK^T}{\\sqrt{d_k}}\`,{output:'mathml',displayMode:true}))"
  ```
  Chromium renders MathML natively. Put the output inside `.eq`.
- If the host allows stylesheets and fonts, KaTeX's auto-render script also works; verify in the screenshot that the equation isn't showing raw `$$`.
- Always verify the LaTeX against the paper; a wrong subscript is worse than no equation.

## 5. Mermaid

Tool choice, usage rules, the themed snippet, and the checks live in [`diagrams.md`](diagrams.md).

## 6. Interactivity (optional, only when it teaches)

Good: a slider that changes a parameter and updates a plain-SVG chart, a hover that reveals what each box does, a "step" button that advances a mechanism diagram. Keep it to vanilla JS in the same file. Everything interactive needs a static fallback state that makes sense in a screenshot and in PDF.

## 7. Hosting constraints

- Single self-contained `.html`; inline CSS and JS; embed images as `data:` URIs; pin library versions.
- Scripts from `cdnjs.cloudflare.com` are the safest. If publishing as a hosted page with a strict content-security policy, external stylesheets and arbitrary hosts may be blocked, so prefer inline SVG, pre-rendered math, and libraries that need only a script.
- Don't use `localStorage` for anything the content depends on.
- For print/PDF: `@media print` rules in the template hide the nav and avoid breaking figures across pages.
