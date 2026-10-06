# Agent Skills

This repository is a collection of custom agent skills.

Each skill lives under `skills/` and follows the standard skill layout:

```text
skills/
└── skill-name/
    ├── SKILL.md
    └── references/
```

## Skills

- `agents-md-writer` - guidance for creating, reviewing, and improving `AGENTS.md` files for AI coding agents.
- `ai-architecture` - domain-driven design and clean/hexagonal architecture for LLM-based Python systems: layering, ports, adapters, use-case boundaries, and the `RAGService` monolith smell.
- `brainstorm` - a process for open-ended or uncertain problems.
- `eval-driven-design` - specify success before building: criteria, metrics, suites, pass rules, and reporting for non-deterministic systems.
- `python-tdd` - test-driven development for Python changes: writing the test first, reproducing a bug with a test, and deciding whether a change needs tests.
- `visual-explainer` - a topic, dataset, or paper turned into a designed visual page: a single-image infographic or one-pager, or a multi-section explainer with diagrams, charts, and math, themed by an optional brand style layer.

## Navigation

Open a skill's `SKILL.md` for its main instructions. Supporting material that should only be loaded when relevant lives in that skill's `references/`, `scripts/`, or `assets/` directories.
