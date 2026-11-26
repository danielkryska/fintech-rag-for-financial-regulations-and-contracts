---
description: Create or revise one C4 architecture drawing, run the C4 reviewer/fix loop, and gate every level on explicit user confirmation
argument-hint: "[lvl1|lvl2|lvl3|next] [drawing name] (optional)"
---

# Create a C4 drawing

You own one C4 drawing at a time and the gate around it: **draw → review → fix → re-review → user confirmation → next level**. You do not choose platform services for Level 1 or Level 2. Level 3 is drawn by the matching platform architect and reviewed through the same gate.

**This command is the canonical C4 drawing standard**: rules, naming, gates, and the Level 3 checklist live here. The drawing index is the C4 table in [`README.md`](../../README.md). `c4-reviewer` and the platform architects read this file; do not maintain a competing standard elsewhere.

## 1. Read first

- This command — the canonical drawing standard (sections 3–6 and 12) and the Level 3 checklist (section 11).
- `REQUIREMENTS.md`
- `ARCHITECTURE.md`
- `ADR/README.md` and every accepted ADR.
- The project walkthrough PDF in `ADR/`, including its hand-drawn flows. If the PDF has no text layer, render its pages to images first (for example with PyMuPDF `page.get_pixmap()` at 140–260 DPI, rotating landscape pages), then read the images.
- `src/README.md`, `infra/README.md`.
- Every existing `c4-architecture/*.drawio` and the index table in `README.md`.

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

The current map is three steps: step 1 document ingestion, step 2 embed and index, step 3 retrieve, generate, cite, stream, authorize. Split further only if a slice is too large to draw without crossings or too broad to review.

Ask the user to confirm the slice map. Then, for each slice:

1. Draw `c4-architecture/step<K>_lvl2_v<N>_<slice>.drawio`, where K is the slice step number.
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

Follow the XML skeleton below.

- One complete `<mxfile>` with exactly one `<diagram>` page.
- Required IDs: `title`, `band-representation`, `band-business`, `band-repository`. Legend and note cells use ids starting `legend-` or `note-`.
- Every box has a label. Every edge has a source, a target, and waypoints where the route needs them; edges carry a label at Level 2 and 3, no text at Level 1 (solid/dashed style instead).
- No line crossings, no edge through an unrelated box, no overlapping boxes, no orphan boxes.
- Level 1 title block: only `C4 Level 1 - <system name>`. Level 2 and 3 title block: level, name, version, status, date, requirements covered, and ADRs referenced.
- Write the file with the status `Draft` (in the title block at Level 2 and 3; Level 1 tracks status only in the index). Add or update its index row as `Draft`.
- Do not create a PNG unless the draw.io CLI is available and the user asked for it. Never claim a render that does not exist.

### File conventions

- Drawings live in `c4-architecture/` — the only architecture drawing folder. There is no `ARCHITECTURE/` folder.
- Level 1: `lvl1_v<K>_<drawing_name>.drawio`. Level 2: `step<K>_lvl2_v<N>_<drawing_name>.drawio`, where K is the slice step (1 = document ingestion, 2 = embed and index, 3 = retrieve and generate). Level 3: `lvl3_v<K>_<technology>_<drawing_name>.drawio`, technology `aws`, `azure`, or `k8s`.
- `<drawing_name>` is lowercase snake_case. One drawing per file, one `<diagram>` page per file.
- The XML is the source of truth. A PNG is optional; never commit a PNG without its XML, and never claim a render that does not exist.
- Versions are never overwritten once confirmed. A material change creates a new version file; the index marks the old row `Superseded by <file>`.
- Status values: `Draft`, `In review`, `Confirmed`, `Superseded by <file>`.
- Only the latest version of each drawing stays in `c4-architecture/`; superseded iterations are deleted after the newer version is committed (git history keeps them).

### XML skeleton

Use this shape for every drawing. The `title` ID is required by the review checklist. Level 2 uses one outer `sys-container` with three dashed no-fill groups inside it (`grp-ui`, `grp-backend`, `grp-repos`); Level 3 uses the three band IDs below.

