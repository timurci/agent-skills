---
name: eval-driven-design
description: Use when the user wants eval-driven design or EDD, agent evaluation workflow, eval guidelines/criteria/metrics/rubrics, capability vs regression suites, or pass@k or pass^k reporting. Also use when the user asks how to tell if an agent or AI system is actually working, how to catch regressions before shipping, how to build a test suite for a non-deterministic system, or expresses doubt about an LLM judge's reliability — even if they don't use eval-specific vocabulary.
---

# Eval-driven design (EDD)

EDD is TDD for agents: **specify success before (or while) building**, then climb and guard that bar. Mechanics differ — stochastic **trials**, graded **metrics**, unit under test is usually **model + agent harness**.

**Core loop:** evidence (real transcripts/failures) → guideline → criteria → metrics → tasks (from dataset rows) → trials → pass rules → report (and optional gate).

```text
Read what actually happens (transcripts/failures);
give the agent a task (from a dataset row); it runs (trial);
apply a metric to judge a criterion from the guideline;
aggregate with pass rules and reports.
```

## Terms you must not conflate

| Word | Means | Does not mean |
|------|--------|----------------|
| **Task** | One job for the agent | A criterion, a metric, or a whole dataset |
| **Criterion** | What good/bad means | How you measure it |
| **Metric** | How you measure a criterion → score | The agent’s job |
| **Rubric** | Spec inside a **judge** metric | Required for code metrics |
| **Suite** | Tasks + scoring purpose | A raw dump of rows |
| **pass@k / pass^k** | Multi-trial reliability over **binary trial success** | A substitute for defining success |

Full glossary: [`references/glossary.md`](references/glossary.md).  
Axes and criterion families: [`references/coverage.md`](references/coverage.md).

**Domain language:** prefer **metric** (and **rubric** for judges). **Grader** is optional harness jargon for the adapter that runs a metric on a trial.

**Layers:**

```text
Domain:  guideline (+ criteria), metrics (code | rubric-judge), business mapping
Eval:    Spec (datasets → tasks → suites, pass rules, gates)
         Runtime (harness, storage, CI) — implements the spec
```

## Workflow

Treat steps 0–5 as one fast pass, not a waterfall. Get a thin version of every step working end-to-end before deepening any one step. Revisit earlier steps as Step 6 (build/measure/iterate) surfaces gaps. Step 0 is skippable only if a criteria list already exists and is *evidenced*, not just assumed. For a narrow question (e.g. only pass@k), jump to the relevant step and load its reference; still respect the term table above.

### 0. Error analysis first

Before writing any guideline, read a sample of real transcripts (production logs, pilot runs, or manual dry-runs if nothing exists yet). A guideline written without this usually encodes what you *imagine* goes wrong, not what actually does — let criteria in Step 1 emerge from real failures, then check the list against [`references/coverage.md`](references/coverage.md) for blind spots.

**Done when:** you can point to specific transcripts that justify each criterion you're about to write.

### 1. Guideline and criteria

Write what the application **should** and **should not** do in domain language. List **criteria** inside that guideline (application-specific names, not a fixed universal list).

Use criterion families as a **coverage checklist** (not a metric schema): domain/cognitive · generation · instruction-following · operational. Load [`references/coverage.md`](references/coverage.md) when choosing what to cover.

**Done when:** a reader can list the criteria and state should/shouldn’t without seeing implementation; two experts would agree on binary pass/fail for each crisply defined criterion.

### 2. Metrics (and rubrics)

For each criterion: choose score shape (binary / int / \[0,1\] / …) and one or more **metrics**.

- **Code metric** — deterministic check → score (+ optional feedback).
- **Judge metric** — **rubric** (levels, rules, examples) + human or LLM → score (+ feedback).

**Method** = procedure; **metric** = that measurement as the tracked quantity. One criterion may have several metrics (e.g. cheap signal @100% + expensive judge @1%). Prefer **outcomes** over brittle full tool-call paths unless process *is* the product. Prefer code metrics where possible; judges where necessary; humans for gold standard and calibration.

Metrics live in the **domain** (what you optimize against). The guideline stays the coarse doc; rubrics are operational detail for judge metrics.

**Done when:** every criterion has at least one metric; each judge metric has an unambiguous rubric with examples; score shapes and ownership (domain) are explicit.

### 3. Business mapping

Tie metric bands to business outcomes (automation rate, cost, risk). Eval scores are proxies until this link is stated and later validated in production.

**Done when:** for primary metrics, it is clear what a score change is *worth* and why you would invest to move it.

### 4. Datasets, tasks, suites

- **Dataset** — rows (inputs, optional references, tags).
- **Task** — one row + setup: the concrete agent job + which criteria/metrics/pass rules apply.
- **Suite** — many tasks with a shared purpose.

Mark each suite **capability** (scoreboard / hill-climb, starts hard) or **regression** (gate, near 100%; saturated capability tasks may graduate here).

Evaluate **E2E** always; add **step / turn / intermediate** metrics only where failure modes need isolation.

**Done when:** suite purpose is clear; tasks are solvable and unambiguous (reference solution where useful); capability vs regression is labeled.

### 5. Pass rules and reporting

Define **trial success** from metric scores: binary · weighted · hybrid · partial credit. Then aggregate:

- trials → **pass@k** (≥1 success in *k*) or **pass^k** (all *k* succeed)
- suite → means, per-criterion breakdown, slices, ops (latency, tokens, cost)
- time → deltas vs baseline

**Regression → gate. Capability → scoreboard.** Trust numbers only after sampling **transcripts**. Details: [`references/pass-and-report.md`](references/pass-and-report.md).

**Done when:** success is defined before pass@k; report shows per-criterion and ops signals; gates (if any) are explicit.

### 6. Build, measure, iterate

Implement agents/tools/workflows against the suite. Improve the system; fix **eval bugs** when strong models score ~0% (often task/metric failure, not model failure). Watch **saturation**. Re-calibrate judges. Offline evals are one layer beside prod monitoring, A/B, and human review.

Binding trade-offs: [`references/constraints.md`](references/constraints.md).

**Done when:** changes are judged against the suite; regressions are visible; capability work has an unsaturated hill or a graduated regression net.

## Output expectations

When applying EDD in-session, produce artifacts in domain language where possible:

1. Guideline excerpt (should/shouldn’t + criteria)
2. Metric plan (criterion → metric(s) → score shape; rubrics for judges)
3. Business mapping notes for primary metrics
4. Suite sketch (purpose, capability vs regression, task sources, pass rules, *k*, gates vs report-only)
5. Evidence trail: which real transcripts/failures motivated each criterion in the guideline excerpt

Do not invent harness tooling choices unless asked. Do not call a criterion a task or a metric a task. Point to the transcripts that motivated each criterion — a criterion with no cited failure is a guess dressed up as a finding, and guesses are exactly what step 0 exists to avoid.
