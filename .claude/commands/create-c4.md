---
description: Create or revise one C4 architecture drawing, run the C4 reviewer/fix loop, and gate every level on explicit user confirmation
argument-hint: "[lvl1|lvl2|lvl3|next] [drawing name] (optional)"
---

# Create a C4 drawing

You own one C4 drawing at a time and the gate around it: **draw → review → fix → re-review → user confirmation → next level**. You do not choose platform services for Level 1 or Level 2. Level 3 is drawn by the matching platform architect and reviewed through the same gate.

The canonical rules, naming, index, and Level 3 checklist live in [`c4-architecture/README.md`](../../c4-architecture/README.md). Read it before drawing; this command does not replace it.

## 1. Read first

- `c4-architecture/README.md` — the drawing standard, naming, index, and Level 3 checklist.
- `REQUIREMENTS.md`
- `ARCHITECTURE.md`
- `ADR/README.md` and every accepted ADR.
- The project walkthrough PDF in `ADR/`, including its hand-drawn flows. If the PDF has no text layer, render its pages to images first (for example with PyMuPDF `page.get_pixmap()` at 140–260 DPI, rotating landscape pages), then read the images.
- `src/README.md`, `infra/README.md`.
- Every existing `c4-architecture/*.drawio` and the index in `c4-architecture/README.md`.

If documents disagree, the ADR wins. Report the conflict before drawing.

## 2. Determine the request

- `next` or no argument: the next unconfirmed level.
  - If Level 1 is not `Confirmed`, do Level 1.
  - If Level 1 is confirmed and no Level 2 slices exist, propose the slice map and confirm it with the user before drawing.
  - If all Level 2 slices are confirmed, ask which platform and slice for Level 3.
- `lvl1`: system context.
- `lvl2 <slice>`: one business-flow slice. If the slice map is not agreed, propose it first.
- `lvl3 <slice>`: platform realisation. Ask which platform (`aws`, `azure`, `k8s`) if not given. Level 3 requires confirmed Level 1 and Level 2.
- Revising a confirmed drawing: create a new version; never overwrite a confirmed file.

A level is confirmed only when the index says `Confirmed` and the user approved it.

## 3. Level 1 — system context

Level 1 is top-down: actors in a row on top, exactly one own-system black box in the middle, external systems at the bottom. Each layer is centered horizontally on the page's center axis. The flow is the initial request only: actors → system and system → external systems. There are no return lines.

Use the draw.io C4 shape set:

- Actors: `shape=mxgraph.c4.person2` boxes in one centered row, no container box, fill `#1F4E79`. Each box shows the actor name (bold), the type tag `[Person]`, and the actor's responsibilities as bullets, vertically centered, in white. Bold the name with an explicit white colour span (`&lt;span style="color:#ffffff;font-weight:bold"&gt;`), not `<b>` — the plain `<b>` tag renders grey in some viewers.
- Own system: `shape=mxgraph.c4.system`, exactly one box for this project. It contains the system name (for example "Enterprise RAG knowledge assistant"), the type tag `[Software System]`, and bullets describing what the system as a whole does — one feature per bullet, in business terms (what happens, not how). Fill `#DAE8FC`, thick solid border. Do not split it into ingestion, retrieval, and governance black boxes.
- External systems: `shape=mxgraph.c4.external`. Each box shows the name, the type tag `[Software System]`, and a one-line description. Fill `#F5F5F5`, solid border.
- Lines: one line per initial request, pointing downward. Level 1 lines carry no text; the line style carries the communication type: solid = synchronous request, dashed = asynchronous request.
- A legend box with colour swatches (person, software system, external software system) and two arrow samples: solid = synchronous request, dashed = asynchronous request.
- Title block: top-left corner, `C4 Level 1 - <system name>` only. Version, status, date, requirements, and ADRs live in the index.

Before drawing, list:

- Actors from `REQUIREMENTS.md` and the walkthrough: employee, records administrator, compliance officer, reviewer, access-control owner, platform operator, and build-time roles such as the retrieval engineer. Roles may be merged into one actor when the user consolidates them; add or drop roles only with a reason.
- External systems outside the platform boundary: corporate identity provider, HR/directory attributes, source document systems, model providers (embedding, reranking, text generation), SIEM, evaluation tooling, and any other system the requirements imply.
- The initial requests to show: one line per actor → system and one line per system → external system, solid or dashed by synchronous/asynchronous.

