# Fintech RAG for Financial Regulations and Contracts

**This is a showcase repository: a portfolio-grade demonstration of production-depth RAG, not a production system and not affiliated with any institution. All documents and data used here are synthetic.**

This project explores what it actually takes to run retrieval-augmented generation for a regulated financial institution. The scenario: a Swiss private bank or insurance group needs an internal assistant that answers employee questions across 50,000+ policy PDFs, scanned contracts, and regulatory circulars. Access must be strict (an adviser in Geneva must never retrieve Zürich private-banking documents), every answer must cite its source passages, and every answer must leave an audit trail. The keyword search used today returns too many false positives and offers no traceable reasoning.

The repository covers the full path from document ingestion to a governed answer: OCR and parsing, adaptive chunking, hybrid retrieval with permission-aware filtering, grounded generation with inline citations, evaluation discipline, and the compliance, latency, and cost controls that separate a demo from a system a bank could operate. It is intended to demonstrate RAG at production depth (not toy depth), large-file handling, evaluation discipline, compliance thinking, and reasoning about QPS and cost in AI systems.

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

## Showcase

_To be added: demo video or GIF, screenshots of the assistant with inline citations, a sample insufficient-context response, the evaluation dashboard, and benchmark results for latency, retrieval quality, and cost._

## License

Released under the [MIT License](LICENSE).
