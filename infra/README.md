# Infrastructure

Infrastructure as code and deployment definitions for the targets described in [ARCHITECTURE.md](../ARCHITECTURE.md).

## Planned layout

```
infra/
├── azure/       # Azure target: model access, search, networking, Terraform
├── aws/         # AWS target: model access, search, networking, Terraform
├── k8s/         # Portable deployment, autoscaling, policy
└── modules/     # Shared Terraform and Helm building blocks
```

Do not choose a provider or service here. Decisions that shape this layout are recorded in [ADR/README.md](../ADR/README.md); run `/create-adr` to make one.

_Contents to be added._
