# Explaining a paper

## 1. Extract

Start by getting clean text, figures, and tables out of the PDF.

```bash
pip install pymupdf --break-system-packages
python - <<'EOF'
import pymupdf as fitz, pathlib
doc = fitz.open("paper.pdf"); out = pathlib.Path("extract"); out.mkdir(exist_ok=True)
text = []
for i, page in enumerate(doc, 1):
    text.append(f"\n\n=== PAGE {i} ===\n" + page.get_text())
    for j, img in enumerate(page.get_images(full=True)):
        pix = fitz.Pixmap(doc, img[0])
        if pix.n - pix.alpha >= 4: pix = fitz.Pixmap(fitz.csRGB, pix)
        if pix.width > 200: pix.save(out / f"p{i}_img{j}.png")
(out / "text.txt").write_text("".join(text))
EOF
```

For two-column layouts, equations, and tables, `marker` or GROBID give better structure than raw text extraction; if neither is installed, rasterize the page (`page.get_pixmap(dpi=150)`) and read it visually for anything the text dump garbles. If the user pasted the paper or attached it so the content is already in context, skip extraction.

## 2. Read for the contribution

Answer these in notes before outlining. Quote section/figure numbers for each.

1. What problem, and why did existing approaches fail at it?
2. What is the one new idea (ideally one sentence)?
3. What exactly is the mechanism: inputs, steps, outputs?
4. What is the evidence: datasets, baselines, headline numbers, ablations that isolate the idea?
5. What does the paper admit it can't do? What would you worry about that it didn't say?

If you can't answer #2 in one sentence, you aren't ready to design visuals.

## 3. Standard outline (adjust, don't force)

| # | Section (as claim) | Visual |
|---|---|---|
| 0 | Title + TL;DR (problem → trick → result) | none, or one hero stat |
| 1 | The problem: why the old way breaks | Before-state diagram or a tiny failing example |
| 2 | The key idea in one picture | The core diagram; this is the page's hero figure |
| 3 | How it works, step by step | Small multiples or annotated architecture; math here if needed |
| 4 | Training / setup details that matter | Pipeline flow (skip if not central) |
| 5 | What the results show | Highlighted chart or table; one sentence per headline number |
| 6 | Why it works (ablations) | Bar chart of ablation deltas |
| 7 | Limits and open questions | Cards: "Doesn't handle", "Assumes", "Unknown" |
| 8 | Remember / read next | 3-bullet recap, related work links |

## 4. Figures

- **Redraw, don't paste,** the architecture figure: copyright aside, paper figures are dense and unreadable at web width. Simplify to the 5–8 components that matter and say "simplified from Fig. 2" in the caption.
- Embedding an original figure is fine for results plots when it's the clearest evidence, with the figure number cited. Crop tight, embed as a data URI, and add your own one-line "what to notice".
- Results: rebuild as HTML tables or simple charts from the reported numbers so they match the page styling and the key row can be highlighted.

## 5. Fidelity rules

- Every numeric claim carries its source ("Table 2", "Sec. 4.3").
- Separate three voices visually and verbally: **what the paper claims**, **what the evidence shows**, **your interpretation**. Interpretation goes in the amber `.analogy` box or a clearly labeled "Our take" callout.
- Don't smooth over weak baselines, small sample sizes, or missing ablations; one honest paragraph in "Limits" earns the reader's trust.
- If the paper is a preprint, say so. If you couldn't verify something (e.g. an equation garbled in extraction), say that in the page rather than guessing.
- Define notation once, early, and keep it identical to the paper's symbols.
