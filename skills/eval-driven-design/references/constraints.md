# Constraints and trade-offs

Binding limits when applying EDD:

1. **Proxy risk** — Eval metrics ≠ business metrics until **business mapping** is explicit and periodically validated in production.  
2. **Coverage vs cost** — Step/turn metrics help debug and cost maintenance. E2E always; intermediate only for hot failure modes.  
3. **Composite vs split** — Joint scores for ship decisions; split metrics for diagnosis.  
4. **Path vs outcome** — Full path checks punish valid solutions; under-specified process misses policy/tool abuse. Gate outcomes + *necessary* constraints.  
5. **Judge validation** — Rubrics need examples and human calibration, *and*:
   - Measure the judge's agreement rate (precision/recall, or Cohen's kappa) against a human-labeled gold set before trusting it at scale.
   - Watch for self-preference bias: a judge model scoring outputs from the same or a closely related model tends to rate them favorably. Prefer a different model family as judge, or validate against humans specifically on this axis.
   - Watch for position/verbosity bias in pairwise or long-output judging; rotate order and don't let length stand in for quality.
   - Re-run judge-human agreement checks whenever the rubric, the judge model, or the task distribution changes — a calibrated judge doesn't stay calibrated forever.
6. **Task quality** — Ambiguous tasks and buggy metrics masquerade as model failure.  
7. **Saturation** — ~100% capability suite is a regression net, not an improvement signal.  
8. **TDD analogy limit** — Same discipline (success first); not the same determinism or unit under test.  
9. **Swiss cheese** — Offline evals alone are insufficient; combine with prod monitoring, A/B, feedback, transcript review, human studies as needed.
10. **Eval set staleness (Goodhart's law)** — A static eval set that never changes becomes a target the team optimizes to, not a proxy for real quality. Periodically inject new tasks from fresh production data and hold out some tasks from active optimization to catch overfitting to the suite itself.

## Parked (not specified by this skill)

- Exact CI thresholds and *k* per product  
- Formality bar for “investment-grade” business mapping  
- Whether safety/policy is its own criterion family  
- Code interfaces for metrics  
- Choice of harness/framework products  