```xml
<mxfile host="app.diagrams.net">
  <diagram id="lvl2-query-answering" name="L2 Query and answer generation">
    <mxGraphModel grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1200" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="title" value="C4 Level 2 - ..." style="text;html=1;align=left;verticalAlign=top;fontSize=18;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="40" y="10" width="800" height="30" as="geometry" />
        </mxCell>
        <mxCell id="sys-container" value="&lt;b&gt;System name&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#DAE8FC;strokeColor=#6C8EBF;strokeWidth=3;verticalAlign=top;align=left;container=1;collapsible=0;" vertex="1" parent="1">
          <mxGeometry x="40" y="60" width="1520" height="680" as="geometry" />
        </mxCell>
        <mxCell id="grp-ui" value="Web app UI" style="rounded=0;whiteSpace=wrap;html=1;dashed=1;dashPattern=8 4;fillColor=none;strokeColor=#666666;verticalAlign=top;align=left;container=1;collapsible=0;" vertex="1" parent="sys-container">
          <mxGeometry x="40" y="40" width="1440" height="160" as="geometry" />
        </mxCell>
        <mxCell id="grp-backend" value="Backend" style="rounded=0;whiteSpace=wrap;html=1;dashed=1;dashPattern=8 4;fillColor=none;strokeColor=#666666;verticalAlign=top;align=left;container=1;collapsible=0;" vertex="1" parent="sys-container">
          <mxGeometry x="40" y="240" width="1440" height="240" as="geometry" />
        </mxCell>
        <mxCell id="grp-repos" value="Repositories (DBs)" style="rounded=0;whiteSpace=wrap;html=1;dashed=1;dashPattern=8 4;fillColor=none;strokeColor=#666666;verticalAlign=top;align=left;container=1;collapsible=0;" vertex="1" parent="sys-container">
          <mxGeometry x="40" y="520" width="1440" height="140" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

Boxes inside a Level 2 group use `parent="grp-ui"`, `parent="grp-backend"`, or `parent="grp-repos"`. Level 3 boxes inside a band use `parent="band-representation"`, `parent="band-business"`, or `parent="band-repository"`. Edges use `parent="1"`, a `source`, a `target`, and waypoints in the edge `<mxGeometry>` when the route needs them. An edge carries its label either as its own non-empty `value` or in a child `edgeLabel` cell (use the child cell when the label needs an offset away from the line).

## 6. Check the mechanical rules

There is no static validator. Before invoking the reviewer, go through the review checklist below yourself and fix what you find. `c4-reviewer` re-checks all of them.

### Review checklist

- File naming matches the level (`lvl1_v<K>_<name>.drawio`, `step<K>_lvl2_v<N>_<name>.drawio`, `lvl3_v<K>_<aws|azure|k8s>_<name>.drawio`); one `<mxfile>` with one `<diagram>` page; unique cell ids; every edge has a source, a target, and valid waypoints.
- Title block: at Level 1 only `C4 Level 1 - <system name>`; at Level 2 and 3 the level, name, version, status, date, requirements, and ADRs.
- Level 1: exactly one `system` cell; ids `actor-<name>`, `system`, `ext-<name>`; top-down order (actors above the system, externals below), each layer centered horizontally on the page's center axis; actors in a centered row with `mxgraph.c4.person2`, fill `#1F4E79`, and white labels (bold name, `[Person]`, responsibility bullets) vertically centered; the system with `mxgraph.c4.system`, fill `#DAE8FC`, thick solid border, `[Software System]`, and bullet points; externals with `mxgraph.c4.external`, fill `#F5F5F5`, solid border, and `[Software System]`; edges run only `actor → system` and `system → external`, routed orthogonally like circuit-board traces (right-angle paths, no diagonals); lines carry no text — solid = synchronous request, dashed = asynchronous request; a legend box shows the swatches and arrow samples; no requirement IDs, vendor names, or technology tags on the drawing.
- Level 2: one outer system container (light blue, thick border, named after the system) holding three dashed no-fill groups in order (Web app UI, Backend, Repositories (DBs)); every box in exactly one group with a generic `[technology]` line at the end of its label; box labels are bold name / bullets / technology line; edge labels are two lines (action newline `[protocol]`); externals below the block; queues, streams, and brokers appear on the edge, never as boxes. Level 3: the three bands in order (Representation, Business logic, Repository); every box in exactly one band with a `[technology]` tag; business boxes list what they do as bullets; every edge label carries a `[protocol]` tag and an action description; queues, streams, and brokers appear on the edge, never as boxes.
- No vendor or cloud service names at Level 1 and 2; no orphan boxes; no overlapping boxes; no edge crossings; no edge through an unrelated box.

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

The C4 index is the "C4 architecture" table in `README.md`:

- One row per current drawing: title (level, step, version), description, and file URL.
- Only the latest version of each drawing stays in `c4-architecture/`; when a new version replaces an old one, replace the row (git history keeps the old file).
- Do not invent rows for drawings that do not exist.
- Do not mark a drawing `Confirmed` without the user's explicit approval.

## 10. Proceed to the next level

- Level 1 confirmed → ask whether to proceed to Level 2. If yes, propose the slice map (section 4).
- Level 2 confirmed → ask whether to proceed to Level 3. If yes, ask which platform and which slice, then invoke the matching platform architect.
- Level 3 confirmed → stop and report what remains for the other platforms and slices.

## 11. Level 3 handoff

- Invoke `architect-aws`, `architect-azure`, or `architect-k8s` with: the confirmed Level 1 and Level 2 files, the accepted ADRs, this standard, the target slice, and the Level 3 completeness checklist below.
- The architect writes `c4-architecture/lvl3_v<K>_<technology>_<slice>.drawio` and returns the Level 2 → Level 3 mapping, checklist coverage, and open decisions.
- Check the review checklist in section 6, then run `c4-reviewer`, the fix loop, and the same user confirmation gate.
- The platform architect does not mark the drawing confirmed.
- If the architect finds a missing high-level decision, route it to `/create-adr`; do not invent it.

### Level 3 completeness checklist

Use this checklist for every Level 3 drawing; add a note for any item that is not applicable.

- [ ] Region(s) and AZ placement; DR region if the ADR requires it.
- [ ] VPC/VNet, CIDR, subnets (public/private/isolated) with CIDR and AZ.
- [ ] Route tables, internet gateway, NAT gateway, VPC endpoints/private endpoints, peering/hub.
- [ ] Security groups/NSGs with ingress/egress rules; NACLs if used.
- [ ] Load balancer/API gateway, WAF, CDN, DNS, TLS termination and certificates.
- [ ] Identity provider, IAM roles/policies, workload identity, least privilege.
- [ ] Secrets manager, KMS/Key Vault, encryption in transit and at rest.
- [ ] Compute: containers/functions/VMs, autoscaling, GPU pool if self-hosted.
- [ ] Queues/streams/topics named on edges, with DLQ, retention, encryption.
- [ ] Object storage, relational DB, vector DB, search index, cache, audit store, backups, replication, retention/WORM.
- [ ] Model endpoints (LLM, embedding, reranker), model access path, quotas.
- [ ] Observability: logs, metrics, traces, audit export/SIEM, alerting.
- [ ] Egress to external systems, proxy/egress firewall, on-prem connectivity.
- [ ] Every Level 2 element mapped; every edge labelled with `[protocol] action`.

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
