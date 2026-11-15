# C4 architecture

All C4 drawings for the project live in this folder. They are draw.io XML source, not screenshots. The [ADRs](../ADR/README.md) remain the source of truth for decisions; these drawings show the resulting structure and business flows.

This file is the canonical drawing standard. `/create-c4`, `c4-reviewer`, `architect-aws`, `architect-azure`, and `architect-k8s` all follow it.

## Inputs

Read these before drawing:

1. [REQUIREMENTS.md](../REQUIREMENTS.md) — actors, functional and non-functional requirements.
2. [ARCHITECTURE.md](../ARCHITECTURE.md) — system summary and open decisions.
3. [ADR/README.md](../ADR/README.md) and every accepted ADR.
4. The project walkthrough PDF in `ADR/` — including its hand-drawn flows.
5. [src/README.md](../src/README.md) and [infra/README.md](../infra/README.md).
6. Every existing `c4-architecture/*.xml` and the index below.

If the walkthrough PDF has no text layer, render its pages to images first (for example with PyMuPDF `page.get_pixmap()` at 140–260 DPI, rotating landscape pages), then read the images. Do not guess at a drawing you have not read.

## Folder and file conventions

- This is the only architecture drawing folder. There is no `ARCHITECTURE/` folder.
- Level 1 and 2: `lvl<N>_v<K>_<drawing_name>.xml` — for example `lvl1_v1_system_context.xml`, `lvl2_v1_query_answering.xml`.
- Level 3: `lvl3_v<K>_<technology>_<drawing_name>.xml` — technology is `aws`, `azure`, or `k8s`; for example `lvl3_v1_aws_query_answering.xml`.
- `<drawing_name>` is lowercase snake_case. One drawing per file. One `<diagram>` page per file.
- The XML is the source of truth. A PNG is optional; never commit a PNG without its XML, and never claim a render that does not exist.
- Versions are never overwritten once confirmed. A material change creates a new version file; the index marks the old one `Superseded by <file>`.
- Status values: `Draft`, `In review`, `Confirmed`, `Superseded by <file>`.
- Every drawing carries a title block with level, name, version, status, date, requirements covered, and ADRs referenced.

## Drawing standard

These rules apply to every level.

### Layout

1. At Level 2 and Level 3, use three full-width bands, in this order, top to bottom: **Representation**, **Business logic**, **Repository**.
   - Representation: UI, API gateway, edge/streaming gateway, identity entry point, external-facing adapters.
   - Business logic: services, workers, orchestrators, model and reranker endpoints, domain logic. Split services the way the service architecture splits them.
   - Repository: databases, vector stores, search indexes, object storage, caches, audit stores.
2. Keep the bands aligned and in the order above. Do not reorder for convenience.
3. At Level 2 and Level 3, every box sits in exactly one band. Neighbouring system slices, external systems, and actors sit outside the bands, at the left or right edge, in the row where they interact. At Level 1, use the top-down actor → system → external layout in the Level 1 section.
4. No line intersections. No edge may cross another edge, and no edge may pass through an unrelated box. Use orthogonal routing, dedicated channels, and explicit waypoints. If a crossing cannot be removed, split the drawing by slice or flow instead of accepting it.
5. No overlapping boxes. Leave enough space for labels.
6. Edge labels sit near the middle of the edge, offset from the line. They must not overlap another edge or box.

### Lines

1. Every edge has a label that states what is happening, using a verb: `get document metadata`, `submit question`, `read permitted chunks`, `publish chunk.ready`.
2. At Level 2 and Level 3, prefix the label with the communication protocol or connection type in square brackets: `[http] submit question`, `[sql] read chunk permissions`, `[queue message] document.uploaded`, `[event stream] chunk.indexed`. At Level 1, put the description first and the communication type in brackets after it: `submit documents [http]`, `request embeddings [http]`.
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
- Level 2 and Level 3 use a restrained palette: one neutral fill for representation, one for business, one for repository, grey for external systems, white for notes. Bands are swimlane or group containers with a visible title. Do not encode meaning in colour alone; the band label and the box label carry the meaning.

## Level 1 — System context

Level 1 is top-down: **actors on top, the own system in the middle, external systems at the bottom**. The flow is the initial request only: actors → system, system → external systems. Do not draw return lines or responses.

Use the ids `actor-<name>`, `system`, and `ext-<name>` for the three rows. The validator uses them to check the order, the colours, and the edge directions.

Use the draw.io C4 shape set for the three rows:

