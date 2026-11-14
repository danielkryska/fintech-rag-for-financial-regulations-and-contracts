# Architecture drawings and target detail

This folder holds the architecture drawings and per-target detail. High-level decisions and rationale live in [ADRs](../ADR/README.md); this folder shows the resulting design.

## Layout

| Folder | Contents |
| --- | --- |
| [aws/](aws/README.md) | AWS target diagrams, service mapping, and C4 Level 3 components. |
| [azure/](azure/README.md) | Azure target diagrams, service mapping, and C4 Level 3 components. |
| [k8s/](k8s/README.md) | Kubernetes and portable target diagrams and C4 Level 3 components. |
| [process-level-modeling/](process-level-modeling/README.md) | End-to-end process flows, swimlanes, and exception paths. |
| [low-level-architectures/](low-level-architectures/README.md) | Component- and module-level designs that are not platform-specific. |

## C4 model

- **Level 1 (system context)** and **Level 2 (containers)** are system-wide. They are tied to the ADRs that explain them.
- **Level 3 (components)** is platform-specific. The platform architects (`architect-aws`, `architect-azure`, `architect-k8s`) produce these from accepted ADRs. One container per diagram.
- **Level 4 (code)** is out of scope; the code documents itself.

C4 Level 3 naming: `c4-l3-<container>-<name>.xml` plus `c4-l3-<container>-<name>.png`, stored in the target folder. Link each diagram from the target README and from the ADR it explains.

## Drawing conventions

- The editable source is draw.io XML: `<topic>-<name>.xml`.
- The render is `<topic>-<name>.png`, stored next to the source.
- If a drawing illustrates a high-level decision, it lives in [ADR/](../ADR/README.md) and uses `NNNN-<name>.xml` plus `NNNN-<name>.png`.
- C4 Level 3 drawings live in the target folder and use `c4-l3-<container>-<name>`.
- Never leave a PNG without its XML source.
- Link each drawing from the README of its folder, and from [ARCHITECTURE.md](../ARCHITECTURE.md) when it is system-wide.

## Ownership

- `/create-adr` owns high-level ADRs and their system-wide diagrams.
- The platform architects own C4 Level 3 diagrams for their target. They do not create or edit ADRs.

## Status

Process models are documented. Target and low-level drawings are added as ADRs are accepted; see the open decisions in [ARCHITECTURE.md](../ARCHITECTURE.md#open-decisions).
