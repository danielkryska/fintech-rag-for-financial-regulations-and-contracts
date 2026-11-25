# C4 architecture

All C4 drawings for the project live in this folder. They are draw.io XML source, not screenshots. The [ADRs](../ADR/README.md) remain the source of truth for decisions; these drawings show the resulting structure and business flows.

This file is the canonical drawing standard. `/create-c4`, `c4-reviewer`, `architect-aws`, `architect-azure`, and `architect-k8s` all follow it.

## Inputs

Read these before drawing:

1. [REQUIREMENTS.md](../REQUIREMENTS.md) — actors, functional and non-functional requirements.
2. [ARCHITECTURE.md](../ARCHITECTURE.md) — system summary and open decisions.
3. [ADR/README.md](../ADR/README.md) and every accepted ADR.
4. The project walkthrough PDF in this folder and in `ADR/` — including its hand-drawn flows.
5. [src/README.md](../src/README.md) and [infra/README.md](../infra/README.md).
6. Every existing `c4-architecture/*.drawio` and the index below.

If the walkthrough PDF has no text layer, render its pages to images first (for example with PyMuPDF `page.get_pixmap()` at 140–260 DPI, rotating landscape pages), then read the images. Do not guess at a drawing you have not read.

## Folder and file conventions

- This is the only architecture drawing folder. There is no `ARCHITECTURE/` folder.
- Level 1: `lvl1_v<K>_<drawing_name>.drawio` — for example `lvl1_v3_system_context.drawio`. Level 2: `step<K>_lvl2_v<N>_<drawing_name>.drawio`, where K is the slice step (1 = document ingestion, 2 = embed and index, 3 = retrieve and generate, 4 = stream and authorize) — for example `step3_lvl2_v4_retrieve-generate-stream.drawio`.
- Level 3: `lvl3_v<K>_<technology>_<drawing_name>.drawio` — technology is `aws`, `azure`, or `k8s`; for example `lvl3_v1_aws_query_answering.drawio`.
- `<drawing_name>` is lowercase snake_case. One drawing per file. One `<diagram>` page per file.
- The XML is the source of truth. A PNG is optional; never commit a PNG without its XML, and never claim a render that does not exist.
- Versions are never overwritten once confirmed. A material change creates a new version file; the index marks the old one `Superseded by <file>`.
- Status values: `Draft`, `In review`, `Confirmed`, `Superseded by <file>`.
- Every drawing carries a title block: Level 1 drawings carry only `C4 Level 1 - <system name>` in the top-left corner (version, status, date, requirements, and ADRs live in the index); Level 2 and 3 drawings carry level, name, version, status, date, requirements covered, and ADRs referenced.

## Drawing standard

These rules apply to every level.

### Layout

1. At Level 2, use one outer system container with three dashed groups inside, top to bottom: **Web app UI** (representation), **Backend**, **Repositories (DBs)** — see the Level 2 section. At Level 3, use three full-width bands in this order: **Representation**, **Business logic**, **Repository**.
   - Representation: UI, API gateway, edge/streaming gateway, identity entry point, external-facing adapters.
   - Business logic: services, workers, orchestrators, model and reranker endpoints, domain logic. Split services the way the service architecture splits them.
   - Repository: databases, vector stores, search indexes, object storage, caches, audit stores.
2. Keep the groups or bands aligned and in the order above. Do not reorder for convenience.
3. At Level 2 and Level 3, every box sits in exactly one group or band. Neighbouring system slices, external systems, and actors sit outside the groups or bands, at the left or right edge, in the row where they interact — external systems sit below the block at Level 2. At Level 1, use the top-down actor → system → external layout in the Level 1 section.
4. No line intersections. No edge may cross another edge, and no edge may pass through an unrelated box. Use orthogonal routing, dedicated channels, and explicit waypoints. If a crossing cannot be removed, split the drawing by slice or flow instead of accepting it.
5. No overlapping boxes. Leave enough space for labels.
6. Edge labels sit near the middle of the edge, offset from the line. They must not overlap another edge or box.

### Lines

