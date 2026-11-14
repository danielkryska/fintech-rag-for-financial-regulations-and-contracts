# Azure architecture

Service mapping and C4 Level 3 diagrams for the Azure deployment target. High-level decisions are recorded in the [ADR index](../../ADR/README.md); platform-specific service choices and component designs are documented here.

## Scope

- Model access: Azure OpenAI Service, Azure AI Foundry models, or external model APIs; embeddings and reranker.
- Retrieval and storage: Azure AI Search, PostgreSQL with pgvector on Azure, or an external vector store; Blob Storage layout.
- Parsing and OCR: Azure AI Document Intelligence or self-managed libraries.
- Runtime: Azure Container Apps, AKS, Functions, Service Bus, Event Grid, streaming response path.
- Identity and security: Microsoft Entra ID, managed identities, Key Vault, private endpoints, API Management, WAF.
- Residency and compliance: EU or Swiss regions, data classification, retention, Log Analytics, immutable blob storage.

## Well-architected review

Reviews use the five Azure Well-Architected Framework pillars: reliability, security, cost optimization, operational excellence, and performance efficiency, with sustainability as an additional design consideration. Ask `architect-azure` for an advisory review to find gaps, simplifications, security issues, and cost drivers. Findings that require a high-level choice are routed to `/create-adr`; the rest become follow-ups.

## C4 Level 3 diagrams

`architect-azure` produces component-level diagrams for this target. Naming: `c4-l3-<container>-<name>.xml` plus `.png`. Link each diagram here and from the ADR it explains.

| Container | Diagram | ADR | Status |
| --- | --- | --- | --- |

_None yet. The platform architect adds these after the relevant ADRs are accepted._

## Decisions

High-level decisions are in the [ADR index](../../ADR/README.md). Run `/create-adr`; do not write ADRs here.

## Open decisions

The authoritative list is the [open decisions table](../../ARCHITECTURE.md#open-decisions) in `ARCHITECTURE.md`. Do not record a decision here; link to its ADR.
