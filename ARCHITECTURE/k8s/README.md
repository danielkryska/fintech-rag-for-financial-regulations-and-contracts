# Kubernetes and portable architecture

Service mapping and C4 Level 3 diagrams for the portable target: Kubernetes on a provider, on-premises, or in a private cloud. High-level decisions are recorded in the [ADR index](../../ADR/README.md); platform-specific service choices and component designs are documented here.

## Scope

- Model serving: vLLM, Text Generation Inference, Ollama, KServe, or Ray Serve; GPU scheduling.
- Retrieval and storage: Qdrant, Milvus, Weaviate, pgvector, or self-hosted OpenSearch; S3-compatible object storage.
- Packaging and scaling: Helm or Kustomize, HPA, KEDA, PodDisruptionBudgets, NetworkPolicies.
- Identity and policy: Keycloak or another OIDC provider, mTLS and service mesh, OPA Gatekeeper or Kyverno.
- External SaaS: managed model APIs, managed vector stores, and other third-party services used by the portable target.
- Operations: OpenTelemetry, Prometheus, Grafana, Loki, immutable audit storage, backup and restore.

## Well-architected review

Reviews use six pillars adapted from the cloud well-architected frameworks and the cloud-native principles behind Kubernetes production readiness: operational excellence, security, reliability, performance efficiency, cost optimization, and sustainability. Ask `architect-k8s` for an advisory review to find gaps, simplifications, security issues, and cost drivers. Findings that require a high-level choice are routed to `/create-adr`; the rest become follow-ups.

## C4 Level 3 diagrams

`architect-k8s` produces component-level diagrams for this target. Naming: `c4-l3-<container>-<name>.xml` plus `.png`. Link each diagram here and from the ADR it explains.

| Container | Diagram | ADR | Status |
| --- | --- | --- | --- |

_None yet. The platform architect adds these after the relevant ADRs are accepted._

## Decisions

High-level decisions are in the [ADR index](../../ADR/README.md). Run `/create-adr`; do not write ADRs here.

## Open decisions

The authoritative list is the [open decisions table](../../ARCHITECTURE.md#open-decisions) in `ARCHITECTURE.md`. Do not record a decision here; link to its ADR.
