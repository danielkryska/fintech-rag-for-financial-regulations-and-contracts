# AWS architecture

Service mapping and C4 Level 3 diagrams for the AWS deployment target. High-level decisions are recorded in the [ADR index](../../ADR/README.md); platform-specific service choices and component designs are documented here.

## Scope

- Model access: Amazon Bedrock, SageMaker, or external model APIs; embeddings and reranker.
- Retrieval and storage: Amazon OpenSearch, Aurora PostgreSQL with pgvector, or an external vector store; S3 layout.
- Parsing and OCR: Amazon Textract or self-managed libraries.
- Runtime: ECS or EKS, Lambda, Step Functions, SQS, streaming response path.
- Identity and security: IAM, Cognito, KMS, VPC endpoints, WAF, Secrets Manager.
- Residency and compliance: EU or Swiss regions, data classification, retention, CloudTrail, S3 Object Lock.

## Well-architected review

Reviews use the six AWS Well-Architected Framework pillars: operational excellence, security, reliability, performance efficiency, cost optimization, and sustainability. Ask `architect-aws` for an advisory review to find gaps, simplifications, security issues, and cost drivers. Findings that require a high-level choice are routed to `/create-adr`; the rest become follow-ups.

## C4 Level 3 diagrams

`architect-aws` produces component-level diagrams for this target. Naming: `c4-l3-<container>-<name>.xml` plus `.png`. Link each diagram here and from the ADR it explains.

| Container | Diagram | ADR | Status |
| --- | --- | --- | --- |

_None yet. The platform architect adds these after the relevant ADRs are accepted._

## Decisions

High-level decisions are in the [ADR index](../../ADR/README.md). Run `/create-adr`; do not write ADRs here.

## Open decisions

The authoritative list is the [open decisions table](../../ARCHITECTURE.md#open-decisions) in `ARCHITECTURE.md`. Do not record a decision here; link to its ADR.
