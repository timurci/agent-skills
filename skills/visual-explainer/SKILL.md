---
name: visual-explainer
description: Use when the user wants a topic, dataset, paper, or concept made visual — asks for an infographic, one-pager, stat or comparison card, TL;DR graphic, or a sectioned explainer; uploads a paper to understand; or asks for something to be explained, even without saying "visual". Renders a designed HTML page to PNG, PDF, or HTML.
---

# Visual explainer

Teach one thing well, using pictures where pictures are better than words.

Both formats run the same method: understand, distill, build, render, then the **look pass** — read the lint, look at the image, fix what you see. The look pass is the gate; nothing else proves the page works.

## Formats

Pick from the user's wording. If it is ambiguous, choose and say which you assumed. If the user wants an answer in chat rather than a page, answer in chat.

| Format | Deliverable | Choose when |
|---|---|---|
| **One-pager** | a single image (PNG + HTML) a stranger gets in about ten seconds | the whole idea fits one image and must land at a glance |
| **Explainer** | a multi-section page, scrolling or paged, optionally PDF or per-section PNGs | the idea needs several sections, each carrying its own visual |

Format rules: [`references/one-page.md`](references/one-page.md), [`references/explainer.md`](references/explainer.md).

## Workflow

1. **Understand the source before designing anything** — do this in prose, before any code.
   - *Concept:* write down the 3–7 ideas a learner must hold, in dependency order.
   - *Paper or long document:* extract text, figures, tables, and equations first ([`references/paper-workflow.md`](references/paper-workflow.md)); note which figure and table numbers carry the key claims.
   - *Dataset or notes:* find the one number or comparison the eye should land on first.
   - *Facts check:* every number and name comes from the source or a lookup you performed.

   **Done when** every fact, number, and name the page will show traces to the source or to a lookup you made.

2. **Distill the claim.** One sentence the viewer should believe afterward; it becomes the title, and titles are claims, not topic labels — "Capacity Decides Fit, Bandwidth Decides Speed", not "GPU Comparison". Then outline: a one-pager gets 3–6 blocks supporting the claim (more than that is two infographics); an explainer gets a section count and length that follow the reader's voice ([`references/explainer.md`](references/explainer.md)), each section carrying the question it answers and its single visual named.

   **Done when** you can state the claim in one sentence and every block or section visibly supports it.

3. **Build the page.** Write the HTML yourself, styling it by whichever route in [`references/style.md`](references/style.md) the user's project already has — `assets/base.css` and the two templates in `assets/` are the shipped route — and keep the five colour roles fixed either way. Make each visual per [`references/toolkit.md`](references/toolkit.md) and [`references/diagrams.md`](references/diagrams.md).

   **Done when** `scripts/render.py` can screenshot the page as-is: no dev server, no build step the user did not ask for.

4. **Look pass.** Render (paths below are relative to this skill's directory), then:
   ```
   python scripts/render.py page.html out.png                   # the one image
   python scripts/render.py page.html out.pdf                   # a paginated PDF
   python scripts/render.py page.html shots/ --split section.s  # one PNG per section
   ```
   Setup once: `pip install playwright && playwright install chromium`. Fix the lint warnings, re-render, then look at the image and work the format's checklist ([`one-page.md`](references/one-page.md#look-pass-checklist), [`explainer.md`](references/explainer.md#look-pass-checklist)).

   **Done when** the lint is clean *and* every checklist item passes. Clean lint is necessary, not sufficient: it sees geometry only, so a stylesheet that never loaded or raw `$$` TeX still reports clean.

5. **Fact-pass.** Building introduced numbers the source never stated — axis floors, derived ratios, rounded figures, invented filler. Recheck every number, name, and claim against the source. Report numbers as the source gives them, with the table or figure reference, and label anything simplified or inferred ("simplified", "approximately", "our illustration, not from the paper").

   **Done when** every number on the page is either the source's own figure or labelled as yours, and every simplification is labelled on the page.

6. **Deliver** the PNG or the HTML page as the main output, plus the HTML so the user can edit text, and say what they should verify — numbers lifted from their material, estimates, anything you could not confirm. For edits, change the HTML and re-render rather than regenerating, so the design stays stable.

   **Done when** the user has the page and every number they should verify is named.

## Principles (both formats)

- **Heading = claim.** "Attention lets every word look at every other word", not "Attention". A reader skimming only the headings should get the argument.
- **One idea per block or section, one visual per idea.** If a section needs two figures, it is probably two sections.
- **One hero.** Name the single thing the eye lands on first and keep everything else quieter; if everything is bold, nothing is.
- **Words are scarce.** Body text supports the picture, and every visual must be *needed* to understand its idea.
- **Colour carries meaning, not decoration.** Five roles, whichever styling route the page takes: `subject` (the thing / recommended path), `baseline` (old or compared-to), `meta` (control / process), `alert` (warning, or the emphasized phrase), `note` (aside). Assign them once and hold them for the whole page; grey for everything that isn't the story.
- **Concrete before abstract.** A tiny worked example (3 tokens, 4 nodes, one user) comes before the general formulation.
- **Label your fidelity.** When you redraw a figure or simplify a mechanism, say so in the caption; the caption carries the distinction between the source's claim and your illustration.
- **Close the loop.** End with what to remember (3 bullets max), the limits, and what to read or try next. A one-pager's memory hook is the single callout; an explainer's is the closing section.
- **Density is a design choice, crowding is not.** Word budgets live in the format's page rules ([`one-page.md`](references/one-page.md)); diagram size limits live in [`diagrams.md`](references/diagrams.md). Split anything that exceeds them.