1. Every edge at Level 2 and Level 3 has a label that states what is happening, using a verb: `get document metadata`, `submit question`, `read permitted chunks`, `publish chunk.ready`. At Level 2 the label is two lines: the action on the first line, the protocol tag on the second (`POST /documents` newline `[http]`).
2. At Level 2 and Level 3, the label carries the communication protocol or connection type in square brackets: `[http] submit question`, `[sql] read chunk permissions`, `[queue message] document.uploaded`, `[event stream] chunk.indexed`. Level 1 lines carry no text; the line style carries the meaning: solid = synchronous request, dashed = asynchronous request. At Level 2, solid and dashed lines also mark sync vs async.
3. Show direction with the arrowhead. Bidirectional interactions use two labelled edges, not an unlabelled double arrow.
4. Queues, brokers, event streams, buses, and topics are **not boxes**. Show them on the edge: `[queue message]`, `[event stream]`, `[broker message]`. At Level 3, name the specific technology in the tag (`[SQS queue message]`, `[Kafka event stream]`) and put retention, DLQ, and encryption details in a note, not a box.
5. Every box is connected to the flow. No orphan boxes and no dangling edges.
6. Where one flow dominates, number the edge labels in order (`1. [http] ...`, `2. [queue message] ...`) so the drawing reads as a business flow.

### Box content

1. System elements carry a generic technology category in square brackets at Level 2: `[web ui]`, `[api gateway]`, `[service]`, `[worker]`, `[orchestrator]`, `[model endpoint]`, `[vector db]`, `[object storage]`, `[relational db]`, `[search index]`, `[key-value store]`, `[audit store]`.
2. Business-logic blocks contain bullet points describing what the block does, in business terms: what it validates, what it filters, what it authorizes, what it searches, what it assembles, what it stores. Do not put implementation detail in the bullets.
3. One clear responsibility per block. If a block needs more than about five bullets, split it.
4. No secrets, credentials, account IDs, tokens, or real personal data.

### Shape and colour

- Use the draw.io C4 shape set for C4 elements: `mxgraph.c4.person2` for actors, `mxgraph.c4.system` for the own system, `mxgraph.c4.external` for external systems, and the C4 container, component, and database shapes where they fit at Level 2 and Level 3. Use plain draw.io shapes only when the C4 stencil has no match; platform Level 3 drawings use the official platform shapes for services.
- Level 1 colours: actors `#1F4E79` with white text, own system `#DAE8FC`, external systems `#F5F5F5`.
- Level 2 and Level 3 use a restrained palette: one neutral fill for representation, one for business, one for repository, grey for external systems, white for notes. The Level 2 groups are dashed containers with no fill and a visible title; the Level 2 outer block is light blue like the Level 1 system box. Do not encode meaning in colour alone; the group label and the box label carry the meaning.

## Level 1 — System context

Level 1 is top-down: **actors in a row on top, the own system in the middle, external systems at the bottom**. Each layer is centered horizontally on the page's center axis. The flow is the initial request only: actors → system, system → external systems. Do not draw return lines or responses.

Use the ids `actor-<name>`, `system`, and `ext-<name>` for the three rows. The review checklist uses them to check the order, the colours, and the edge directions.

Use the draw.io C4 shape set for the three rows:

