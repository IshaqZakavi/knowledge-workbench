# Folder structure and the later vault form

The public root follows the original project-work template rather than hiding
records inside a Python package's `data/` directory.

## Original template contract

| Folder | Role | In this release |
| --- | --- | --- |
| `notes/raw/.originals/` | Permitted original non-Markdown captures | Boundary documentation; no originals |
| `notes/raw/` | Normalized source text | Fictional transcript and email |
| `notes/curated/` | Comprehensive structured records, mirrored 1:1 | Both sources have matching `-CURATED.md` files |
| `notes/atomic/` | Selective reusable insights | One sourced idea; no atom for routine coordination |
| `reference/people/` | Canonical names, aliases, observations and hypotheses | Two invented people |
| `reference/processes/` | Expected workflow | An evidence-to-brief process |
| `reference/process-runs/` | Evidence of a particular execution | One explicitly partial example |
| `reference/terms/` | Canonical vocabulary | A lineage term |
| `reference/architecture-patterns/` | Problem, forces and reusable design | Review-before-routing pattern |
| `goals/` | Durable outcome | A reviewable pilot decision |
| `backlog-items/` | Work thread under a goal | Preparing a decision brief |
| `work-items/` | Accepted active work | Source comparison, still in progress |
| `work-products/` | Draft/output for a particular audience | Cited decision brief |
| `context/manifests/` | A chosen source bundle | Documented contract, no generated bundle |
| `published/` | Reviewed outward context | Separate manifests/exports/consumers; no approval implied |
| `ops/` | Proposals and pending external effects | Documented boundaries; no executor |

The last operational areas also appear in the broader operator-system design.
Their presence here is a documented scaffold, not a claim that this Python
example implements the full control plane.

## Later shape: stages across domains

The same project developed a shared TypeScript protocol with tenant-specific
vaults. A domain gets the same five-stage structure:

```text
<workspace>/
  vault.yaml
  <domain>/
    1-original/
    2-raw/
    3-curated/
    4-atomic/
    5-work-products/
  reference/
  ops/
  .stores/                 Derived retrieval/graph/insight projections
  .sync/                   Incremental sync state
```

For example, research and writing can have separate domains while sharing stage
semantics. Separate personal and professional vaults are a further boundary,
not just different tags within one unrestricted search pool.

| Original form | Later form |
| --- | --- |
| `notes/raw/.originals/` | `<domain>/1-original/` |
| `notes/raw/` | `<domain>/2-raw/` |
| `notes/curated/` | `<domain>/3-curated/` |
| `notes/atomic/` | `<domain>/4-atomic/` |
| `work-products/` | `<domain>/5-work-products/` |

This is a medallion-like refinement model, adapted to knowledge work rather than
a claim of a deployed data lakehouse. Sources, interpretations and reusable
knowledge remain distinguishable as they become useful outputs.

## Identity and metadata

The original contract uses title/status, known dates and contributors, `origin`,
`related`, `supporting`, project vocabulary and typed object fields. The public
validator uses that actual selected schema with a fictional project registry.

The later envelope adds stable IDs distinct from human-readable slugs, prior
paths, schema/protocol versions, vault, domain, stage, sensitivity and explicit
share lists. Those formats should not be casually mixed. A migration must
preserve identity and source links instead of renaming folders and hoping the
indexes still agree.

In this public adapter, `origin` is direct derivation; `supporting` lists other
evidence; `related` carries broader context. The original composition guidance
also used `related` as a source list. This stricter distinction is an explicit
adaptation so related work is not automatically treated as evidentiary support.
