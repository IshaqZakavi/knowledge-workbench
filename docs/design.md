# Design: sources, interpretations and relationships

The larger project explores a personal agentic operating-system template for
knowledge work. Notes are one input. People, decisions, processes, tasks and
goals provide context for what to do with that information.

This repository makes a small, working slice of that design available for
inspection. It keeps the executable behavior separate from the broader ambition.

## Layers have different responsibilities

| Layer | Purpose | What can go wrong |
| --- | --- | --- |
| Raw | Preserve a permitted original record | Capturing material that should never have been retained |
| Curated | Make an interpretation and its source explicit | Turning an uncertain statement into a fact |
| Atomic | Extract an idea worth reusing | Generalizing one experience too far |
| Work product | Answer a question for a particular audience | Sharing private context or presenting stale state as current |

This resembles a medallion-style separation of source and derived material,
adapted to knowledge work. The additional atomic layer is selective. Every
meeting does not need to become a universal principle.

In this example the notes are authored fixtures. There is no automated curation
pipeline or claim that every work-product sentence has a verified citation.
`origin` records declared derivation. A person still has to assess whether the
source actually supports the claim.

## Metadata is a small contract

Each note declares its ID, title, tier, date, contributors, origins and related
notes. Loading rejects unknown fields, duplicate IDs and unresolved links.
Source cycles are rejected when the graph is built.

Known note IDs are also the read interface. The MCP server does not accept a
vault path, remote URL or client-supplied corpus. That narrow boundary is useful
for a public demo. It is not a replacement for authentication in a larger system.

## Three ways to find context

**Lexical retrieval** preserves exact vocabulary and identifiers. This demo uses
term frequency and inverse document frequency. It is not BM25 or the full
template's persistent search index.

**Semantic retrieval** uses a pinned local Sentence Transformers model. Vectors
are normalized and compared with a dot product. This is an optional in-memory
adapter, not a hosted vector database. Long documents would require a real
chunking policy; these fixtures are intentionally short.

**Graph traversal** follows explicit typed edges. NetworkX is an in-memory graph
library here, not a separately operated graph-database service. The graph can
answer structural questions that similarity alone does not encode.

Rank fusion combines lexical and vector candidates. Graph context stays a
separate tool so a reviewer can see when a result came from a relationship
rather than textual resemblance. The sample does not demonstrate that this
ranking is optimal or that hybrid always wins.

## People and relationships require restraint

The wider design explores working hypotheses about collaboration and context.
An inferred relationship must remain distinguishable from a recorded fact.
Recording consent, tone interpretation, sensitive person notes and changing
sharing boundaries make that especially important.

This sample avoids those inferences. It recognizes only fictional contributors
and explicit Owner/Assigned-to annotations within their notes. It does not
classify emotions, infer reporting lines or score people.

## Tools and skills have different jobs

MCP exposes small operations: search, read, graph context and lineage. An agent's
skill or workflow can compose them into a question such as a status review.
The skill does not gain extra permissions merely because it can call a tool.

The demo has no write tools, shell execution or external connectors. An MCP
client can still send returned text to its configured model provider. Read-only
tools do not mean the surrounding assistant cannot disclose or misuse data.

## What a production extension would need

- Authorization before retrieval, graph expansion, embedding and any external
  reranking, with consistent boundaries across caches and derived artifacts.
- Retention, deletion and recording-permission policies for source material.
- Stable identifiers for extracted items across note edits. This demo's typed
  item IDs use ordinal position and can change when a note is reordered.
- Incremental indexing, concurrency behavior, freshness and deletion handling.
- Evaluation against real permitted queries, including no-answer cases. A vector
  nearest neighbor can still be irrelevant; this demo has no calibrated cutoff.
- Trace-level observability, review gates and separate permissions for actions
  such as updating tasks or sharing a report.

Those are requirements and design considerations, not completed capabilities
claimed by this public sample.

## Implementation references

- [NetworkX MultiDiGraph](https://networkx.org/documentation/stable/reference/classes/multidigraph.html)
- [Sentence Transformers semantic search](https://www.sbert.net/examples/sentence_transformer/applications/semantic-search/README.html)
- [MCP Python SDK, v1 branch](https://github.com/modelcontextprotocol/python-sdk/tree/v1.x)
