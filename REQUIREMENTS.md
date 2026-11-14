# Requirements

Source of truth for what the system must do. Requirements are business- and system-level; concrete libraries and cloud services belong in ADRs.

**Status rule:** a box is checked only when the requirement is implemented and verified. Architecture decisions cite these IDs (for example `NFR-04`).

## Functional requirements

- [ ] **FR-01 Ingestion** — As a records administrator, I want PDF, DOCX, and scanned documents ingested with OCR fallback, so that all policy, contract, and regulatory sources are searchable, including poorly scanned originals.
- [ ] **FR-02 Adaptive chunking** — As a retrieval engineer, I want chunking to respect section hierarchy and to switch between fixed, semantic, and hybrid strategies based on document type, so that retrieved passages stay coherent, citable, and within context-token limits.
- [ ] **FR-03 Hybrid retrieval** — As an employee, I want keyword and semantic retrieval combined with a reranking step, so that exact regulatory terminology and paraphrased questions are both handled well.
- [ ] **FR-04 Permission-aware retrieval** — As an access-control owner, I want metadata filters to enforce role-based access at query time, so that the Geneva adviser can never receive Zürich private-banking documents.
- [ ] **FR-05 Grounded answers with citations** — As an employee, I want generated answers with inline citations to the source passages, so that I can verify every claim before acting on it.
- [ ] **FR-06 Insufficient-context fallback** — As a risk-aware reader, I want an explicit "confidence: insufficient context" response instead of a plausible guess, so that thin evidence never becomes fabricated policy.
- [ ] **FR-07 Provenance and audit trail** — As a compliance officer, I want every answer logged with its sources, requester, and model/prompt version, so that any answer can be reconstructed after the fact.
- [ ] **FR-08 Feedback loop** — As a reviewer, I want to mark answers helpful or not helpful, so that feedback is stored and feeds the evaluation set.

## Non-functional requirements

- [ ] **NFR-01 Latency and streaming** — P95 time-to-first-token ≤ 3 s; responses are streamed, never returned as a blocking dump.
- [ ] **NFR-02 Throughput and graceful degradation** — Per-user and per-tenant retrieval quotas, token-bucket throttling of LLM calls, and degradation to retrieval-only mode when the budget is exhausted.
- [ ] **NFR-03 Privacy and GDPR** — PII detection and redaction before embedding and before any LLM call; data residency in the EU or Switzerland.
- [ ] **NFR-04 Local and private deployment** — The design must support private or locally hosted LLM deployments and enterprise-grade vector storage for scenarios where data may not leave the institution's boundary.
- [ ] **NFR-05 EU AI Act readiness** — Transparency notice, model card, and an answer provenance log for every interaction.
- [ ] **NFR-06 Security** — Prompt-injection defenses through input/output filtering and instruction hierarchy, strict tenant isolation, and encryption of the vector store at rest.
- [ ] **NFR-07 Cost control** — Per-query token accounting, cached embeddings, and cheaper models for low-risk queries.
- [ ] **NFR-08 Context management** — Token budgets are enforced end to end, sliding-window overlap is used where document structure is weak, and grounding plus the insufficient-context fallback are the primary defenses against hallucination.

## Evaluation gate (definition of done)

The project is not done until all of the following pass on a 100-question golden set:

- [ ] **EVAL-01 Faithfulness (groundedness)** — ≥ 0.90.
- [ ] **EVAL-02 Answer relevancy** — ≥ 0.85.
- [ ] **EVAL-03 Context precision** — ≥ 0.80.
- [ ] **EVAL-04 CI regression gate** — The evaluation suite runs in CI on every prompt change, alongside a regression set built from the user feedback loop.

These map to the RAG Triad: context relevance, groundedness, and answer relevance.

## Traceability

- ADRs must cite the requirement IDs they affect.
- A requirement is not complete because an option was chosen; it is complete when the behavior is implemented and verified against the evaluation gate.
