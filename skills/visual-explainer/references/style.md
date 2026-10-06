# Styling: use ours, or bring your own

`assets/base.css` and the two templates are a **reference implementation**, not a requirement. Write the page from scratch; what stays fixed is the *design* content — see [What must survive any route](#what-must-survive-any-route). How the page is styled is a choice:

| Route | Use when | Cost |
|---|---|---|
| **Shipped components** — `base.css` + a template | a one-off page, no existing design system | the page carries the skill's default look |
| **Your own component set** — a stylesheet you build once and reuse | the user will make more than one page, or has a brand | one setup pass, then every page is content |
| **Tailwind**, with Tailwind UI components if licensed | the user already lives in Tailwind, or wants utilities | a CDN tag or a build step |

## Build the components once, then stop

When the user will make several pages, spend the first one on the components rather than the page: settle the colours, write the handful of blocks every page needs (card, stat, bar, step, tag, callout, figure), put them in one file, and reuse that file for every later page. The second page should be content only. Keep the file with the project (`./.visual-style/` is a fine home) and inline it when building each page.

## Tailwind

- **CDN, zero build:** `<script src="https://cdn.tailwindcss.com"></script>`, with the config script after it. Verified to render through `scripts/render.py`.
- **Pin the roles as theme colours** so the page keeps the skill's vocabulary:

  ```html
  <script>tailwind.config = { theme: { extend: { colors: {
    subject:'#0b6b4f', baseline:'#1b4f9c', meta:'#5b3fc4', alert:'#c0392b', note:'#a9711a' } } } }</script>
  ```

  Then `border-subject`, `bg-baseline`, and `text-alert` mean what they mean in `base.css`.
- **Built CSS, deterministic:** `npx tailwindcss -i in.css -o out.css --content page.html`, then `<link rel="stylesheet" href="out.css">`. Works offline, and a sibling file resolves for the render script over `file://` (verified).
- **Tailwind UI / Tailwind Plus components** are copy-paste HTML under a commercial licence — lift them only when the user has one, and adapt the markup to the page's roles and words budget instead of shipping the demo content.
- **One styling system per page.** On a Tailwind page leave `base.css` out; two systems fight over every default.

## Keeping `base.css`

Retargeting it is cheap: the `:root` block holds the colours, fonts, radius, spacing, and page width, and the roles point at the palette.

```css
:root{ --subject:#0b6b4f; --subject-bg:#e7f5ef;   /* meanings: SKILL.md */
       --baseline:#1b4f9c; --baseline-bg:#e9f0fb;
       --meta:#5b3fc4;     --meta-bg:#efecfb;
       --alert:#c0392b;    --alert-bg:#fdecea;
       --note:#a9711a;     --note-bg:#fdf3e0; }
```

Components reference the roles, never a raw hue, so remapping the five is a whole rebrand. The **wordmark** is the one page-level brand asset: put the name or an inlined `logo.svg` in the slot each template marks, one per page, in `--muted`/`--faint`.

## What must survive any route

- **The roles.** `--subject`… in CSS, theme colours in Tailwind, whatever you name in your own sheet. The mapping is the skill's content, the CSS is an implementation.
- **Renderability.** `scripts/render.py` loads the page over `file://`, waits for the network to settle, and screenshots `.page` unless you pass `--selector`; an output name ending in `.pdf` writes a paginated PDF instead. Local `<link>`/`<script>` siblings resolve; anything the page `fetch()`es at runtime does not — Chromium blocks `file://` CORS, so load assets through tags.
- **The layout rules**, on every page and in every styling route: the Principles section of `SKILL.md`, unchanged.
