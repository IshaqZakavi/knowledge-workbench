# From a session note to an answer you can check

The question is simple: **Why keep separate stems, and what still needs to happen?**
The answer crosses a decision, two people, unfinished tasks and an original
conversation. Putting all of those in one paragraph makes the distinctions easy
to lose.

This walkthrough uses invented records. Open the linked files alongside the
commands to see what the system knows and what it does not.

## 1. Preserve the record

In the [session record](../src/knowledge_workbench/data/01-session-record.md),
Avery wants to adjust the texture independently of the percussion. Rowan offers
to check the loop boundary. Release permission is still unresolved.

The raw layer holds this evidence. In a real system, retaining a record would
depend on permission, retention policy and whether it should be captured at all.
More capture is not automatically better.

## 2. Make an interpretation explicit

The [curated note](../src/knowledge_workbench/data/02-session-decisions.md)
separates decisions, action items and risks. It points back to `session-record`.

The extractor reads those section headings and explicit owner annotations. It
does not use a model to guess who agreed, who was responsible or what someone
felt. A checked box means the note records completion. It is not an independent
verification that the work happened.

| Item | Recorded owner | Recorded state |
| --- | --- | --- |
| Export separate parts | Avery | Open |
| Check the loop boundary | Rowan | Open |
| Save the current stereo mix for comparison | Avery | Complete |
| Review release permission | No explicit assignment | Unresolved risk |

The last row matters. An unassigned risk should not quietly become someone's
task just because their name appears elsewhere in the note.

## 3. Retrieve by wording or meaning

```bash
knowledge-demo --query 'LS-014'
knowledge-demo --semantic --query 'Why retain the ability to adjust individual musical parts?'
```

The first query needs an exact identifier. The second asks about an idea without
using the session's exact phrasing. Neither retrieval route is always better.
The hybrid response exposes each route's rank, then combines them with:

`score(note) = sum(1 / (60 + rank_in_channel))`

Ranks start at one. A missing channel contributes zero. The score is a ranking
device, not a probability of truth. The demo does not silently prefer newer or
more polished notes.

## 4. Follow the relationships

`graph_context("person:Avery", 1)` returns Avery's connections to notes and
explicitly assigned actions. Each edge includes a source note ID. Use two hops
to inspect the next set of relationships.

This preserves a useful distinction: contributing to a note and owning an
action are different relationships. The graph retains both when they connect
the same pair of entities. A shared connection does not imply agreement,
authority or friendship.

## 5. Trace the status back to its source

`source_lineage("release-brief")` returns these directed relationships:

```text
release-brief ---------> session-decisions ---------> session-record
      |
      +----> editability-principle ----> session-decisions
```

The [export checklist](../src/knowledge_workbench/data/05-export-checklist.md) is
related context, but is not listed as an origin. It therefore stays out of this
lineage walk. General relatedness and evidence have different jobs.

An answer supported by these records can say the team intends to preserve
editability and has two remaining tasks. It cannot say the export is finished,
the track sounds better or the work is cleared for public release.

## What this adds to knowledge work

The useful unit becomes more than a search result. A reader can inspect a claim,
its source, an associated action and the recorded owner together. That creates
a foundation for status reporting and decision support, while keeping the
interpretation open to correction.

The demo stops at retrieval and inspection. It does not create tasks elsewhere,
send a report or change a source note.
