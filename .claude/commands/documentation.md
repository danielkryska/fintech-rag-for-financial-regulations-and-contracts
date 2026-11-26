---
description: Check and update every Markdown document for consistency with the ADRs and the C4 index, sync the indexes, and report contradictions
argument-hint: "[check|fix] (default: fix)"
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Documentation consistency pass

Maintain the documentation system: one fact, one canonical home; no contradictions; indexes match reality; the architecture summary and the C4 index stay current.

Mode: `$ARGUMENTS` — `check` reports only; `fix` or empty applies safe fixes and reports.

## 1. Inventory

List every Markdown file, tracked and untracked:

```bash
git ls-files '*.md'
git ls-files --others --exclude-standard '*.md'
```

Read every file. Also inventory drawing assets:

```bash
git ls-files 'ADR/*.xml' 'ADR/*.png' 'c4-architecture/*.drawio' 'c4-architecture/*.png'
git ls-files --others --exclude-standard 'ADR/*.xml' 'ADR/*.png' 'c4-architecture/*.drawio' 'c4-architecture/*.png'
```

Confirm the folder move:

```bash
test -d c4-architecture && test ! -d ARCHITECTURE
```

## 2. Precedence when documents disagree

1. `ADR/NNNN-*.md` — decisions. Highest authority.
2. `ARCHITECTURE.md` — the summary and register.
3. `REQUIREMENTS.md` — what must be true.
4. `.claude/commands/create-c4.md` — the canonical C4 drawing standard.
5. `README.md` — landing page and the C4 index table.
6. Subfolder READMEs — local layout and scope.

`AGENTS.md` and `CLAUDE.md` only route; they must not contain rules that contradict the documents above.

If two sources disagree, the ADR wins and the lower source is corrected. If the ADR is wrong, do not edit it: propose a superseding ADR and report it.

## 3. Checks

| ID | Check |
| --- | --- |
| DOC-01 | `README.md` is a landing page: no repository layout tree, no requirement list, no architecture decisions. It links to `ADR/README.md`, `REQUIREMENTS.md`, `ARCHITECTURE.md`, and `c4-architecture/`. |
| DOC-02 | `REQUIREMENTS.md` uses `- [ ]` / `- [x]` checkboxes, IDs are unique and sequential, no service or library prescriptions, and no box is checked without implementation evidence. |
| DOC-03 | `ARCHITECTURE.md` register has one row per ADR and no stale rows. Number, one-line decision, scope, status, and date match the ADR files. No decision appears that is not in an ADR. Open decisions are labelled Open. |
| DOC-04 | `ADR/README.md` index has one row per ADR file and no stale rows. Number, title, scope, status, and date match. Rows are sorted by number. |
| DOC-05 | ADR filenames match `NNNN-kebab-title.md`; numbers are unique, four digits, and sequential without unexplained gaps; required header fields and sections (Context, Options considered, Decision, Well-architected assessment, Simplification check, Consequences) exist; status and scope values are valid; dates are ISO. |
| DOC-06 | ADRs are high-level and platform-agnostic: flag implementation detail, a specific AWS/Azure/Kubernetes service choice in a high-level ADR, missing alternatives, missing negatives in Consequences, an assessment that ignores security, reliability, or cost, missing simplification, or a settled decision recorded outside an ADR. Implementation detail belongs in code or `c4-architecture/`. |
| DOC-07 | Every referenced `.drawio`, `.xml`, or `.png` exists. ADR sketches use `NNNN-<drawing-name>.xml` and `.png`; every PNG has its XML source; no claimed render is missing; inline XML is a complete `<mxfile>` in a fenced `xml` block. C4 files are complete `<mxfile>` documents with one `<diagram>` page. |
| DOC-08 | Every relative Markdown link resolves, case-sensitively, including anchors when the anchor target is checkable. |
| DOC-09 | Terminology is consistent: the drawing folder is `c4-architecture/`; there is no `ARCHITECTURE/` folder and no link to one; "C4" is uppercase; "draw.io" is spelled consistently; Level 3 technology tokens in filenames are lowercase (`aws`, `azure`, `k8s`); no stale `kubernetes/` path or `template.md` reference. |
| DOC-10 | `CLAUDE.md` imports `AGENTS.md`; `AGENTS.md` stays thin, routes to canonical documents, directs ADR creation to `/create-adr`, directs C4 creation to `/create-c4`, and neither duplicates nor contradicts the canonical documents. |
| DOC-11 | No secrets, credentials, tokens, account IDs, or real personal data. Synthetic data only. |
| DOC-12 | The canonical ADR template lives in `.claude/commands/create-adr.md`; ADR files use its fields and sections. The platform agents must not contain a competing template, and `ADR/template.md` must not exist. The canonical C4 standard lives in `.claude/commands/create-c4.md`; agents and commands must not contain a competing drawing standard. |
| DOC-13 | `c4-architecture/` exists and holds the current C4 drawings plus the walkthrough PDF; `ARCHITECTURE/` does not exist. The C4 index is the table in `README.md` with one row per C4 drawing file and no stale rows. |
| DOC-14 | Requirement IDs cited by ADRs exist. A requirement affected by a decision is referenced; no ADR cites a nonexistent ID. |
| DOC-15 | Each ADR's `## Well-architected assessment` covers operational excellence, security, reliability, performance efficiency, cost optimization, and sustainability. Each row has an impact and evidence, or an explicit `N/A` reason. `## Simplification check` names removed, merged, or deferred components and the simplest viable option. Material gaps are in Consequences → Follow-ups with severity and owner. |
| DOC-16 | The platform agent files own only C4 Level 3 drawings for their target. They reference `/create-adr` for high-level decisions and `/create-c4` plus `.claude/commands/create-c4.md` for the C4 process. They do not own Levels 1 or 2, do not contain an ADR template, and do not contain a competing drawing standard. |
| DOC-17 | `.claude/commands/create-adr.md` exists and contains the platform-agnostic scope gate, the ADR template, and the review/fix loop with `adr-reviewer` that asks which findings to fix and repeats until no Blocking or Major findings remain. |
| DOC-18 | `.claude/commands/create-c4.md` exists and contains the draw → review → fix → user confirmation gate, the level sequence, and the Level 3 handoff. `.claude/agents/c4-reviewer.md` exists, is read-only, blocks confirmation on Blocking or Major findings, and performs the mechanical checks from the review checklist in `.claude/commands/create-c4.md` (there is no static validator). |
| DOC-19 | C4 naming and versioning: Level 1 files match `lvl1_v<K>_<drawing_name>.drawio` and Level 2 files match `step<K>_lvl2_v<N>_<drawing_name>.drawio`; Level 3 files match `lvl3_v<K>_<aws\|azure\|k8s>_<drawing_name>.drawio`; version numbers are not reused; confirmed versions are not overwritten; the index row matches the file's level, version, drawing name, and status. |
| DOC-20 | Every `c4-architecture/*.drawio` is well-formed XML with one `<diagram>` page, and the mechanical rules of the review checklist in `.claude/commands/create-c4.md` hold (naming, ids, title block, colours, shapes, type tags, edge directions, no crossings or overlaps), or the Blocking findings are reported for `/create-c4` to fix. The semantic review belongs to `c4-reviewer`; this pass checks presence, naming, indexing, and mechanical well-formedness. |

