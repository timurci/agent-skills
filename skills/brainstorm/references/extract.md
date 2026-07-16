# Extract — substance-only documentation

Use this only when the user asks for a summary, handout, extract, or similar close-out of a brainstorm. The discussion skill stays conversational; this file is the write-up path.

## Goal

Capture **substance** and **final conclusions** — what was decided, what matters, and what remains open.

Do **not** include:

- nitpicks and abandoned tangents
- the back-and-forth that led there
- steering prompts, meta-discussion, or process notes
- options that were explored and discarded, unless the discard itself is a lasting decision ("we will not do X because…")

## What to extract

From the conversation, produce only what still holds:

| Keep | Drop |
| --- | --- |
| Problem / goal as finally framed | Early wrong framings unless still relevant |
| Living agreements that still stand | Superseded agreements (or note them as superseded if useful) |
| Chosen direction and why (brief) | Full debate history |
| Critical trade-offs that constrain the design | Exhaustive option matrices |
| Constraints, non-goals, edge cases that matter | Speculative asides with no residual force |
| Open questions / unresolved forks | Rhetoric and encouragement |

If later agreements overrode earlier ones, document the **current** state. Mention a superseded point only when it prevents re-litigating a closed path.

## Shape of the handout

Prefer one document unless the user asks for a set, or the substance cleanly splits (e.g. architecture overview vs decision log).

Default structure (omit empty sections):

1. **Context** — one short paragraph: what we were figuring out
2. **Conclusions** — the settled substance; lead with decisions
3. **Critical constraints & trade-offs** — only the ones that still bind
4. **Open questions** — unresolved forks the user may continue later

Match the domain: for software architecture, decisions and constraints may look like lightweight ADRs; for product or strategy, tighter prose is fine. Form follows substance; do not force a template that adds empty sections.

## Voice

- Write as finished documentation the user can hand to a future reader (including a future agent).
- Neutral and concrete. No "we discussed…", "you said…", "I suggested…".
- Prefer present-tense commitments: "Use X for Y because Z."
- Short. Every sentence should earn its place as residual value from the discussion.

## Completion

The extract is done when a reader who never saw the conversation can act on the conclusions without the chat log — and when nothing essential from the final living agreements is missing.
