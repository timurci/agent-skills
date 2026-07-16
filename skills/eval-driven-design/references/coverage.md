# Coverage: structural axes and criterion families

Two taxonomies. **Axes** describe how measurement is built. **Families** checklist *what qualities* to cover. Metrics need not map 1:1 to families.

## Structural axes

1. **Unit under test** — model · model + harness · full product surface  
2. **Interaction structure** — single-turn · multi-turn · long-horizon  
3. **Object of judgment** — transcript · outcome · both  
4. **Metric modality** — code · model · human  
5. **Success semantics** — binary · weighted · hybrid · partial credit  
6. **Purpose** — capability · regression · calibration  
7. **Reliability framing** — single-shot · pass@k · pass^k  
8. **Agent / domain type** — coding · conversational · research · computer-use · …  
9. **Signal source** — offline evals · prod monitoring · A/B · human review  
10. **Specification hardness** — exact match → rubric → open-ended expert judgment  
11. **Task provenance** — real production traffic · synthetic · hand-authored · hybrid. Prefer real traffic where available; synthetic tasks need explicit validation that they resemble real failure modes, not just plausible-sounding ones.

Defaults that usually hold:

- Prefer **outcome** grading over rigid full paths (unless process is the product).  
- Prefer **code** metrics where possible; **judges** where necessary; **humans** for gold standard and calibration.

## Criterion families (coverage checklist)

1. **Domain / cognitive** — understanding, reasoning, knowledge in the domain  
2. **Generation quality** — fluency, coherence, factual consistency, faithfulness, relevance, voice, safety-in-output, …  
3. **Instruction following** — schema, keywords, forbidden content, language, format, constraints  
4. **Operational** — cost, latency, tokens, efficiency  

Agentic turns often hit several families at once (reason + tools + format + answer). Use families to ask “did we forget safety/ops/IF?” — not to force one module per family.

**Composite metrics** (one score spanning many criteria) suit ship/no-ship; split metrics when you need diagnosis.

## Where to attach metrics

| Level | Use |
|-------|-----|
| **E2E** | Always — business-shaped outcomes |
| **Step / intermediate** | When a stage has independent failure modes worth isolating |
| **Turn** | When interaction quality or loop behavior is the product |

Exhaustive per-node metrics are a maintenance tax; pragmatism is part of EDD.
