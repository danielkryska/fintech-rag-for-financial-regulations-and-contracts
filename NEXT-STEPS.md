# Next steps (handoff)

Temporary handoff note for continuing on another machine. The canonical rules are in [c4-architecture/README.md](c4-architecture/README.md), [AGENTS.md](AGENTS.md), and the ADRs. Delete this file once the Level 1 drawing is confirmed.

## Current state

- The C4 workflow is in place:
  - `/create-c4` command.
  - `c4-reviewer` agent.
  - `.claude/scripts/validate_c4_drawio.py`.
  - The old architecture folder was removed; all C4 drawings live in `c4-architecture/`.
- The Level 1 guide now reflects the latest user rules:
  - Top-down: actors on top, one own-system black box in the middle, external systems at the bottom.
  - Multiple actors are fine; exactly one own-system black box for this project.
  - Actors and the system box show a name plus bullets. Actors use the draw.io C4 person shape (`mxgraph.c4.person2`); the system uses `mxgraph.c4.system`; external systems use `mxgraph.c4.external`.
  - Colours: actors `#1F4E79` with white text, system `#DAE8FC`, external systems `#F5F5F5`.
  - Lines are initial requests only, pointing downward: actor → system, system → external. No return lines or responses.
  - Line labels are `description [communication type]`, for example `submit documents [http]`.
- `AGENTS.md`, `ARCHITECTURE.md`, `ADR/README.md`, `/create-adr`, `adr-reviewer`, and the platform architects point at `c4-architecture/` and the new C4 process.
- `c4-reviewer` has been updated for the new Level 1 rules.

## What is not finished

1. **Validator Level 1 checks.** `validate_c4_drawio.py` still has the earlier Level 1 checks. Add checks for:
   - exactly one `system` cell;
   - ids `actor-*`, `system`, and `ext-*`;
   - top-down order: every actor box above the system, every external box below it;
   - actor and system boxes contain bullet points;
   - C4 shapes: `mxgraph.c4.person2` for actors, `mxgraph.c4.system` for the system, `mxgraph.c4.external` for external systems;
   - colours: actors `#1F4E79`, system `#DAE8FC`, external `#F5F5F5`;
   - edge directions: only `actor-*` → `system` and `system` → `ext-*`;
   - a `[communication type]` tag on every Level 1 edge.
   `c4-architecture/README.md` is the source of truth; the validator should mirror it.
2. **Level 1 drawing.** `c4-architecture/lvl1_v1_system_context.xml` is still the earlier three-black-box, left-to-right version with return lines and `umlActor` actors. It is `In review`, not `Confirmed`. Redraw it to the new standard:
   - one `system` box, "Enterprise RAG knowledge assistant", with system-wide bullets;
   - six actor boxes (`actor-employee`, `actor-records`, `actor-compliance`, `actor-reviewer`, `actor-access`, `actor-operator`) with actor bullets and the C4 person shape;
   - five external boxes (`ext-source`, `ext-model`, `ext-idp`, `ext-siem`, `ext-ci`) with the C4 external shape;
   - 11 downward initial-request edges with `description [http]` labels and no return lines;
   - the colours and top-down layout above;
   - notes for the FR-02 retrieval engineer and the reviewer's answer-review path.
3. **Review and confirm.**
   - Run `python .claude/scripts/validate_c4_drawio.py c4-architecture/lvl1_v1_system_context.xml --level 1`.
   - Run `c4-reviewer`; fix every Blocking and Major finding; re-review.
   - Ask the user to confirm. Only explicit user approval sets the title and C4 index to `Confirmed`.
4. **Level 2.** After Level 1 is confirmed, run `/create-c4` and propose the Level 2 slice map: ingestion/processing, indexing/retrieval, query/answering, and governance/audit/evaluation.
5. **Level 3.** After Level 2 is confirmed, use `architect-aws`, `architect-azure`, or `architect-k8s` for `lvl3_v<K>_<technology>_<drawing_name>.xml`.

## Do not

- Do not mark the Level 1 drawing `Confirmed` without explicit user approval.
- Do not commit a PNG without its XML source or claim a render that does not exist.
- Do not add specific cloud services to Level 1 or Level 2.
- Do not recreate the old architecture folder.
