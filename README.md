# Fintech RAG for Financial Regulations and Contracts

**This is a showcase repository: a portfolio-grade demonstration of production-depth RAG, not a production system and not affiliated with any institution. All documents and data used here are synthetic.**

This project explores what it actually takes to run *RAG* (retrieval-augmented generation) for a regulated financial institution. The scenario: a **Swiss private bank or insurance group** needs an internal assistant that answers employee questions across **50,000+ policy PDFs, scanned contracts, and regulatory circulars**. Access must be **strict** (an adviser in Geneva must never retrieve Zürich private-banking documents), **every answer must cite its source passages**, and **every answer must leave an audit trail**. The keyword search used today returns too many false positives and offers **no traceable reasoning**.

The repository covers the full path from document ingestion to a governed answer: *OCR* and parsing, adaptive chunking, *hybrid retrieval* with permission-aware filtering, grounded generation with *inline citations*, evaluation discipline, and the **compliance, latency, and cost controls** that separate a demo from a system a bank could operate. It is intended to demonstrate **RAG at production depth (not toy depth)**, large-file handling, evaluation discipline, compliance thinking, and reasoning about *QPS* and cost in AI systems.

## Start here

| Document | What it covers |
| --- | --- |
| **[ADR/README.md](ADR/README.md)** | **The list of architecture decisions. Start here for decisions.** |
| [REQUIREMENTS.md](REQUIREMENTS.md) | Functional and non-functional requirements, with completion checkboxes. |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System-wide architecture summary and the decision register. |
| [c4-architecture/](c4-architecture/README.md) | C4 architecture drawings and business flows (draw.io XML), including Level 3 platform realisations. |
| [src/README.md](src/README.md) | Planned application layout. |
| [infra/README.md](infra/README.md) | Planned infrastructure layout. |
| [AGENTS.md](AGENTS.md) | How AI agents work in this repository. |

## C4 architecture

The architecture follows the C4 model. All drawings are draw.io XML sources; the drawing standard, index, and review process live in [c4-architecture/README.md](c4-architecture/README.md). GitHub does not render `.drawio` files inline — open them in [diagrams.net](https://app.diagrams.net) (File → Open from → URL, with the file's raw link) or with the VS Code drawio extension. To show a diagram inline in this README, commit a PNG or SVG export next to its `.drawio` source.

| Title | Description | URL |
| --- | --- | --- |
| System context (Level 1, v3) | Who uses the assistant and which external systems it depends on | [lvl1_v3_system_context.drawio](c4-architecture/lvl1_v3_system_context.drawio) |
| Document ingestion (Level 2 step 1, v6) | Upload, registration, hierarchical chunking, and the hand-off to embedding | [step1_lvl2_v6_document-ingestion.drawio](c4-architecture/step1_lvl2_v6_document-ingestion.drawio) |
| Embed and index (Level 2 step 2, v2) | Event-driven embedding and index writes to the vector DB, keyword index, and chunk store | [step2_lvl2_v2_embed-and-index.drawio](c4-architecture/step2_lvl2_v2_embed-and-index.drawio) |
| Retrieve, generate, cite, stream, authorize (Level 2 step 3, v4) | The question and answer path: retrieval, reranking, generation, citations, and SSE streaming | [step3_lvl2_v4_retrieve-generate-stream.drawio](c4-architecture/step3_lvl2_v4_retrieve-generate-stream.drawio) |
| Stream and authorize (Level 2 step 4, v1) | Query workers, answer events, and SSE streaming to the browser | [step4_lvl2_v1_stream-and-authorize.drawio](c4-architecture/step4_lvl2_v1_stream-and-authorize.drawio) |
| Project walkthrough (PDF) | Hand-drawn flows and the project walkthrough used as drawing input | [project 1 - rag knowledge assistant fo regulation docs-2026-11-14-19-06.pdf](c4-architecture/project%201%20-%20rag%20knowledge%20assistant%20fo%20regulation%20docs-2026-11-14-19-06.pdf) |

## Showcase

_To be added: demo video or GIF, screenshots of the assistant with inline citations, a sample insufficient-context response, the evaluation dashboard, and benchmark results for latency, retrieval quality, and cost._

## License

Released under the [MIT License](LICENSE).
