---
description: Check and update every Markdown document for consistency with the ADRs, sync the indexes, and report contradictions
argument-hint: "[check|fix] (default: fix)"
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Documentation consistency pass

Maintain the documentation system: one fact, one canonical home; no contradictions; indexes match reality; the architecture summary stays current as ADRs are accepted.

Mode: `$ARGUMENTS` — `check` reports only; `fix` or empty applies safe fixes and reports.

## 1. Inventory

List every Markdown file, tracked and untracked:

```bash
git ls-files '*.md'
git ls-files --others --exclude-standard '*.md'
```

Read every file. Also inventory drawing assets:

```bash
git ls-files 'ADR/*.xml' 'ADR/*.png' 'ARCHITECTURE/**/*.xml' 'ARCHITECTURE/**/*.png'
git ls-files --others --exclude-standard 'ADR/*.xml' 'ADR/*.png' 'ARCHITECTURE/**/*.xml' 'ARCHITECTURE/**/*.png'
```

## 2. Precedence when documents disagree

1. `ADR/NNNN-*.md` — decisions. Highest authority.
2. `ARCHITECTURE.md` — the summary and register.
3. `REQUIREMENTS.md` — what must be true.
4. `README.md` — landing page only.
5. Subfolder READMEs — local layout and scope.

`AGENTS.md` and `CLAUDE.md` only route; they must not contain rules that contradict the documents above.

If two sources disagree, the ADR wins and the lower source is corrected. If the ADR is wrong, do not edit it: propose a superseding ADR and report it.

## 3. Checks

| ID | Check |
| --- | --- |
| DOC-01 | `README.md` is a landing page: no repository layout tree, no requirement list, no architecture decisions. It links to `ADR/README.md`, `REQUIREMENTS.md`, `ARCHITECTURE.md`, and `ARCHITECTURE/`. |
| DOC-02 | `REQUIREMENTS.md` uses `- [ ]` / `- [x]` checkboxes, IDs are unique and sequential, no service or library prescriptions, and no box is checked without implementation evidence. |
| DOC-03 | `ARCHITECTURE.md` register has one row per ADR and no stale rows. Number, one-line decision, scope, status, and date match the ADR files. No decision appears that is not in an ADR. Open decisions are labelled Open. |
| DOC-04 | `ADR/README.md` index has one row per ADR file and no stale rows. Number, title, scope, status, and date match. Rows are sorted by number. |
| DOC-05 | ADR filenames match `NNNN-kebab-title.md`; numbers are unique, four digits, and sequential without unexplained gaps; required header fields and sections (Context, Options considered, Decision, Well-architected assessment, Simplification check, Consequences) exist; status and scope values are valid; dates are ISO. |
| DOC-06 | ADRs are high-level and platform-agnostic: flag implementation detail, a specific AWS/Azure/Kubernetes service choice in a high-level ADR, missing alternatives, missing negatives in Consequences, an assessment that ignores security, reliability, or cost, missing simplification, or a settled decision recorded outside an ADR. |
| DOC-07 | Every referenced `.xml` or `.png` exists. ADR drawings use `NNNN-<drawing-name>.xml` and `.png`; every PNG has its XML source; no claimed render is missing; inline XML is a complete `<mxfile>` in a fenced `xml` block. |
| DOC-08 | Every relative Markdown link resolves, case-sensitively, including anchors when the anchor target is checkable. |
| DOC-09 | Terminology is consistent: the folder is `k8s/` and prose says "Kubernetes"; product names are spelled consistently; "ADR" is uppercase; no stale `kubernetes/` path or `template.md` reference. |
| DOC-10 | `CLAUDE.md` imports `AGENTS.md`; `AGENTS.md` stays thin, routes to canonical documents, and directs all ADR creation to `/create-adr`; neither duplicates or contradicts them. |
| DOC-11 | No secrets, credentials, tokens, account IDs, or real personal data. Synthetic data only. |
| DOC-12 | The canonical ADR template lives in `.claude/commands/create-adr.md`; ADR files use its fields and sections. The platform agents must not contain a competing template, and `ADR/template.md` must not exist. |
| DOC-13 | Target folders `ARCHITECTURE/aws`, `ARCHITECTURE/azure`, `ARCHITECTURE/k8s`, `ARCHITECTURE/process-level-modeling`, and `ARCHITECTURE/low-level-architectures` exist, each with a README, and the layout table in `ARCHITECTURE/README.md` matches them. The AWS, Azure, and Kubernetes READMEs each name the framework used for review and document the `c4-l3-<container>-<name>` convention. |
| DOC-14 | Requirement IDs cited by ADRs exist. A requirement affected by a decision is referenced; no ADR cites a nonexistent ID. |
| DOC-15 | Each ADR's `## Well-architected assessment` covers operational excellence, security, reliability, performance efficiency, cost optimization, and sustainability. Each row has an impact and evidence, or an explicit `N/A` reason. `## Simplification check` names removed, merged, or deferred components and the simplest viable option. Material gaps are in Consequences → Follow-ups with severity and owner. |
| DOC-16 | The platform agent files reference `/create-adr` for high-level decisions and own C4 Level 3 diagrams. They do not contain an ADR template or an ADR-writing workflow. |
| DOC-17 | `.claude/commands/create-adr.md` exists and contains the platform-agnostic scope gate, the ADR template, and the review/fix loop with `adr-reviewer` that asks which findings to fix and repeats until no Blocking or Major findings remain. |

Self-scan note: this command file quotes stale examples (`kubernetes/`, `template.md`) and prohibited names. When applying DOC-09 and DOC-12, treat those occurrences as instructions, not content; do not flag this file for them.

## 4. Fix policy

Safe to fix without asking, in `fix` mode:

- Sync `ADR/README.md` and the `ARCHITECTURE.md` register from the ADR files.
- Fix a broken relative link when the target is unambiguous.
- Sort tables by ADR number; normalize dates to ISO; normalize status and scope values.
- Fix stale terminology and folder names (`kubernetes/` to `k8s/`).
- Add missing canonical-document links to a README.
- Fix the ADR index heading levels or table headers.

Ask before:

- Editing an accepted ADR's decision, context, or consequences.
- Deleting content or moving files.
- Changing a requirement or checking a box.

Never:

- Invent a decision or an option.
- Mark a requirement done without evidence.
- Change `Proposed` to `Accepted` without explicit user acceptance.
- Fabricate a PNG or claim a render exists.
- Create `ADR/template.md`.
- Create, supersede, or deprecate an ADR. That belongs to `/create-adr`.

## 5. Sync the architecture register

For each ADR file, extract the title, status, scope, date, and the one-line decision. Ensure both indexes have the row. When an ADR is `Superseded by ADR-NNNN`, keep the row and show the status. Remove only rows whose ADR file no longer exists, after confirming the deletion was intentional.

## 6. Output

1. **Summary:** files checked, files changed, findings by severity.
2. **Findings table:** Check | File | Finding | Severity | Action.
3. **Changes:** files edited with a one-line reason, plus `git diff --stat`.
4. **Open questions** that need the user or a platform architect.
5. **Next action:** the smallest step that resolves the highest-severity finding (for example, "run `architect-azure` to settle the model provider").

In `check` mode, perform sections 1–3, report what section 5 would change, and produce section 6's output. Make no edits.
