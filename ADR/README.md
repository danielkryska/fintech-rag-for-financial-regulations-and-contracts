# Architecture Decision Records

The list of high-level architecture decisions for this project. Each ADR records one platform-agnostic decision, the options considered, the well-architected trade-offs, and the consequences accepted.

ADRs are for decisions that change the flow or create lasting commitment: retrieval architecture, grounding and citation model, tenancy and permissions, audit, evaluation, deployment topology class, a major library class, a SaaS category. Implementation detail and specific cloud service choices belong in the C4 drawings in [c4-architecture/](../c4-architecture/), not here.

## Index

| ADR | Decision | Scope | Status | Date |
| --- | --- | --- | --- | --- |

_No decisions yet. Run `/create-adr` to start._

## Conventions

- Create ADRs only through `/create-adr`. Do not write or edit an ADR directly.
- One decision per file: `NNNN-short-kebab-title.md`.
- Numbers are sequential, four digits, and never reused. The command takes the highest existing number plus one.
- Status values: `Proposed`, `Accepted`, `Superseded by ADR-NNNN`, `Deprecated`.
- High-level ADRs use `Scope: Cross-cutting`. Platform-specific service choices are recorded in the C4 Level 3 drawings and their notes, not as high-level ADRs.
- Accepted ADRs are immutable. Reverse or change a decision with a new ADR that supersedes the old one.
- Reference requirement IDs from [REQUIREMENTS.md](../REQUIREMENTS.md).
- Every ADR includes a `## Well-architected assessment` covering operational excellence, security, reliability, performance efficiency, cost optimization, and sustainability, plus a `## Simplification check`. Mark a pillar `N/A` with a reason; do not omit it.
- Material gaps found during the assessment become follow-ups with a severity and owner.
- The ADR template lives in [.claude/commands/create-adr.md](../.claude/commands/create-adr.md). There is deliberately no separate template file.
- The command updates this index and the decision register in [ARCHITECTURE.md](../ARCHITECTURE.md) in the same change that adds an ADR.

## Drawings

C4 diagrams do not live in this folder. They are owned by `/create-c4` and stored in [c4-architecture/](../c4-architecture/) as draw.io XML, following the standard in [.claude/commands/create-c4.md](../.claude/commands/create-c4.md).

- A high-level, system-wide ADR links the confirmed C4 Level 1 or Level 2 drawing it explains once `/create-c4` has produced it (for example `step3_lvl2_v4_retrieve-generate-stream.drawio`). If none exists yet, the ADR names the drawing `/create-c4` must create. Do not embed C4 XML in the ADR.
- A non-C4 decision sketch may be inline in the ADR as a fenced `xml` block containing a complete `<mxfile>` document, or a sidecar `NNNN-<drawing-name>.xml` linked from the ADR, with a render `NNNN-<drawing-name>.png` only when it exists.
- Never commit a PNG without its XML source or claim a render that does not exist.
- C4 Level 3 drawings are platform-specific. They live in `c4-architecture/`, are named `lvl3_v<K>_<technology>_<drawing_name>.drawio`, and are produced by the platform architect after Levels 1 and 2 are confirmed. `/create-adr` does not create them.

## Who owns ADRs

- `/create-adr` — creates high-level, platform-agnostic ADRs and runs the full create → review → fix loop.
- `/create-c4` — owns C4 Levels 1 and 2, the draw.io standard, the `c4-reviewer` loop, the user confirmation gate, and the C4 index.
- `adr-reviewer` — read-only review of ADRs, invoked by `/create-adr` at every round.
- `c4-reviewer` — read-only review of C4 drawings, invoked by `/create-c4`.
- `architect-aws`, `architect-azure`, `architect-k8s` — platform advice and C4 Level 3 drawings. They do not create or edit high-level ADRs, Level 1, or Level 2.

The platform architects also advise: they review the current design against their platform well-architected framework, find gaps, propose simplifications, and assess security, cost, reliability, operations, performance, and sustainability. Findings that require a high-level choice are routed back to `/create-adr`; the rest become follow-ups.

## Review gate

`/create-adr` loops with `adr-reviewer` until no **Blocking** or **Major** findings remain. Minor findings can be fixed, recorded as follow-ups, or waived by the user. Only then does the command ask for acceptance; the status becomes `Accepted` only with explicit user approval.

C4 drawings have a separate gate in `/create-c4`: `c4-reviewer` (mechanical checklist and semantic review), fix loop, then explicit user confirmation. The reviewer's `Accept` is not user confirmation.
