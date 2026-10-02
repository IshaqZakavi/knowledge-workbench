# An agentic operating system for knowledge work

A reusable template for turning source material into reviewed knowledge,
connected work and grounded outputs. The aim is to retain enough context to
answer: **What did we decide, why, what changed, and what needs attention next?**

This is a public selection from my personal knowledge-management project. Its
core is the folder structure, record contracts and working methods below.
Search and the relationship graph help an assistant use that structure.

## Start with the system

- [The mental model](docs/mental-model.md): why the layers exist and what each keeps.
- [Folder structure](docs/folder-structure.md): the original template and its later five-stage vault form.
- [A complete worked flow](docs/walkthrough.md): source, curation, work, review and output.
- [Learning and inquiry](docs/learning-and-inquiry.md): a recovered design for turning capture into understanding.
- [Architecture and capability map](docs/capability-map.md): what runs here, what is a workflow, and what belongs to the larger implementation.

## The structure is part of the design

```text
notes/
  raw/
    .originals/          Permitted original artifacts, kept separate from extracted text
  curated/               Comprehensive structured records, mirrored to their raw source
  atomic/                Selective reusable ideas; most curated notes produce none
reference/
  people/                Authored identity, aliases, context and provisional hypotheses
  processes/             Expected stages, roles, gates, tools and exceptions
  process-runs/          What happened in a particular execution
  terms/                 Shared vocabulary and ontology
  entities/              Other durable identities
  architecture-patterns/ Reusable design decisions, forces and consequences
goals/                   Outcomes and acceptance criteria
backlog-items/           Durable work threads under goals
work-items/              Accepted active work, with ownership and evidence
work-products/           Briefs, reports and other audience-specific outputs
context/manifests/       Sources selected for a particular question
published/               Reviewed outward-sharing manifests, exports and consumers
ops/                     Proposed changes and pending external actions
.claude/skills/          Selected agent working methods
schema/                  Frontmatter contract selected from the original template
src/knowledge_workbench/ Read-only example mechanics, not the full private runtime
```

The main route is `raw -> curated -> work-products`. Atomic notes are a
**selective branch**, not a mandatory summarization step. References and work
records are maintained alongside those layers.

The later implementation arranges each domain into `1-original`, `2-raw`,
`3-curated`, `4-atomic` and `5-work-products`, with a shared protocol and separate
vaults. [The mapping](docs/folder-structure.md) explains both manifestations of
the same project without pretending they use an identical schema or backend.

## What becomes possible

- Prepare for a discussion with recent decisions, unresolved work and relevant
  person context, while keeping observations separate from hypotheses.
- Produce a status brief for the question being asked now, drawing on goals,
  tasks, process runs and source evidence instead of maintaining a disconnected
  report by hand.
- Trace a recommendation through reviewed interpretation to the source, then
  revisit it when its assumptions change.
- Compare an expected process with observed runs before proposing an improvement.
- Reuse the methodology across projects while keeping their content and sharing
  boundaries distinct.

These are supported workflow purposes. This release makes no quantified
productivity claim and does not include every private runtime capability.

## Follow the fictional pilot

Read the
[kickoff source](notes/raw/transcript-2026-01-12-knowledge-pilot.md), its
[curated record](notes/curated/transcript-2026-01-12-knowledge-pilot-CURATED.md),
the [goal](goals/reviewable-pilot.md), the
[observed process run](reference/process-runs/pilot-review.md) and the
[decision brief](work-products/knowledge-pilot/decision-brief.md).

Two sources have two mirrored curated records. One idea earns an atomic note;
the coordination update does not. The brief stays in draft because source review
and approval ownership are unresolved. Every person and event is invented.

## Inspect it locally

This is a repository template. Use an **editable installation** so the runtime
reads the visible layer folders rather than a second hidden copy of the notes.
Python 3.11 or newer is required.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
knowledge-demo --validate
knowledge-demo --query 'Why was audio deferred?'
python -m pytest -q
```

Optional local semantic retrieval:

```bash
python -m pip install -e '.[semantic]'
knowledge-demo --semantic --query 'What prevents approval of the pilot brief?'
```

The first semantic run downloads a pinned Sentence Transformers model. Embedding
inference then runs locally on CPU. After caching it, add `--local-only` to
prevent model downloads. The default path needs no model or API key and reports
`mode: keyword`; the semantic path reports `mode: hybrid`.

A read-only stdio MCP server is available as `knowledge-mcp`. See
[MCP and skills](docs/mcp-and-skills.md) for setup and workflows. The public
adapter supports search, record reading/listing, graph context and source
lineage. It does not autonomously curate notes, execute tasks or publish outputs.

## How much of the larger system is here?

The public template includes selected record contracts, working methods,
fictional examples and a small verified Python adapter. The larger project also
has persistent retrieval stores, richer people/process tools, work execution,
knowledge-intelligence pipelines and operational traces. The
[capability map](docs/capability-map.md) distinguishes those from this release.

[Provenance](docs/provenance.md) explains the selection and adaptation.
[Verification](docs/verification.md) explains what has been exercised.
[Sharing boundaries](docs/sharing-and-trust.md) explains why a private knowledge
system and its public outputs need different surfaces.

No real client records, recordings, relationship profiles or private Git history
are included. Source is publicly viewable, with copyright retained under
[COPYRIGHT](COPYRIGHT); this release does not grant an open-source license.
