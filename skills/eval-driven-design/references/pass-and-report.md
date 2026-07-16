# Pass rules and reporting

## Pass rules (trial / task level)

| Mode | Meaning |
|------|---------|
| **Binary** | All required metrics pass → trial success |
| **Weighted** | Combined scores must meet a threshold |
| **Hybrid** | Hard gates (safety, schema, policy) + soft quality scores |
| **Partial credit** | Multi-part tasks expose a continuum |

Define **trial success** first. **pass@k** / **pass^k** only summarize that binary over *k* trials. Continuous metrics need a threshold to count as success, or stay as mean/distribution reports.

## Reliability summaries

| Measure | Question | *k* effect |
|---------|----------|------------|
| **pass@k** | ≥1 success in *k* trials? | Score rises with *k* |
| **pass^k** | All *k* succeed? | Score falls with *k* |

- Coding / search where retries are OK → often **pass@k** (and **pass@1** for first-try UX).  
- User-facing reliability → **pass^k**.  
- Always report **pass@1** (or mean per-trial success) for comparability.

## Trusting the numbers

- State the number of trials *k* **and** why it's enough to see the effect size you care about; *k*=3 hides more noise than it resolves.
- Report a confidence interval or variance alongside every pass@k/pass^k and every delta vs. baseline — a delta without a noise floor is not a finding.
- Before gating a regression suite on a drop, check it against normal run-to-run variance — stochastic trials wobble on their own, and gating on a single re-run risks blocking a ship over noise rather than a real break.

## Aggregation ladder

```text
Metric on one trial
  → pass rule → trial success / task score
  → across k trials → pass@k, pass^k, mean, variance
  → across suite → means, histograms, % tasks reliable
  → over time / PRs / models → deltas vs baseline
```

## What a report should show

- pass@1; pass@k and/or pass^k as product requires  
- Soft metric means/distributions; pass rate at threshold τ  
- **Per-criterion** breakdown (not only one blended score)  
- **Slices** (locale, intent, difficulty, …)  
- **Operational:** turns, tool calls, tokens, latency (p50/p95), cost  
- **Delta vs baseline** for CI and model upgrades  

## Suites vs gates

| Suite type | Role | CI habit |
|------------|------|----------|
| **Capability** | Scoreboard; hill to climb | Report; don’t demand max every PR |
| **Regression** | Guardrail; near 100% | Gate on drops / blocker tasks; enforce $ and latency budgets |

## Vs classic software tests

- Stochastic → *k* trials, not one deterministic run  
- Graded scores and thresholds, not only asserts  
- Scoreboards and gates, not every suite failing the build the same way  
- Transcript review required to trust aggregates  
- Cost/latency first-class beside quality  

## Trust checks

- Sample transcripts when scores move or stall.  
- ~0% on strong models across many trials → suspect task/metric bugs.  
- Suite at ~100% capability → saturated; harden tasks or graduate to regression.