Rules:

- Do not show containers, services, databases, cloud services, or technology tags in `[]`; only the type tags `[Person]` and `[Software System]` are allowed.
- No requirement IDs (FR-…, NFR-…, EVAL-…) on the drawing; the index records the coverage.
- No return lines, responses, or bidirectional arrows.
- Top-down order: every actor above the system; every external system below it.
- No line crossings. Use the ids `actor-<name>`, `system`, and `ext-<name>`.
- If an actor or external system is genuinely ambiguous, ask the user with `AskUserQuestion`. Otherwise proceed.

File: `c4-architecture/lvl1_v<K>_system_context.drawio` (or a more specific drawing name if the scope is narrower).

## 4. Level 2 — business-flow slices

Propose the slice map before drawing. A typical map for this project:

| Slice | Scope | Requirements | Repositories | Boundary interactions |
| --- | --- | --- | --- | --- |

Cover at least: document ingestion and processing; indexing and retrieval; query and answer generation; governance, audit, and evaluation. Split further only if a slice is too large to draw without crossings or too broad to review.

Ask the user to confirm the slice map. Then, for each slice:

1. Draw `c4-architecture/lvl2_v<K>_<slice>.drawio`.
2. Structure: one outer container box (`sys-container`) named after the system — light blue `#DAE8FC`, thick border, like the Level 1 black box. Inside it, three groups with dashed lines and no fill: **Web app UI** (`grp-ui`) on top, **Backend** (`grp-backend`) in the middle, **Repositories (DBs)** (`grp-repos`) at the bottom. Actors above the block; external systems below it.
3. Box labels: bold module name on the first line, bullet points of what the block does or keeps, and the generic technology type in brackets on the last line: `[web ui]`, `[worker]`, `[service]`, `[object storage]`, `[vector db]`, `[audit store]`.
4. Edge labels are two lines: the action on the first line, the protocol on the second (`POST /documents` newline `[http]`). Sync and async use solid vs dashed lines, explained in a legend.
5. Put bullet points inside each business-logic block: what it validates, filters, authorizes, searches, assembles, stores, or rejects. Do not put implementation detail in the bullets.
6. Do not draw queues, brokers, event streams, buses, or topics as boxes. Put them on the edge (`[message]`, `[event stream]`).
7. Show the slice end to end: trigger, representation entry point, business steps, repositories read or written, response or event, and the failure or fallback path where the requirements define one.
8. Show permission filtering, PII handling, audit writes, and other controls at the point where they happen.
9. Show only the slice's internals. A neighbouring slice is a grey boundary box with a labelled edge; do not draw the neighbour's internals.
10. Record the slice map, requirements covered, and ADRs referenced in the index.

Do not use vendor, product, or cloud service names at Level 2 and do not select solutions — generic names only (`vector db`, not a specific product). If a technical choice is needed, record it as an open question or route it to `/create-adr`; do not draw it.

## 5. Draw the XML

Follow the standard and the XML skeleton in `c4-architecture/README.md`.

- One complete `<mxfile>` with exactly one `<diagram>` page.
- Required IDs: `title`, `band-representation`, `band-business`, `band-repository`. Legend and note cells use ids starting `legend-` or `note-`.
- Every box has a label. Every edge has a source, a target, and waypoints where the route needs them; edges carry a label at Level 2 and 3, no text at Level 1 (solid/dashed style instead).
- No line crossings, no edge through an unrelated box, no overlapping boxes, no orphan boxes.
- Level 1 title block: only `C4 Level 1 - <system name>`. Level 2 and 3 title block: level, name, version, status, date, requirements covered, and ADRs referenced.
- Write the file with the status `Draft` (in the title block at Level 2 and 3; Level 1 tracks status only in the index). Add or update its index row as `Draft`.
- Do not create a PNG unless the draw.io CLI is available and the user asked for it. Never claim a render that does not exist.

## 6. Check the mechanical rules

There is no static validator. Before invoking the reviewer, go through the review checklist in `c4-architecture/README.md` yourself and fix what you find: file naming, one page, unique ids, edge endpoints, title block, Level 1 ids/order/shapes/colours/type tags/bullets/edge directions/line styles/legend, Level 2/3 bands, `[technology]` and `[protocol]` tags, business bullets, vendor leakage, queue-on-edge, orphan boxes, overlaps, crossings, edges through boxes. `c4-reviewer` re-checks all of them.

