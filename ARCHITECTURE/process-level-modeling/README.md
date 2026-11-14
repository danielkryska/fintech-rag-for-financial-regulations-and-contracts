# Process-level modeling

The system is modeled as two high-level processes: one for bringing documents in, one for answering questions under governance.

These diagrams describe required behavior from [REQUIREMENTS.md](../../REQUIREMENTS.md). They do not record architecture decisions; those live in [ADRs](../../ADR/README.md).

## Ingestion process

```mermaid
flowchart LR
    A[Document sources<br/>PDF · DOCX · scans] --> B[Parse / OCR fallback]
    B --> C[PII detection & redaction]
    C --> D[Adaptive chunking<br/>hierarchy · semantic · fixed]
    D --> E[(Indexes<br/>vector + keyword<br/>ACL metadata attached)]
```

## Query and answer process

```mermaid
flowchart LR
    Q[Employee question] --> R[Query preprocessing<br/>PII redaction · entitlement lookup]
    R --> S[Hybrid retrieval<br/>keyword + semantic]
    E[(Permission-scoped index)] --> S
    S --> T[Rerank + metadata filter]
    T --> U{Sufficient context?}
    U -- yes --> V[Grounded answer<br/>with inline citations]
    U -- no --> W[Confidence: insufficient context]
    V --> X[(Audit log<br/>sources · provenance · token accounting)]
    W --> X
    V --> Y[User feedback]
    Y --> Z[(Evaluation set<br/>RAG Triad · regression CI)]
    Z -.-> T
```

## To be added

- Swimlane detail for both processes, including ownership per step.
- Exception paths: OCR failure, poisoned or malformed document, retrieval outage, model timeout, budget exhaustion, permission-denied query.
- Retry, escalation, and dead-letter handling.
- Editable draw.io versions: `<topic>-<name>.xml` with `<topic>-<name>.png` renders, per the [drawing conventions](../README.md#drawing-conventions).