- **Actors (top, darker blue)** — `shape=mxgraph.c4.person2`, in one row centered on the page, no container box. Each actor box shows the actor name (bold), the type tag `[Person]`, and the actor's responsibilities as bullet points, vertically centered, in white (`fontColor=#ffffff`). Use an HTML label with an explicit white colour on the name span — the `<b>` tag renders an unreadable grey in some viewers, so bold the name with `&lt;span style="color:#ffffff;font-weight:bold"&gt;` instead. Fill `#1F4E79`.
- **Own system (middle, light blue)** — `shape=mxgraph.c4.system`. Exactly one black box for this project. The box shows the system name, the type tag `[Software System]`, and bullet points describing what the system as a whole does — one feature per bullet, in business terms (what happens, not how; no implementation details such as retrieval algorithms or parsing techniques). Use `fillColor=#DAE8FC`, a thick solid border, and dark text. Do not show containers, services, or databases.
- **External systems (bottom, light gray)** — `shape=mxgraph.c4.external`. The systems the platform calls or exchanges data with, outside its boundary. Each box shows the name, the type tag `[Software System]`, and a one-line description. Use `fillColor=#F5F5F5` and a **solid** border, like the own system but gray.
- **Lines** — one line per initial request, pointing downward: actor → system, or system → external system. **Level 1 lines carry no text.** The line style carries the communication type: solid line = synchronous request, dashed line = asynchronous request. No return lines and no responses.
- **Legend** — a legend box with small colour swatches (actor, software system, external software system) and two arrow samples: solid = synchronous request, dashed = asynchronous request.
- **Title block** — top-left corner: `C4 Level 1 - <system name>` only. Version, status, date, requirements, and ADRs live in the index, not on the drawing.
- **Notes** — build-time roles and interactions not visible at runtime go in a `note-*` cell, or are merged into an actor when the user consolidates roles. Do not mention requirement IDs (FR-…, NFR-…, EVAL-…) on the drawing; the index records the coverage.

Rules:

- Exactly one own-system black box. Multiple black boxes are only allowed in a multi-system context the user explicitly agrees to; they are not the default for this project.
- Do not show containers, services, databases, cloud services, or technology tags in `[]`; only the type tags `[Person]` and `[Software System]` are allowed.
- Every actor and external system in the requirements appears, or its absence is justified in a note.
- No line crossings, no overlapping boxes, no edge through an unrelated box.
- Top-down order: every actor box sits above the system box; every external box sits below it.
- The actor and system boxes contain bullets; each actor box shows the name (bold), `[Person]`, and responsibility bullets. A box with only a name is incomplete.
- The external boxes use solid borders; the actor boxes sit in one centered row with no container around them (the legend explains the colours).

## Level 2 — Container and business-flow slices

One drawing per slice. The slice map is agreed with the user before drawing. A typical map for this project:

- Step 1 — Document ingestion (upload, registration, hierarchical chunking)
- Step 2 — Embed and index (event-driven, no user involved)
- Step 3 — Retrieve, generate, cite, stream, authorize (question and answer path)
- Step 4 — Stream and authorize

**Structure** — the drawing follows the c4model.com container-diagram pattern:

- One outer container box named after the system (for example "Enterprise RAG knowledge assistant"): light blue fill `#DAE8FC`, thick border, like the Level 1 black box.
- Inside it, three groups with **dashed** lines and **no fill colour**: `Web app UI` (representation) on top, `Backend` in the middle, `Repositories (DBs)` at the bottom. Use ids `sys-container`, `grp-ui`, `grp-backend`, `grp-repos`.
- Actors above the outer block; external systems **below** the block, connected with labelled edges.
- The lines are the business flow, routed orthogonally like circuit-board traces — right angles only, no diagonals, no crossings.

**Box labels** — three parts, each on its own line: **bold module name**, bullet points of what the block does or keeps, and the generic technology type in brackets on the last line (for example `[worker]`, `[service]`, `[web ui]`, `[object storage]`, `[vector db]`, `[audit store]`).

**Edge labels** — two lines: the action on the first line, the protocol on the second, for example:

```
POST /documents
[http]
```

Sync and async use different line styles (solid vs dashed), and the legend explains them.

Rules:

- Generic technology categories only, in `[]`. No vendor, product, or platform names and no solution selection.
- No queue, stream, or broker boxes; use `[queue message]`, `[event stream]`, `[broker message]` on the edges.
- Cover the slice end to end: the trigger, the representation entry point, the business steps, the repositories read or written, the response or event, and the failure or fallback path where the requirements define one.
- Show permission filtering, PII handling, audit writes, and other controls at the point where they happen; do not hide them in a note.
- A cross-slice interaction is a labelled edge to a grey boundary box for the neighbouring slice. Do not draw the neighbour's internals in this slice.
- The slice map, the requirements covered, and the ADRs referenced are recorded in the index.

### Source business flows

The Level 2 slices must cover two end-to-end flows and their exception paths. Draw them in draw.io; do not add Mermaid or another diagram format.

