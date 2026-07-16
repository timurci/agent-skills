# Glossary

Structural terms align with Anthropic’s agent-eval vocabulary. Domain terms are EDD product language.

## Structural

| Term | Definition |
|------|------------|
| **Evaluation (eval)** | Test of an AI system: inputs plus scoring logic. Here: automated, no real users required. |
| **Task** | One concrete job for the agent (inputs/setup + success criteria). Not a collection; not a metric. |
| **Trial** | One attempt at a task. |
| **Transcript** (trace / trajectory) | Full trial record: messages, tool calls, reasoning, intermediate results. |
| **Outcome** | Final environment state after the trial. |
| **Dataset** | Collection of rows (inputs, optional references, tags, metadata). |
| **Suite** (eval set) | Bundle of tasks for a shared purpose, with metrics and pass rules. Dataset + scoring intent → suite. |
| **Evaluation harness** | Runs evals end-to-end (tools, concurrency, recording, scoring, aggregation). |
| **Agent harness / scaffold** | Runtime that makes a model act as an agent. “The agent” ≈ model + harness. |
| **pass@k** | P(at least one success in *k* trials). Rises with *k*. One success enough. |
| **pass^k** | P(all *k* trials succeed). Falls with *k*. Reliability every time. |
| **Capability suite** | “What can it do well?” Low starting pass rate; hill to climb. |
| **Regression suite** | “Does it still work?” Near-100%; drop = break. |
| **Eval saturation** | Suite essentially solved; little improvement signal left. |

At *k* = 1, pass@k and pass^k coincide.

## Domain (EDD)

| Term | Definition |
|------|------------|
| **Guideline** | High-level doc: should/shouldn’t, good/bad; includes **criteria**. |
| **Criterion** | One dimension of good vs bad for *this* application. |
| **Metric** | How a criterion is measured → **score** (+ optional feedback). Named tracked quantity. |
| **Method** | Procedure behind a metric. Method = how; metric = tracked measurement. |
| **Rubric** | Part of a judge-style metric: scale, rules, examples for human/LLM judge. |
| **Pass rule** | How metric scores become trial success or task-level score. |
| **Report** | Aggregates (metric, task, suite, slice, time) + operational stats. |
| **Gate** | Report subset used as ship/CI criteria. Not every suite is a gate. |
| **Business mapping** | Link from eval scores → business outcomes / investment. |
| **EDD** | Define criteria and metrics (and business link) before/while building; iterate against that suite. |

### Metric kinds

- **Code / deterministic** — schema, state, tests, static analysis, justified tool constraints; pass/fail or numeric.
- **Judge** — human or LLM guided by a **rubric**.

**Grader:** optional runtime name for the adapter that applies a domain metric to a trial. Prefer **metric** in domain talk.

## Product architecture vs eval units

| Layer | Term | Meaning |
|-------|------|---------|
| Product | **Workflow** | Orchestrated multi-step process |
| Product | **Step** | One stage (LLM, agent loop, deterministic, human gate, …) |
| Product | **Agent** | Can choose actions under a harness; autonomy is a spectrum |
| Eval | **Task / trial / turn** | Agent job; one run; one loop iteration in the transcript |

A task may cover one step, several steps, or a whole workflow. One step may contain many turns.

## Quick disambiguation

| Say | Not |
|-----|-----|
| Task = one agent job | Task = criterion or entire dataset |
| Suite = tasks + purpose | Suite = unstructured rows |
| Criterion = what good means | Criterion = cosine similarity |
| Metric = how we measure | “Metric” as every number without context |
| Rubric ⊂ judge metric | Rubric unrelated to measurement |
| pass@k over trial success | pass@k without a success definition |
| Regression = gate; capability = scoreboard | Every suite gates CI the same way |
