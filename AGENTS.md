# Agents

Project guidance for AI agents. This file routes; detailed content lives in the linked documents.

## Read first

1. [REQUIREMENTS.md](REQUIREMENTS.md) — what must be true. Check a box only when implemented and verified.
2. [ARCHITECTURE.md](ARCHITECTURE.md) — current architecture summary and open decisions.
3. [ADR/README.md](ADR/README.md) — the decision index. ADRs are the source of truth.

## Rules

- Use `/create-adr` for every high-level architecture decision. The command owns the ADR template, the reviewer/fix loop, and the index updates. Do not write or edit an ADR directly.
- `/create-adr` is platform-agnostic. Do not use it to choose AWS, Azure, or Kubernetes services.
- Platform architects (`architect-aws`, `architect-azure`, `architect-k8s`) are used after the ADR for platform advice and C4 Level 3 diagrams. They do not create high-level ADRs.
- At the end of every command or task that changes a Markdown file, run `/documentation` in fix mode and resolve its findings before finishing. No command or task is complete until the documentation pass is clean.
- Never invent a decision. Synthetic data only; no secrets, credentials, or real personal data.
- Do not mark a requirement checked without implementation and verification.

## ADR command

`/create-adr` creates the ADR, invokes `adr-reviewer`, asks which findings to fix, applies them, re-reviews, and repeats until no Blocking or Major findings remain. Only then does it ask for acceptance.

After acceptance, the platform architects (`architect-aws`, `architect-azure`, `architect-k8s`) produce C4 Level 3 component diagrams in `ARCHITECTURE/<platform>/`. They work from accepted ADRs and do not change them.
