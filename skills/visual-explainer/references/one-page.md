# One-pager format

One image a stranger understands in about ten seconds and remembers afterward. Distill first, lay out with a proven pattern, then build the page.

## Layout patterns

Pick by the shape of the content.

| Content shape | Pattern | Components |
|---|---|---|
| A vs B (products, approaches, before/after) | **Comparison:** two big cards with a `VS` between, a row of small spec cards, a "buys / doesn't buy" table | `.row .card .vs`, `.g4`, `table` |
| Stages, flow, evolution over time | **Pipeline:** 3 cards joined by arrows, then a numbered step row summarizing the loop | `.row .card .arrow`, `.step` |
| Rankings, benchmarks, scores | **Leaderboard:** 1–2 ranked bar cards, highlight the subject in green, a hero-stat strip below | `.bar-row .track`, `.stat .badge` |
| Many attributes across few items | **Matrix:** a table, with `.tag` color-coding for categories | `table`, `.tag` |
| One surprising number | **Hero stat:** giant number + one sentence + 3–4 `.chip` qualifiers | `.stat`, `.chip` |

Most pages are one pattern plus a callout. Combine at most two patterns; five different patterns read as clutter.

## Page rules

- **Width:** 1280px page, or 900px (`.page.narrow`) for tall or narrow posts; rendered at 2x.
- **Type:** sans for content (the `--sans` stack), monospace only for tiny uppercase labels, tags, and the callout; that pairing is what gives these posts their "technical but clean" feel. Reuse the scale in `base.css` rather than adding sizes. Retheming is a `:root` token override — fonts included — and the components stay put.
- **Color is semantic.** Each card gets one role accent (stripe + tag), 3 per page max; the `.c-subject` / `.c-baseline` / `.c-meta` / `.c-alert` / `.c-note` classes apply the five roles.
- **Styling:** any route ([`style.md`](style.md)); the components named below ship in `base.css`. The patterns, the role map, and the words budget below do not change.
- **Words are scarce:** card title ≤ 4 words, card body ≤ 20 words, pills 1–3 words, table cells ≤ 12 words, callout ≤ 20 words. If a sentence is longer, cut it; the user can say the rest out loud.
- **Space:** 24px gaps, generous card padding, no more than ~35% of the page filled with text.
- **One callout per page,** at the bottom, as the memory hook: the action or the implication, not the title repeated.
- **Footer:** sources, dates, and scale notes in small grey text. Bar charts that don't start at zero or use a custom scale (e.g. "bar scale: 1850") say so; truncated bars exaggerate gaps and viewers notice.

## Look-pass checklist

Look at the rendered image; the lint cannot see any of these.

- Can you state the claim after two seconds of looking?
- Is the eye drawn first to the hero, then to the callout — and does the callout carry the implication, rather than repeat the title?
- Do the limits make it onto the page? One footer line or one chip.
- Is the final aspect between 1:1 and 16:10? Very tall pages get skipped in feeds — check the PNG's dimensions, since tall content pushes the page past the band.
- Any card with a lot of empty space at the bottom next to a fuller sibling? Shorten the tall one, or let `.row` stretch; avoid mismatched heights.
- Any title wrapping to two lines in one card but not its siblings? Shorten, or wrap them all consistently.
- Contrast: grey text on grey surface at small sizes is the usual failure.
- Are the numbers right, and are units shown?
- Does every accent color mean something?
- Is anything simplified or inferred labelled as such, in the caption or the callout?
