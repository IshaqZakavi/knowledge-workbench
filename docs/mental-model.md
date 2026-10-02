# The mental model

The project started with a practical problem: useful context is spread across
meetings, notes, documents, conversations and work already in progress. Finding
a paragraph helps, but a useful assistant also needs to know what it means,
what changed, what remains unresolved and what can be shared.

The structure gives those questions different places to live.

## Preserve the source; make the interpretation inspectable

Original artifacts and raw text have different jobs. A recording or PDF is the
original. A transcript or text extraction is a fallible representation of it.
A curated note is a further interpretation. Collapsing those into one file makes
it difficult to tell which transformation introduced an error.

The source remains available for checking when permission and retention rules
allow it. The curated record organizes meaningful detail into context, key
points, decisions, action items, risks and open questions. It should preserve a
qualification such as "for this pilot only" even if a shorter summary sounds
cleaner without it.

In the Python template, raw and curated files mirror one another. The later
vault protocol supports type-specific curation: a meeting record, research brief
and interview should not all be forced through one generic summary format.
Reading a source is not, by itself, curation.

## Atomic notes are selective

An atomic note should carry a reusable idea beyond the meeting that introduced
it. Routine status, one-off requests and configuration details usually stay in
curated records. Search first: an existing idea may need another source or a
correction rather than a near-duplicate note.

Curated material can feed a work product directly. In the example, the later
review-progress email has a curated record and no atom. Its value is timely
coordination, not a new enduring principle.

## Relationships make context addressable

People, decisions, actions, processes, terms and goals have identities and typed
relationships. A graph can distinguish who contributed to a record, who owns a
work item, which process a run followed and which source supports an output.
Those are different predicates, even if the endpoints are the same.

Person records add aliases and working context. Observations, working hypotheses
and unresolved questions remain visibly different. One request for an example
is evidence of that request. It is not a personality diagnosis or proof of how
someone will behave in another situation. Tone and transcription errors make
that restraint particularly important.

## A process definition is not an execution

A process describes expected stages, roles, tools, gates and exception paths.
A process run records what happened in a particular instance and points to its
evidence. Without that split, an incomplete run can quietly rewrite the supposed
standard, or a documented process can be mistaken for something people actually
followed.

Terms and architecture patterns provide shared vocabulary and reusable design
context. They are authored reference records; the graph is their derived view.

## Knowledge and work belong together, without becoming the same thing

A goal explains the outcome. A backlog item represents a durable work thread.
A proposed item has not been accepted. A task is accepted work with a scope and
owner. A run is one attempt to execute it. An output is the artifact produced.
Evidence may support all of these without becoming another task.

Connecting them allows a just-in-time report to ask why work matters, what is
blocked and what has actually changed. It also makes it possible to reconsider
work when the source premise changes. This is the direction of the system, not
a claim that a graph automatically makes better decisions.

## Separate kinds of state

| State | Authority |
| --- | --- |
| Sources, curated records and authored references | Files and their declared lineage |
| Accepted work, runs, checkpoints and approvals | The configured operational runtime or tracker |
| Full-text, vectors, graph views and insight indexes | Derived projections, rebuilt from their appropriate sources |
| Outward-facing context | Explicitly selected, reviewed output bundles |

Operational state is not universally disposable. A search index can be rebuilt;
a record of an approval or unfinished run needs its own durable handling. Earlier
design notes used broader "everything is rebuildable" language, but the control
runtime requires this distinction.

## The operating pattern

1. Capture only permitted material and preserve its origin.
2. Curate it without inventing missing facts.
3. Review changes to people, processes, vocabulary and possible work.
4. Accept, reject or defer proposed work, then track its execution separately.
5. Compose an output for a question and audience, with evidence attached.
6. Review support and sharing permission before anything leaves the workspace.

Search, MCP and skills serve this pattern. They are not the definition of the
whole system.

## Five connected loops

The operator design connects memory, review/routing, execution, artifacts and
publishing. Capture and curation build memory. Review decides whether a source
changes knowledge or suggests work. Execution tracks accepted work and evidence.
Artifact composition turns selected context into something a person can inspect.
Publishing decides what can leave the private workspace.

The artifact design uses a source bundle and a reviewable intermediate package
before rendering a brief, deck, diagram or other output. The operator UI reads
backend contracts and state; it should not become a second source of workflow
truth. These are broader design elements, not additional services shipped here.
