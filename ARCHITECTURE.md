# Architecture

System-wide architecture overview for the Fintech RAG showcase. **ADRs are the source of truth for decisions.** This document summarizes them and links out; it must never introduce a decision that is not recorded in an ADR.

## Document map

| Document | Role |
| --- | --- |
| [REQUIREMENTS.md](REQUIREMENTS.md) | What the system must do; checked only when implemented and verified. |
| [ADR/README.md](ADR/README.md) | Index of architecture decisions, one per file. |
| [c4-architecture/](c4-architecture/README.md) | C4 drawings and business flows (draw.io XML), the drawing standard, the index, and Level 3 platform realisations. |
| [infra/README.md](infra/README.md) | Infrastructure-as-code layout. |
| [src/README.md](src/README.md) | Application layout. |

## System summary

A governed retrieval-augmented generation pipeline. Documents are ingested, parsed with OCR fallback, redacted, chunked, and indexed with permission metadata. Questions are redacted, retrieved with hybrid search, permission-filtered, reranked, and answered with inline citations or an explicit insufficient-context response. Every interaction is audited and feeds evaluation. The required behavior and quality gates are in [REQUIREMENTS.md](REQUIREMENTS.md).

The system must be deployable on three targets: AWS, Azure, and Kubernetes / portable. The platform-specific realisations will be recorded as C4 Level 3 drawings in [c4-architecture/](c4-architecture/README.md), named `lvl3_v<K>_<aws|azure|k8s>_<drawing_name>.drawio` and produced by the matching platform architect after Levels 1 and 2 are confirmed.

## Architectural constraints

These come from requirements, not from an ADR. They constrain every decision:

- Permission-aware retrieval at query time (FR-04).
- Inline citations and an explicit insufficient-context fallback (FR-05, FR-06).
- Reconstructable audit trail (FR-07).
- PII redaction before embedding and before any model call; EU or Swiss residency (NFR-03).
- Support for private or locally hosted models and vector storage (NFR-04).
- P95 time-to-first-token ≤ 3 s with streaming (NFR-01); graceful degradation when budgets are exhausted (NFR-02).
- Per-query token and cost accounting, cached embeddings (NFR-07).
- End-to-end context budgets (NFR-08).
- EU AI Act transparency and provenance (NFR-05).
- Prompt-injection defenses and strict tenant isolation (NFR-06).

## Well-architected lens

Every target is reviewed against its platform framework: the **AWS Well-Architected Framework**, the **Azure Well-Architected Framework**, and the adapted cloud-native pillars for **Kubernetes**. The shared lens covers six quality areas:

- Operational excellence
- Security
- Reliability
- Performance efficiency
- Cost optimization
- Sustainability

AWS treats all six as framework pillars. Azure treats the first five as framework pillars and sustainability as an additional design consideration. The Kubernetes target adapts all six to cloud-native practice.

The platform architects advise on their target. They review existing designs, find architecture gaps, propose simplifications, and assess security, reliability, cost, operations, performance, and sustainability. They do not create or edit high-level ADRs; `/create-adr` owns those. Every ADR records a pillar-by-pillar impact assessment and a simplification check. `adr-reviewer` checks coverage before acceptance, `c4-reviewer` checks the C4 drawings, and `/documentation` checks the documents and indexes across the set.

## Decision register

Every accepted decision is recorded in [ADR/](ADR/README.md) through `/create-adr`. This register mirrors the index; the ADR file is authoritative.

| ADR | Decision | Scope | Status | Date |
| --- | --- | --- | --- | --- |

_No decisions yet. Run `/create-adr` to start._

## Open decisions

Tracked but not yet decided. Each high-level decision is resolved through `/create-adr`; a working preference is not a decision. C4 Levels 1 and 2 are drawn with `/create-c4`; Level 3 is drawn by the platform architects after the high-level ADRs and Levels 1 and 2 are confirmed.

| Area | Targets | Owner | Status |
| --- | --- | --- | --- |
| Model and embedding provider | AWS, Azure, Kubernetes | `/create-adr` | Open |
| Retrieval engine and vector store | AWS, Azure, Kubernetes | `/create-adr` | Open |
| Document parsing and OCR | AWS, Azure, Kubernetes | `/create-adr` | Open |
| API, orchestration, and streaming runtime | AWS, Azure, Kubernetes | `/create-adr` | Open |
| Identity, tenancy, and permission enforcement | AWS, Azure, Kubernetes | `/create-adr` | Open |
| Audit, observability, and retention | AWS, Azure, Kubernetes | `/create-adr` | Open |
| Infrastructure as code and deployment topology | AWS, Azure, Kubernetes | `/create-adr` | Open |
| Evaluation harness and CI gate | Cross-cutting | `/create-adr` | Open |
| Guardrails and prompt-injection defenses | Cross-cutting | `/create-adr` | Open |

## Process models

End-to-end business flows will be expressed in the confirmed C4 Level 2 slice drawings in [c4-architecture/](c4-architecture/README.md). Each line is a step in the flow and each business block lists the actions it performs.

## Architecture views

- All C4 drawings live in [c4-architecture/](c4-architecture/README.md) as draw.io XML. The standard, naming, index, and review gate are defined there.
- C4 Level 1 (system context) and Level 2 (containers and business-flow slices) are system-wide and platform-agnostic. They are drawn by `/create-c4` and tied to the ADRs that explain them.
- C4 Level 3 (platform realisation) is platform-specific. The matching platform architect draws it after Levels 1 and 2 are confirmed; `/create-c4` runs `c4-reviewer` and the user confirmation gate. File naming is `lvl3_v<K>_<aws|azure|k8s>_<drawing_name>.drawio`.
- C4 Level 4 (code) is out of scope; the code documents itself.

## Changing the architecture

1. Run `/create-adr` for the high-level decision. It interviews, presents options, writes the ADR, and runs the review/fix loop with `adr-reviewer`.
2. Answer its questions and choose an option. The command asks which review findings to fix and repeats until no Blocking or Major findings remain.
3. Accept explicitly; the command sets the status and syncs the ADR index and decision register.
4. If the decision changes the design, run `/create-c4` to revise the affected Level 1 or Level 2 drawing. After those are confirmed, `/create-c4` invokes the matching platform architect for the Level 3 realisation.
5. Run `/documentation` to check every Markdown file, the ADR indexes, and the C4 index for contradictions.
6. An accepted ADR is immutable; change it only through a superseding ADR created by `/create-adr`.

If documents disagree, the ADR wins and the other document is corrected. If an ADR is wrong, stop and propose a superseding ADR.