**Ingestion:** document sources (PDF, DOCX, scans) → parse with OCR fallback → PII detection and redaction → adaptive chunking (hierarchical, semantic, fixed) → vector and keyword indexes with ACL metadata.

**Query and answer:** employee question → query preprocessing (PII redaction, entitlement lookup) → hybrid retrieval (keyword and semantic) over the permission-scoped index → rerank and metadata filter → sufficient-context decision → grounded answer with inline citations, or an explicit insufficient-context response → audit log (sources, provenance, token accounting) → user feedback → evaluation set (RAG Triad, regression CI) → back to retrieval.

**Exception paths to show where they occur:** OCR failure, malformed or poisoned document, retrieval outage, model timeout, budget exhaustion, and permission-denied query.

## Level 3 — Platform realisation

Level 3 is platform-specific and is produced by `architect-aws`, `architect-azure`, or `architect-k8s` after Level 1 and Level 2 are confirmed. `/create-c4` runs the same review gate.

Show:

- Specific products and services, with official platform shapes where draw.io provides them.
- The three bands, plus the platform topology around them: region(s), availability zones, VPC/VNet and CIDR, public/private/isolated subnets with CIDR and AZ, route tables and routes, internet gateway, NAT gateway(s), VPC endpoints/private endpoints, peering/Transit Gateway/hub, security groups/NSGs and their ingress/egress rules, load balancer/API gateway, WAF, DNS, certificates, identity and IAM roles/policies, secrets and keys, compute units and autoscaling, model endpoints, data stores, backup/DR and replication, observability and audit export.
- Every external-internet path, every private path, and every trust boundary.
- The queue or stream technology on the edge label, with DLQ, retention, and encryption in a note, not as a box.
- Every Level 2 element mapped to a Level 3 component. The mapping matrix is part of the drawing's notes or the command output.

Rules:

- No Level 2 element may silently disappear. If a component is not applicable on this platform, record why.
- No line crossings; split the Level 3 drawing by slice if the topology does not fit.
- Never fabricate a PNG. The XML is the deliverable; export only when the draw.io CLI is available.
- The platform architect does not mark the drawing `Confirmed`; `/create-c4` asks the user.

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

## Process and gates

1. Run `/create-c4`.
2. The command draws the requested level, or the next unconfirmed level, using the inputs above.
3. The command invokes `c4-reviewer` (read-only), which checks the mechanical rules in the review checklist above plus the semantic dimensions. Findings are classified Blocking, Major, Minor. The command asks which to fix and repeats until no Blocking or Major findings remain. If the same finding survives two rounds, stop and ask the user.
4. Only after the review is clean, the command asks the user to confirm the drawing. The status becomes `Confirmed` only with explicit approval. If the user rejects it, capture the feedback, fix, re-review, and ask again.
5. After confirmation, update the index and proceed to the next level only with the user's go-ahead.
6. Level 3: `/create-c4` asks which platform and slice, invokes the matching platform architect, then runs `c4-reviewer`, the fix loop, and the confirmation gate.

A drawing is never `Confirmed` because the reviewer said `Accept`; it is `Confirmed` because the user approved it.

## Index

The index is the authoritative list of drawings and their status. `/create-c4` updates it; do not hand-edit status.