## 7. Review/fix loop

Set the drawing's index status to `In review`. Repeat until no Blocking or Major findings remain:

1. Invoke the `c4-reviewer` subagent on the drawing. Include the requirements, the relevant ADRs, and the confirmed Level 1/Level 2 inputs.
2. Present its findings to the user in a table. Ask which findings to fix, using `AskUserQuestion` with `multiSelect: true` when available. Recommend fixing all Blocking and Major findings. Minor findings can be fixed, recorded as follow-ups, or waived.
3. Apply only the selected fixes. Never change a confirmed decision; if a finding requires a different decision, ask the user and route it to `/create-adr`.
4. Re-run `c4-reviewer`.
5. If the same finding survives two rounds, stop and ask the user to resolve it.

Do not accept a drawing while Blocking or Major findings remain.

## 8. User confirmation gate

After the review is clean:

- Present the drawing path, what it shows, the requirements covered, the open questions, and the reviewer's verdict.
- Ask the user: "Is this drawing correct and complete enough to confirm?" Use `AskUserQuestion` with `Yes, confirm`, `No, changes needed`, and `Review the XML first`.
- Only `Yes` sets `Status: Confirmed`, the confirmation date, and the index status.
- On `No`, capture concrete feedback, fix, re-run the reviewer, and ask again. Repeat until confirmed or the user stops.
- The reviewer's `Accept` is not user confirmation. A drawing is `Confirmed` only because the user approved it.

## 9. Update the index

In `c4-architecture/README.md`:

- Add or update the row: level, version, drawing, file link, scope, requirements, ADRs, status, confirmed date.
- When a new version supersedes a confirmed one, keep the old row and set `Superseded by <file>`.
- Do not invent rows for drawings that do not exist.
- Do not mark a drawing `Confirmed` without the user's explicit approval.

## 10. Proceed to the next level

- Level 1 confirmed → ask whether to proceed to Level 2. If yes, propose the slice map (step 4).
- Level 2 confirmed → ask whether to proceed to Level 3. If yes, ask which platform and which slice, then invoke the matching platform architect.
- Level 3 confirmed → stop and report what remains for the other platforms and slices.

## 11. Level 3 handoff

- Invoke `architect-aws`, `architect-azure`, or `architect-k8s` with: the confirmed Level 1 and Level 2 files, the accepted ADRs, the C4 standard, the target slice, and the Level 3 completeness checklist.
- The architect writes `c4-architecture/lvl3_v<K>_<technology>_<slice>.drawio` and returns the Level 2 → Level 3 mapping, checklist coverage, and open decisions.
- Check the review checklist in `c4-architecture/README.md`, then run `c4-reviewer`, the fix loop, and the same user confirmation gate.
- The platform architect does not mark the drawing confirmed.
- If the architect finds a missing high-level decision, route it to `/create-adr`; do not invent it.

## 12. Rules you must not break

- draw.io XML only; no screenshots, images, or other diagram formats.
- Three bands: **Representation** on top, **Business logic** in the middle, **Repository** on the bottom.
- No line intersections, no edge through a box, no overlapping boxes.
- Level 1 lines are unlabelled: solid = synchronous request, dashed = asynchronous request. Level 2 and 3 lines are labelled with what happens; protocols in `[]`.
- Queues, streams, brokers, buses, and topics are edge labels, not boxes.
- Level 1: actors in a centered row, external systems with solid borders, black-box system(s); no internals and no technology tags; only `[Person]` and `[Software System]` type tags; no requirement IDs on the drawing; every layer centered on the page's center axis; edges routed orthogonally like circuit-board traces.
- Level 2: generic technology categories only; no vendor, product, or cloud service names.
- Level 3: specific technologies and full infrastructure topology; nothing skipped.
- Level 3 only after Level 1 and Level 2 are confirmed.
- No secrets, credentials, account IDs, or real personal data.

## Output

Return:

1. Drawing path, level, version, and status.
2. Reviewer loop summary: rounds run, findings raised, findings fixed, findings waived or deferred.
3. Requirements and ADRs covered; open questions.
4. The confirmation result and the next level or handoff.
