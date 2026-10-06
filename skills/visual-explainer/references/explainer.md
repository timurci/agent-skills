# Explainer format

A multi-section page where each section answers one question and carries one visual, written for a specific reader.

## Voice

Pick from the user's wording and context; if ambiguous, default to *practitioner* and say what you assumed.

| | **ELI5 / newcomer** | **Practitioner** (default) | **Researcher / paper deep-dive** |
|---|---|---|---|
| Reader | Smart, no background | Technical, new to this topic | Knows the field, wants the contribution fast |
| Voice | Short sentences, everyday words, "imagine…" | Direct, precise, defines jargon once | Dense but structured, states assumptions, cites sections/figures |
| Anchor | **One analogy** carried through the page, with a note where it breaks | Running example with concrete numbers | The paper's own claims, baselines, and ablations |
| Visuals | Illustrated metaphors, before/after, step-by-step panels built from shapes | Flow and architecture diagrams, annotated charts | Reproduced-then-simplified architecture figure, results tables/charts, equation walkthroughs |
| Math | Avoid; use a number example | Only when it earns its place, always explained in words | Show it, then annotate each term |
| Length | 4–6 sections, ~600–900 words | 5–8 sections, ~1200–2000 words | 6–9 sections, ~1500–2500 words |

## Section plan

Build up, don't dump: order by dependency — problem → intuition → mechanism → evidence → limits. Introduce each term the moment it is needed, with a plain-language gloss. The standard outline for a paper is in [`paper-workflow.md`](paper-workflow.md).

## Page and layout

- Reading column ~860px, 18px body, 1.6 line height; figures may be wider. Sticky mini table of contents at the top.
- Every figure gets a caption that says what to notice, not just what it is: "Notice the dashed box: nothing inside it can touch the network."
- Reuse components from `base.css` and the template: `.analogy`, `.sowhat`, `.eq`, `figure.fig`, cards, tags, steps, callouts. Consistent components are what make the page look designed rather than generated.
- **Visual first for structure, text first for reasoning.** Processes, architectures, and comparisons deserve a picture; arguments and caveats deserve prose.
- **Paged variant:** if the user wants slide-like pages, make each `section.s` exactly one viewport (`min-height:100vh`, scroll-snap) with next/previous buttons, and export with `--split section.s`.
- **Styling:** any route ([`style.md`](style.md)). The roles still apply: `.tldr` and `.sowhat` carry `--subject`, `.analogy` carries `--note`. The reading column and figure widths are structure — they hold unless the user asks otherwise.

## Choosing the visual

Recipes, snippets, and constraints live in [`toolkit.md`](toolkit.md) and [`diagrams.md`](diagrams.md).

| Idea type | Visual |
|---|---|
| Sequence of steps / data flow | Mermaid `flowchart` for plain structure; hand SVG when polish matters |
| System architecture, containers, groups | Inline SVG on a grid (dashed groups, labeled arrows) |
| Interactions over time (client/server, agents) | Mermaid `sequenceDiagram` |
| Comparison of options | Cards + table (components from `base.css`) |
| Quantities, results, ablations | Bar/line chart as generated SVG or Vega-Lite; annotate the key bar |
| Intuition for a mechanism | Small-multiples SVG: 3–4 panels showing step-by-step state change |
| Equation | KaTeX or pre-rendered MathML, then a "symbol → meaning" row |
| Hierarchy / taxonomy | Nested boxes or an indented tree |
| Before / after, old / new | Two-column cards with identical structure |

## Look-pass checklist

Look at the rendered sections; the lint cannot see any of these.

- Is every visual *needed* to understand its section, and does it match the text beside it?
- Is any figure unreadable at final width — small labels, overlapping arrows, clipped boxes?
- Does every caption say what to notice?
- Is each term defined where it first appears, in the register of the chosen voice?
- Does the closing section close the loop — what to remember (3 bullets max), the limits, what to read or try next?
- Is anything simplified or inferred labelled as such, in the caption or the callout?
