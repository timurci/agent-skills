---
name: change-intent
description: Write a short note stating the intent behind this session's changes, so a reviewer can judge the diff against the request. Use when a task that changed files is wrapping up, and when the user asks about the intent.
---

# Change intent

A reviewer sees the diff, not the conversation. The request, the user's corrections and the decisions behind the code exist only in this session, so without a note the reviewer has to guess why anything is there. This note carries that context across in a few lines.

## What goes in

Every line must pass the **diff test**: if the diff shows it, the note omits it.

- **Asked**: what the user wanted and why, in their terms. Every constraint they set and every correction that changed direction lands here ("no flag, always do X").
- **Did**: how the request was met: why this shape, which cases are covered, and what was run to check them.
- **Beyond the ask**: anything you added or changed that wasn't requested, and why.
- **Left out**: what was deliberately skipped or deferred, and anything known not to work.

`Asked` is always there. Drop any other line that has nothing to say.

## Rules

- No more than 100 words. If it runs longer, you're restating the diff or the change grew past what was asked.
- Each line answers why this shape or how far the delivery goes.
- Write from the conversation, not from `git diff`. Cover only changes made in this session; if the tree holds changes you didn't make, leave them out.
- Be accurate rather than flattering. A case counts as covered only if you handled or tested it; say what you didn't run. If the request was ambiguous, say which reading you took.
- Describe the end state. Mention a dropped approach only if traces of it remain in the code.
- Before writing a **Beyond the ask** line, ask whether it belongs. An extra you can't justify in a sentence should be removed from the change, not explained.

## Example

Not this, because every line fails the diff test:

> Implemented retry logic in upload.py. Added a backoff helper and tests. Updated the docs.

This:

> **Asked:** retry uploads that fail with 429 or 503 only; user said other 4xx are caller bugs and must surface immediately.
> **Did:** exponential backoff in `upload()`. Covers 429 with a `Retry-After` header, 503 without one, and cancel mid-wait. Existing suite passes; new test for those three.
> **Beyond the ask:** capped the delay at 30s, because unbounded backoff stalled the test run.
> **Left out:** multipart uploads (user: separate PR). No jitter.

## Where it goes

Give the note in your final reply, and save it to `$(git rev-parse --git-dir)/change-intent.md` (usually `.git/change-intent.md`), overwriting any earlier one. That path is outside the working tree, so the note can't end up in the diff or a commit; the `review-additions` skill looks for it there. If the user names another place (the commit message, a PR description, a file), put it there instead. If the write is blocked or this isn't a git repo, the reply alone is fine.
