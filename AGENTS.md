# Agents

Project guidance for AI agents. This file routes; detailed content lives in the linked documents.

## Read first

1. [REQUIREMENTS.md](REQUIREMENTS.md) — what must be true. Check a box only when implemented and verified.
2. [ARCHITECTURE.md](ARCHITECTURE.md) — current architecture summary and open decisions.
3. [ADR/README.md](ADR/README.md) — the decision index. ADRs are the source of truth.
4. [c4-architecture/README.md](c4-architecture/README.md) — the C4 drawing standard, index, and Level 3 checklist.

## Rules

- Use `/create-adr` for every high-level architecture decision. The command owns the ADR template, the reviewer/fix loop, and the index updates. Do not write or edit an ADR directly.
- Use `/create-c4` for every C4 drawing. The command owns the level sequence, the draw.io standard, the validator run, the `c4-reviewer` fix loop, the user confirmation gate, and the index updates. Do not write C4 XML directly.
- `/create-c4` is platform-agnostic for Levels 1 and 2. Platform architects (`architect-aws`, `architect-azure`, `architect-k8s`) create Level 3 drawings for their platform after Levels 1 and 2 are confirmed. They do not create Levels 1 or 2 and do not edit ADRs.
- All C4 drawings are draw.io XML in [c4-architecture/](c4-architecture/README.md). Never use another diagram format. Never create an `ARCHITECTURE/` folder.
- Drawing non-negotiables: at Levels 2 and 3, three bands (Representation on top, Business logic in the middle, Repository on the bottom); at Level 1, top-down actors → one own-system black box → external systems. No line intersections, every line labelled with what happens, communication types in `[]` at all levels, queues/streams/brokers on lines instead of boxes, generic technology categories only at Level 2, specific technologies and complete infrastructure at Level 3.
- A C4 level is confirmed only after `/create-c4` runs `c4-reviewer` to no Blocking or Major findings and the user explicitly approves. Do not mark a drawing `Confirmed` otherwise.
- At the end of every command or task that changes a Markdown file, run `/documentation` in fix mode and resolve its findings before finishing. No command or task is complete until the documentation pass is clean.
- Never invent a decision. Synthetic data only; no secrets, credentials, or real personal data.
- Do not mark a requirement checked without implementation and verification.

## Commands and agents

- `/create-adr` — creates the high-level, platform-agnostic ADR, invokes `adr-reviewer`, asks which findings to fix, applies them, re-reviews, and repeats until no Blocking or Major findings remain. Only then does it ask for acceptance.
- `/create-c4` — creates one C4 drawing or the next level, runs the draw.io validator, invokes `c4-reviewer`, asks which findings to fix, re-reviews, and asks the user to confirm. Only then does it move to a lower level.
- `c4-reviewer` — read-only review of C4 drawings. It blocks confirmation on Blocking or Major findings.
- `architect-aws`, `architect-azure`, `architect-k8s` — platform advice and Level 3 drawings. They work from accepted ADRs and confirmed Levels 1 and 2, and do not change them.
- `/documentation` — consistency pass over every Markdown file, the ADR indexes, and the C4 index.
