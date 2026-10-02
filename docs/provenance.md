# What this public sample contains

This repository is adapted from Ishaq Zakavi's existing personal knowledge-system
template. It is a fresh public sample, not a copy of a private vault or its Git
history. No employer or client code is intentionally included.

## Carried over and adapted

- Structured note extraction: Markdown section detection, list and checkbox
  parsing, typed decision/risk/action extraction, explicit person annotations
  and source-linked graph enrichment.
- Graph primitives for typed nodes, relationships and source references.
- The reciprocal-rank-fusion approach used to combine retrieval channels.
- The source/curated/atomic/work-product model and distinction between evidence
  and related context.

## Added or changed for this release

- A six-note fictional corpus about a music-production session.
- A small package, loader, CLI and four-tool read-only MCP surface.
- An in-memory lexical index and optional local embedding adapter. The larger
  template's persistent LanceDB indexing implementation is not included.
- Multiple predicates between the same graph nodes, directional lineage and
  deduplicated traversal with explicit bounds.
- Transparent one-based rank components, without the template's tier and
  recency weighting.
- Narrower person linking through explicit assignments. Agreement or a mention
  is not promoted to leadership or responsibility.
- Tests, walkthrough and design documentation.

The public adaptation, documentation and tests were prepared with AI assistance.
This release should not be represented as a historical snapshot of a previously
deployed product or as evidence of production scale.

## Deliberately excluded

Private notes, names, recordings, relationship hypotheses, client examples,
proprietary vocabulary, internal agent instructions, credentials, model caches,
private Git history and research compilations containing third-party material.

There is no real customer data behind the synthetic example. Its numbers and
states are fixtures, not performance metrics or outcomes.