- **Actors (top, darker blue)** — `shape=mxgraph.c4.person2` (the C4 person icon, not `umlActor` or a stick figure). Use as many actors as the requirements need. Each actor is a box, not just a name: the box contains the actor name and bullet points describing what the actor does in the system. Use `fillColor=#1F4E79`, white text.
- **Own system (middle, light blue)** — `shape=mxgraph.c4.system`. Exactly one black box for this project. The box contains the system name (for example "Enterprise RAG knowledge assistant") and bullet points describing what the system as a whole does. Use `fillColor=#DAE8FC`, a thick border, and dark text. Do not show containers, services, databases, or technology tags.
- **External systems (bottom, light gray)** — `shape=mxgraph.c4.external`. The systems the platform calls or exchanges data with, outside its boundary. Each is a simple labelled box; no bullets are required. Use `fillColor=#F5F5F5` and a dashed border.
- **Lines** — one line per initial request, pointing downward: actor → system, or system → external system. No return lines and no responses. Label every line with the description first and the communication type in brackets, for example `submit documents [http]`, `request embeddings [http]`. Use a generic communication type, not a vendor or protocol stack.
- **Notes** — build-time roles and interactions not visible at runtime (for example the FR-02 retrieval engineer) go in a `note-*` cell, not in an actor box.

Rules:

- Exactly one own-system black box. Multiple black boxes are only allowed in a multi-system context the user explicitly agrees to; they are not the default for this project.
- Do not show containers, services, databases, cloud services, or technology tags in `[]`.
- Every actor and external system in the requirements appears, or its absence is justified in a note.
- No line crossings, no overlapping boxes, no edge through an unrelated box.
- Top-down order: every actor box sits above the system box; every external box sits below it.
- The actor and system boxes contain bullets; a box with only a name is incomplete.

## Level 2 — Container and business-flow slices

One drawing per slice. The slice map is agreed with the user before drawing. A typical map for this project:

- Document ingestion and processing
- Indexing and retrieval
- Query and answer generation
- Governance, audit, and evaluation

Each drawing shows the slice's inner representation, business-logic, and repository elements, plus the neighbouring slices, actors, and external systems at the boundary. Keep the three bands. The lines are the business flow. The business blocks list their capabilities.

Rules:

- Generic technology categories only, in `[]`. No vendor or product names.
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

Level 3 is platform-specific and is produced by `architect-aws`, `architect-azure`, or `architect-k8s` after Level 1 and Level 2 are confirmed. `/create-c4` runs the same validation and review gate.

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
3. The command runs `.claude/scripts/validate_c4_drawio.py <file> --level <n>` and fixes every Blocking finding.
4. The command invokes `c4-reviewer` (read-only). Findings are classified Blocking, Major, Minor. The command asks which to fix and repeats until no Blocking or Major findings remain. If the same finding survives two rounds, stop and ask the user.
5. Only after the review is clean, the command asks the user to confirm the drawing. The status becomes `Confirmed` only with explicit approval. If the user rejects it, capture the feedback, fix, re-review, and ask again.
6. After confirmation, update the index and proceed to the next level only with the user's go-ahead.
7. Level 3: `/create-c4` asks which platform and slice, invokes the matching platform architect, then runs the validator, `c4-reviewer`, the fix loop, and the confirmation gate.

A drawing is never `Confirmed` because the reviewer said `Accept`; it is `Confirmed` because the user approved it.

## Index

The index is the authoritative list of drawings and their status. `/create-c4` updates it; do not hand-edit status.

| Level | Version | Drawing | File | Scope | Covers | ADRs | Status | Confirmed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | v1 | System context | [lvl1_v1_system_context.xml](lvl1_v1_system_context.xml) | Whole system | FR-01 to FR-08, NFR-01 to NFR-08 | — | In review | — |

## Validation

The validator checks the mechanical rules in this standard: file naming, XML shape, one page, cell IDs, edge endpoints and labels, protocol tags at Level 2 and 3, the three bands and their order, technology tags, business bullets, vendor-name leakage at Level 1 and 2, queue boxes, overlapping boxes, edge crossings, edges through boxes, orphan boxes, and the title block. It is not a substitute for `c4-reviewer`; the reviewer checks meaning, completeness, and consistency with the requirements and ADRs.

Run it as:

```bash
python .claude/scripts/validate_c4_drawio.py c4-architecture/lvl2_v1_query_answering.xml --level 2
```

## XML skeleton

Use this shape for every drawing. The band IDs and the `title` ID are required by the validator.

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
        <mxCell id="band-representation" value="Representation" style="swimlane;html=1;startSize=26;container=1;collapsible=0;fillColor=#dae8fc;strokeColor=#6c8ebf;verticalAlign=top;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="40" y="60" width="1520" height="180" as="geometry" />
        </mxCell>
        <mxCell id="band-business" value="Business logic" style="swimlane;html=1;startSize=26;container=1;collapsible=0;fillColor=#d5e8d4;strokeColor=#82b366;verticalAlign=top;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="40" y="260" width="1520" height="300" as="geometry" />
        </mxCell>
        <mxCell id="band-repository" value="Repository" style="swimlane;html=1;startSize=26;container=1;collapsible=0;fillColor=#ffe6cc;strokeColor=#d79b00;verticalAlign=top;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="40" y="580" width="1520" height="200" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

Boxes inside a band use `parent="band-representation"`, `parent="band-business"`, or `parent="band-repository"`. Edges use `parent="1"`, a `source`, a `target`, a non-empty `value`, and waypoints in the edge `<mxGeometry>` when the route needs them.
