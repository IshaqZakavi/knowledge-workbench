# From knowledge to work and just-in-time reporting

The important shift is that a note can influence work without becoming a task
immediately. Reviewing a source may suggest a new task, clarify an existing goal,
update a process, change a working hypothesis or require no action at all.

## Different objects answer different questions

| Object | Question |
| --- | --- |
| Goal | What outcome matters and how would we recognize it? |
| Backlog item | What durable work thread moves us toward that outcome? |
| Candidate | What might be worth doing, pending review? |
| Task/work item | What work has actually been accepted, by whom? |
| Run | What happened during one execution attempt? Where can it resume? |
| Output | What artifact exists, and has anyone reviewed it? |
| Evidence | What supports the claim, decision, work state or outcome? |

The later runtime has tracker adapters, runs, checkpoints, candidates, approvals,
threads and traces. A personal vault also has explicit goal records. Those are
related parts of one project, but the existence of each component does not prove
that every workflow is automatically integrated.

## A useful status question

"Can the pilot decision brief be shared, and what blocks the goal?"

A response assembled from the example should use:

- The goal's acceptance criteria.
- The latest curated update, which says source comparison is unfinished.
- The active work item and its evidence.
- The process definition's review gate and the partial process run.
- The brief's draft status and unresolved approval owner.

It should conclude that the example is still in review. It should not mark the
goal achieved because a document exists, or infer approval from a task checkbox.

This is what just-in-time reporting means here: compose for the current question
from connected records, with dates and evidence visible. The assistant still
needs to check freshness, missing sources and contradictory updates.

## Execution and verification

The broader design keeps resumable work state, evidence links, answer traces,
structured memory, guardrail events and evaluation records. These help explain
what an agent attempted, what it actually changed and what needs verification.
Hooks, tool permissions and review gates should depend on the consequences of
the action. A read-only source lookup and a production deployment should not
inherit the same authority merely because one agent performs both.

The public template demonstrates the records and read surfaces. It does not
ship a task runner, an external tracker integration or a deployment tool.
