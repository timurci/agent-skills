# Diagrams inside a page

Use when a page needs a real diagram (orchestrator → workers, harness vs harness, containers with arrows) that CSS cards can't express cleanly. The look to aim for is the shape vocabulary in the snippet below, with the page's role tokens carrying the meaning.

## Pick the tool

| Need | Tool | Trade-off |
|---|---|---|
| Plain flow / sequence / state, correctness over polish | Mermaid | Fast, auto-layout, generic look. Style with `themeVariables` (below) |
| Nested containers, grids, nice default themes | D2 | Better groups than Mermaid; needs the `d2` binary |
| Hand-tuned, brand-consistent, annotated diagrams | Inline SVG on a grid | Most work, best polish. Default choice for hero diagrams |

## Inline SVG recipe

1. Choose a `viewBox` (e.g. `0 0 1200 520`) and a 20px grid. Put every x/y on a multiple of 20 so things align.
2. Define reusable styles once in `<defs><style>` with the shape classes (`.node`, `.group`, `.note`, `.wire`); never repeat inline attributes per node.
3. Place nodes first, then arrows, then notes. Compute arrow endpoints from node edges (`x + w`, `y + h/2`), not by eye.
4. Text: ≥ 14px **at final rendered width**, aiming 15–18px, `font-family` same sans as the page, centered with `text-anchor="middle"` and `dominant-baseline="central"`. Keep labels ≤ 3 words per line; break with separate `<text>` lines. A wide `viewBox` in a narrow column shrinks the rendered size: a 1200-unit figure at the 860px reading column turns 17px text into 12px, so size up. (The lint measures the specified size, not the rendered one.)
5. Color: use the role tokens the page has already assigned — `--subject`, `--baseline`, `--meta`, `--alert`, `--note`, each with its `-bg` fill. `base.css` defaults them to green/blue/purple/red/amber, and whichever route styles the page remaps them ([`style.md`](style.md)); max 4 per figure.
6. Shapes: rounded rect = component, cylinder = storage, circle = actor/token, dashed rect = boundary/scope, small pale rect = annotation with a dashed connector. Accessibility: `role="img"` plus an `aria-label` that states the figure's message.

```html
<svg viewBox="0 0 1200 520" width="100%" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Orchestrator fans out to sandboxed workers">
  <defs>
    <style>
      text{font-family:var(--sans);font-size:17px;font-weight:650;fill:var(--ink);text-anchor:middle;dominant-baseline:central}
      .on-dark{fill:var(--bg)} .cap{font-size:14px;font-weight:500;fill:var(--subject-bg)}
      .node{rx:10;stroke-width:2}
      .dark{fill:var(--ink);stroke:var(--ink)}
      .active{fill:var(--subject-bg);stroke:var(--subject)}
      .group{fill:none;stroke:var(--ink);stroke-width:2;stroke-dasharray:7 6;rx:14}
      .note{fill:var(--note-bg);stroke:var(--note);rx:8}
      .wire{stroke:var(--ink);stroke-width:2;fill:none;marker-end:url(#a)}
      .ret{stroke:var(--alert);stroke-width:2;fill:none;marker-end:url(#ao)}
      .dash{stroke:var(--muted);stroke-width:1.6;stroke-dasharray:5 5;fill:none;marker-end:url(#ag)}
      .mk{fill:var(--ink)} .mk-alert{fill:var(--alert)} .mk-muted{fill:var(--muted)}
    </style>
    <marker id="a"  viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path class="mk" d="M0 0L10 5L0 10z"/></marker>
    <marker id="ao" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path class="mk-alert" d="M0 0L10 5L0 10z"/></marker>
    <marker id="ag" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path class="mk-muted" d="M0 0L10 5L0 10z"/></marker>
  </defs>

  <rect class="node dark" x="80" y="200" width="300" height="120"/>
  <text class="on-dark" x="230" y="250">Orchestrator Agent</text>
  <text class="on-dark cap" x="230" y="280">(no sandbox)</text>

  <rect class="group" x="480" y="40" width="340" height="440"/>
  <rect class="node active" x="520" y="80" width="260" height="70"/><text x="650" y="115">Background Agent</text>
  <rect class="node active" x="520" y="200" width="260" height="70"/><text x="650" y="235">Background Agent</text>

  <path class="wire" d="M380 240 L520 115"/>
  <path class="wire" d="M380 260 L520 235"/>
</svg>
```

## Mermaid, themed

Use for: plain flowcharts, sequence diagrams, state machines, simple timelines. When it comes out generic or tangled, redraw that one figure as hand SVG; don't fight the auto-layout. Theme it so it matches the page — point `themeVariables` at the page's token colors:

```html
<pre class="mermaid">
flowchart LR
  O[Orchestrator] --> A[Agent 1] --> S1[(Sandbox)]
  O --> B[Agent 2] --> S2[(Sandbox)]
</pre>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.9.1/mermaid.min.js"></script>
<script>
mermaid.initialize({startOnLoad:true,theme:'base',flowchart:{curve:'basis',htmlLabels:true},
  themeVariables:{fontFamily:'Inter, system-ui, sans-serif',fontSize:'16px',
  primaryColor:'#f8cf34',primaryBorderColor:'#e0b514',primaryTextColor:'#1b1d22',
  lineColor:'#1f2125',secondaryColor:'#e88a24',tertiaryColor:'#f8f9fb'}});
</script>
```

Past the node limit (Checks), auto-layout turns to spaghetti; hand-place the SVG instead. Mermaid renders client-side, so the render script's short wait covers it; confirm the diagram appears in the screenshot.

## Checks

- Arrowheads visible and pointing the right way; no arrow crossing a text label.
- Dashed = grouping/optional, solid = main flow, accent color = return/feedback. Say so in a tiny legend if the diagram isn't self-evident.
- Min text size 14px at final width.
- Whitespace around groups ≥ 20px.
- Node count ≤ 10 per figure; split bigger systems into multiple figures.
