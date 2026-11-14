# Source

Application code for the RAG assistant.

## Planned layout

```
src/
├── api/           # HTTP API, streaming responses, authentication context
├── ingestion/     # Parsing, OCR fallback, PII redaction, adaptive chunking
├── retrieval/     # Hybrid search, reranking, permission filtering
├── generation/    # Prompting, grounded answers, citations, fallbacks
├── evaluation/    # Golden set, RAG Triad metrics, CI regression suite
└── observability/ # Audit log, token accounting, tracing
```

Behavior is specified in [REQUIREMENTS.md](../REQUIREMENTS.md). Architecture decisions that shape this layout are recorded in [ADR/README.md](../ADR/README.md).

_Contents to be added._
