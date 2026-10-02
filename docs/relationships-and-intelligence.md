# Relationships, hypotheses and knowledge intelligence

## A graph is more than related documents

The project uses relationships among notes, people, decisions, actions, risks,
process stages, terms, goals and work. Edges have types and source context. A
person contributing to a note, owning an action and reporting to someone are
three different claims.

The Python implementation derives a NetworkX graph from authored records and
extraction. The later TypeScript implementation includes a SQLite graph and
read operations for entity search, neighbors and paths. These are distinct
backends used in manifestations of the same project, not one combined database.

The public adapter preserves multiple predicates, source paths and direction.
It links authored work objects and explicit assignments; it does not infer a
relationship just because two names appear near one another.

## Social context with visible uncertainty

The larger person-context tool separates working-style signals from working
hypotheses, alongside aliases, roles, interaction history and open loops.
Speaker-aware transcription preserves uncertain speaker mapping and review cues.
Those features support thoughtful preparation, but neither a transcript nor a
model reading tone establishes someone's emotion or intention reliably.

The fictional Rowan record shows the intended discipline: a request for a
concrete example is observed; the idea that another example might help is a
provisional working hypothesis. Evidence, uncertainty and a chance to revise
belong with that hypothesis. Real person profiles and recordings are excluded
from this public template.

## Processes, vocabulary and architecture patterns

A process ontology links stages, roles, tools, triggers, gates, exceptions and
dependencies. Process runs bring evidence of actual execution. Glossary terms
normalize drifting vocabulary; architecture patterns preserve the context,
problem, forces and consequences of a reusable design choice.

This is useful for asking where a workflow repeatedly gets stuck, whether the
process description matches actual work and which proposed automation addresses
a real problem. The public adapter exposes example records and relationships;
the original process traversal and gap-reporting tools are broader.

## Agreement and disagreement across research

The later implementation also has a knowledge-intelligence pipeline:

```text
curated briefs with claims
  -> extract and enrich claims
  -> normalize themes and entities
  -> embed and cluster
  -> derived consensus / contradiction / claim views
  -> MCP tools and cited synthesis skills
```

Its design includes content-derived cluster IDs, categorical confidence,
provenance and a filter for clusters that share wording without sharing a useful
proposition. Principle candidates need review before promotion into durable notes.

These are implemented scripts and interfaces in the larger project, not shipped
executables in this public selection. Counting distinct channels is a heuristic
for corroboration, not proof of independent evidence. Claimed agreement,
contradiction and confidence remain subject to review.