| Level | Version | Drawing | File | Scope | Covers | ADRs | Status | Confirmed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | v3 | System context | [lvl1_v3_system_context.drawio](lvl1_v3_system_context.drawio) | Whole system: who uses the assistant and which external systems it depends on | FR-01 to FR-08, NFR-01 to NFR-08 | — | Draft | — |
| 2 | v6 | Document ingestion (step 1) | [step1_lvl2_v6_document-ingestion.drawio](step1_lvl2_v6_document-ingestion.drawio) | Slice: upload, registration, hierarchical chunking, processed store, hand-off to step 2 | FR-01, FR-02, NFR-03, NFR-06 | — | Draft | — |
| 2 | v2 | Embed and index (step 2) | [step2_lvl2_v2_embed-and-index.drawio](step2_lvl2_v2_embed-and-index.drawio) | Slice: indexing coordinator, embedding, index writes to vector DB, keyword index, and chunk store; event-driven, no user involved | FR-02, FR-03, FR-04, NFR-03, NFR-04, NFR-06, NFR-07 | — | Draft | — |
| 2 | v4 | Retrieve, generate, cite, stream, authorize (step 3) | [step3_lvl2_v4_retrieve-generate-stream.drawio](step3_lvl2_v4_retrieve-generate-stream.drawio) | Slice: question path (gateway, BFF, query preparation, retrieve & rerank, context builder, answer worker) and answer path (PII re-hydration, SSE streaming) | FR-03 to FR-08, NFR-01 to NFR-03, NFR-05 to NFR-08 | — | Draft | — |
| 2 | v1 | Stream and authorize (step 4) | [step4_lvl2_v1_stream-and-authorize.drawio](step4_lvl2_v1_stream-and-authorize.drawio) | Slice: query workers, answer events, edge streaming service, SSE to the browser | FR-05, FR-08, NFR-01, NFR-02, NFR-06, NFR-07 | — | Draft | — |

## Review checklist

There is no static validator. `c4-reviewer` checks the mechanical rules in this standard by reading the XML, together with the semantic review of meaning, completeness, and consistency with the requirements and ADRs. Before confirming a drawing, the reviewer goes through:

- File naming matches the level (`lvl1_v<K>_<name>.drawio`, `step<K>_lvl2_v<N>_<name>.drawio`, `lvl3_v<K>_<aws|azure|k8s>_<name>.drawio`); one `<mxfile>` with one `<diagram>` page; unique cell ids; every edge has a source, a target, and valid waypoints.
- Title block: at Level 1 only `C4 Level 1 - <system name>`; at Level 2 and 3 the level, name, version, status, date, requirements, and ADRs.
- Level 1: exactly one `system` cell; ids `actor-<name>`, `system`, `ext-<name>`; top-down order (actors above the system, externals below), each layer centered horizontally on the page's center axis; actors in a centered row with `mxgraph.c4.person2`, fill `#1F4E79`, and white labels (bold name, `[Person]`, responsibility bullets) vertically centered; the system with `mxgraph.c4.system`, fill `#DAE8FC`, thick solid border, `[Software System]`, and bullet points; externals with `mxgraph.c4.external`, fill `#F5F5F5`, solid border, and `[Software System]`; edges run only `actor → system` and `system → external`, routed orthogonally like circuit-board traces (right-angle paths, no diagonals); lines carry no text — solid = synchronous request, dashed = asynchronous request; a legend box shows the swatches and arrow samples; no requirement IDs, vendor names, or technology tags on the drawing.
- Level 2: one outer system container (light blue, thick border, named after the system) holding three dashed no-fill groups in order (Web app UI, Backend, Repositories (DBs)); every box in exactly one group with a generic `[technology]` line at the end of its label; box labels are bold name / bullets / technology line; edge labels are two lines (action newline `[protocol]`); externals below the block; queues, streams, and brokers appear on the edge, never as boxes. Level 3: the three bands in order (Representation, Business logic, Repository); every box in exactly one band with a generic `[technology]` tag; business boxes list what they do as bullets; every edge label carries a `[protocol]` tag and an action description; queues, streams, and brokers appear on the edge, never as boxes.
- No vendor or cloud service names at Level 1 and 2; no orphan boxes; no overlapping boxes; no edge crossings; no edge through an unrelated box.

The semantic review dimensions (level correctness, slice completeness, consistency with the requirements and ADRs, safety) are in `.claude/agents/c4-reviewer.md`.

## XML skeleton

Use this shape for every drawing. The `title` ID is required by the review checklist. Level 2 uses one outer `sys-container` with three dashed no-fill groups inside it (`grp-ui`, `grp-backend`, `grp-repos`); Level 3 uses the three band IDs below.

```xml
<mxfile host="app.diagrams.net">
  <diagram id="lvl2-query-answering" name="L2 Query and answer generation">
    <mxGraphModel grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1200" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="title" value="C4 Level 2 - Query and answer generation (v1, Draft)" style="text;html=1;align=left;verticalAlign=top;fontSize=18;fontStyle=1;" vertex="1" parent="1">
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
