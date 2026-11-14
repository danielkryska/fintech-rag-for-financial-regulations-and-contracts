# Low-level architectures

Platform-neutral component- and module-level designs for the ingestion, retrieval, generation, evaluation, and audit paths, including their interfaces.

## What belongs here

- Platform-neutral component diagrams and interface contracts.
- Data flow within a module.
- Failure, retry, and degradation paths.
- Capacity and scaling notes tied to requirements.

Not here: platform-specific C4 Level 3 diagrams (see the [AWS](../aws/README.md), [Azure](../azure/README.md), and [Kubernetes](../k8s/README.md) folders), decisions and alternatives (see [ADRs](../../ADR/README.md)), or requirements (see [REQUIREMENTS.md](../../REQUIREMENTS.md)).

## Naming

- `<component>-<name>.xml` plus `<component>-<name>.png`.
- If a drawing explains a specific decision, use `NNNN-<name>.xml` and `NNNN-<name>.png` in the ADR folder and link it from the ADR.

## Index

_To be added._