Self-scan note: this command file quotes the stale folder name and prohibited names. When applying DOC-09 and DOC-12, treat those occurrences as instructions, not content; do not flag this file for them.

## 4. Fix policy

Safe to fix without asking, in `fix` mode:

- Sync `ADR/README.md` and the `ARCHITECTURE.md` register from the ADR files.
- Sync the C4 index table in `README.md` from the XML files and their title blocks.
- Fix a broken relative link when the target is unambiguous.
- Sort tables by ADR number or by C4 level and version; normalize dates to ISO; normalize status and scope values.
- Fix stale terminology and folder names (`ARCHITECTURE/` to `c4-architecture/`, `kubernetes/` to `k8s/`).
- Add missing canonical-document links to a README.
- Fix the ADR index or C4 index heading levels or table headers.

Ask before:

- Editing an accepted ADR's decision, context, or consequences.
- Deleting content or moving files.
- Changing a requirement or checking a box.
- Changing a C4 drawing's level, scope, or confirmed status.

Never:

- Invent a decision or an option.
- Mark a requirement done without evidence.
- Change `Proposed` to `Accepted` without explicit user acceptance.
- Change a C4 drawing to `Confirmed` without explicit user confirmation.
- Fabricate a PNG or claim a render exists.
- Create `ADR/template.md`.
- Create, supersede, or deprecate an ADR. That belongs to `/create-adr`.
- Draw or edit a C4 diagram. That belongs to `/create-c4` and the platform architects.

## 5. Sync the indexes

For each ADR file, extract the title, status, scope, date, and the one-line decision. Ensure both the ADR index and the `ARCHITECTURE.md` decision register have the row. When an ADR is `Superseded by ADR-NNNN`, keep the row and show the status. Remove only rows whose ADR file no longer exists, after confirming the deletion was intentional.

For each `c4-architecture/*.drawio`, extract the level and version from the filename, and the level, drawing name, version, status, requirements, and ADRs from the title block. Ensure the C4 index table in `README.md` has exactly one current row per drawing. Superseded versions are removed from the folder after the newer version is committed (git history keeps them). Do not change a `Confirmed` status without explicit user approval.

## 6. Run the mechanical C4 check

For each `c4-architecture/*.drawio`, go through the review checklist in `.claude/commands/create-c4.md` by hand: parse the XML, check the file naming, one `<mxfile>`/one `<diagram>`, unique cell ids, edge endpoints and waypoints, title block, Level 1 ids/order/shapes/colours/type tags/edge directions/line styles/legend, Level 2/3 bands, `[technology]` and `[protocol]` tags, business bullets, vendor leakage, queue-on-edge, orphan boxes, overlaps, crossings, and edges through boxes.

Report Blocking findings as DOC-20. Report Major findings for `/create-c4` and `c4-reviewer` to resolve; this pass does not waive them. If there are no C4 drawing files yet, state that the check is not applicable.

## 7. Output

1. **Summary:** files checked, files changed, findings by severity.
2. **Findings table:** Check | File | Finding | Severity | Action.
3. **Changes:** files edited with a one-line reason, plus `git diff --stat`.
4. **C4 mechanical check summary:** drawings checked against the review checklist, Blocking/Major/Minor counts.
5. **Open questions** that need the user or a platform architect.
6. **Next action:** the smallest step that resolves the highest-severity finding (for example, "run `/create-c4` to draw Level 1" or "run `architect-azure` to settle the model provider").

In `check` mode, perform sections 1–3 and 6, report what section 5 would change, and produce section 7's output. Make no edits.
