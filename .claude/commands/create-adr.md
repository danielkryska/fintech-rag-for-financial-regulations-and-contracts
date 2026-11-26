---
description: Create a high-level, platform-agnostic ADR, then review it and loop through fixes until no major findings remain
argument-hint: "[decision topic] (optional)"
---

# Create an ADR

You facilitate one high-level, platform-agnostic Architecture Decision Record. You own the whole chain: **create → review → fix → re-review**. Frame the decision, interview, present options, write the ADR, run the reviewer, ask which findings to fix, apply them, re-review, and accept only when the user explicitly approves.

This command does **not** choose AWS, Azure, or Kubernetes services. After the ADR is accepted, `/create-c4` owns the C4 Levels 1 and 2 drawings, and the platform architects (`architect-aws`, `architect-azure`, `architect-k8s`) produce the Level 3 drawings.

## 1. Read first

- `REQUIREMENTS.md`
- `ARCHITECTURE.md`
- `ADR/README.md`
- Every `ADR/NNNN-*.md`
- `README.md` — the C4 index table, for linking or naming an existing drawing.

If these disagree, existing ADRs win. Report the conflict before writing anything.

## 2. Scope gate

An ADR here is high-level and cross-cutting: a decision that shapes the system or the product across targets. Examples: retrieval architecture, grounding and citation model, tenancy and permission model, audit model, evaluation gate, deployment topology class, a major library class, a SaaS category.

Stop and route elsewhere if the request is platform-specific:

- "Which AWS or Azure service?"
- "Which Kubernetes operator, ingress, or service mesh?"
- "Which managed vector database vendor?"
- Any request to choose a specific cloud SKU, region, or service.

Say: "This is platform-specific. `/create-adr` records high-level decisions; use `/create-c4` for Levels 1 and 2 and the relevant platform architect for platform advice and Level 3 drawings." Do not invoke a platform architect or `/create-c4` from this command.

## 3. Interview

Ask 3–5 questions per round, highest-leverage first:

- Which requirement IDs does this affect?
- What is fixed by accepted ADRs or compliance?
- Who are the users, tenants, and data owners?
- What data classification, residency, and retention rules apply?
- What scale, latency, and cost targets matter?
- What must keep working when a dependency fails?
- What is the team's operational capacity?
- What would make this decision wrong in 12 months?

Use `AskUserQuestion` when available. Otherwise return a numbered question list and stop.

## 4. Present options

Present 2–3 viable high-level options. For each: what it is, pros, cons, cost and operational impact, lock-in, residency, failure modes, and pillar impact. Recommend one, state why, and state what would reverse it. No hype.

Run a simplification pass: name the simplest viable option and the components or decisions it removes. Do not simplify away compliance, security, or reliability controls.

Ask the user to choose before writing. Do not write an `Accepted` ADR without explicit approval.

## 5. Write the ADR

Find the next free number by globbing `ADR/[0-9][0-9][0-9][0-9]-*.md` and taking the highest plus one. Never reuse a number. Write `ADR/NNNN-short-kebab-title.md` using the template below with `Status: Proposed` and `Scope: Cross-cutting`.

In the same change:

- Add the row to `ADR/README.md`.
- Add the row to the `ARCHITECTURE.md` decision register.
- If the decision changes the architecture, note that `/create-c4` must update the affected C4 Levels 1 and 2 after acceptance, and that the matching platform architect must then update the Level 3 drawings.

## 6. Review/fix loop

Repeat until no Blocking or Major findings remain:

1. Invoke the `adr-reviewer` subagent on the ADR path. It is read-only.
2. Present its findings to the user in a table. Ask which findings to fix, using `AskUserQuestion` with `multiSelect: true` when available. Recommend fixing all Blocking and Major findings. Minor findings can be fixed, recorded as follow-ups, or waived.
3. Apply only the selected fixes. Never change the decision the user approved; if a finding requires a different decision, ask the user first.
4. Re-run `adr-reviewer`.
5. If the same finding survives two rounds, stop and ask the user to resolve it.

Do not skip the review. Do not accept the ADR while Blocking or Major findings remain. "Mid-level" means Major: the loop stops when no Blocking or Major findings remain.

## 7. Accept

Ask the user to accept. Only with explicit approval:

- Set `Status: Accepted`.
- Set the date to today.
- Re-sync `ADR/README.md` and the `ARCHITECTURE.md` decision register.

If the user declines, leave the ADR `Proposed` and report what remains.

## 8. Hand off to C4

After acceptance, if the decision changes the architecture:

- Run `/create-c4` for the affected Level 1 or Level 2 drawing. It owns the draw.io standard, validator, `c4-reviewer` loop, and user confirmation gate.
- After Levels 1 and 2 are confirmed, `/create-c4` invokes the matching platform architect (`architect-aws`, `architect-azure`, or `architect-k8s`) for the Level 3 drawing in `c4-architecture/` and a platform advisory review.

The platform architects do not rewrite the ADR. If they find a conflict, they report it and the user runs `/create-adr` again for a superseding decision.

## ADR template (canonical)

```markdown
# NNNN. Short decision title

- **Status:** Proposed
- **Date:** YYYY-MM-DD
- **Deciders:** names or roles
- **Scope:** Cross-cutting
- **Related:** ADR-NNNN; REQUIREMENTS.md FR-xx, NFR-xx

## Context

Facts, forces, and constraints. Neutral; no advocacy. State what forces the decision now.

## Options considered

### Option A — name

What it is. Pros. Cons. Cost and operations. Lock-in and residency.

### Option B — name

What it is. Pros. Cons. Cost and operations. Lock-in and residency.

### Option C — name (if viable)

What it is. Pros. Cons. Cost and operations. Lock-in and residency.

## Decision

We will ... . Rationale: ... . What would reverse this: ... .

## Well-architected assessment

| Pillar | Impact | Evidence and mitigation |
| --- | --- | --- |
| Operational excellence | positive / negative / neutral / N/A | ... |
| Security | ... | ... |
| Reliability | ... | ... |
| Performance efficiency | ... | ... |
| Cost optimization | ... | ... |
| Sustainability | ... | ... |

Material gaps found during this assessment are recorded in Consequences → Follow-ups, with severity and owner.

## Simplification check

- Components removed, merged, or deferred: ...
- Simplest viable option considered: ...
- Why the chosen option is no more complex than necessary: ...

## Consequences

- **Positive:** ...
- **Negative:** ...
- **Follow-ups:** ...

## Diagram

For a system-wide decision, link the confirmed C4 drawing in `c4-architecture/` once `/create-c4` has produced it (for example `step3_lvl2_v4_retrieve-generate-stream.drawio`). If no C4 drawing exists yet, name the Level 1 or Level 2 drawing that `/create-c4` must create. Do not embed C4 XML in the ADR. A non-C4 decision sketch may be inline draw.io XML in a fenced `xml` block or a sidecar `NNNN-<drawing-name>.xml`; include `NNNN-<drawing-name>.png` only when it exists.
```

## Output

Return:

1. ADR path and final status.
2. Review loop summary: rounds run, findings raised, findings fixed, findings waived or deferred.
3. Remaining findings, if any, with severity.
4. The next step: `/create-c4` for the affected Level 1 or Level 2 drawing, a platform architect for Level 3, another ADR, or no action.
