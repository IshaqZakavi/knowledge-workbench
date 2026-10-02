# From a source to a decision brief

The question in this fictional pilot is: **Can we approve the initial knowledge-work pilot?**
The example illustrates the records and decisions behind an answer. It is not a transcript of an actual project or an automated run.

## 1. Preserve the evidence

[The kickoff source](../notes/raw/transcript-2026-01-12-knowledge-pilot.md) records an initial scope, an audio restriction and two people's qualified commitments. It is raw evidence. If it came from a permitted recording, the original artifact would be kept separately from the normalized text.

## 2. Curate without flattening

[The mirrored curated record](../notes/curated/transcript-2026-01-12-knowledge-pilot-CURATED.md) retains context, decisions, actions, risks and open questions. Audio is deferred because permission and speaker review are unresolved. Rowan's commitment applies to this pilot. The approval owner is still unknown.

The [curation skill](../.claude/skills/curate/SKILL.md) explains the method. The schema and loader check the mirror and source link. They cannot determine whether the interpretation is accurate.

## 3. Keep the useful relationships

[Rowan's person record](../reference/people/park-rowan.md) distinguishes an observed request from a provisional hypothesis. The [process definition](../reference/processes/evidence-to-brief.md) describes expected stages. The [process run](../reference/process-runs/pilot-review.md) records a partial execution. A term and architecture pattern add reusable vocabulary and reasoning.

These are different kinds of context. A person appearing in a note is not automatically responsible for every action in it. The graph uses explicit assignments and typed links.

## 4. Connect knowledge to work

The [goal](../goals/reviewable-pilot.md) describes the desired outcome. The [backlog item](../backlog-items/prepare-decision-brief.md) holds the durable work thread. The [active work item](../work-items/check-source-coverage.md) names the accepted next step, which remains in progress.

The curated note does not automatically create tasks. The fictional work record represents a separate acceptance step, as described by [review and routing](../.claude/skills/review-and-route/SKILL.md).

## 5. Extract an idea only when it earns its place

[One atomic note](../notes/atomic/keep-decision-context-with-work--b9d40a1.md) expresses a reusable idea about retaining decision context. The later coordination update produces no atom. Neither source must pass through atomization before it can inform an output.

## 6. Answer with the latest state

[The later source](../notes/raw/email-2026-01-14-review-check.md) and [curated update](../notes/curated/email-2026-01-14-review-check-CURATED.md) report that the terminology list is complete but source comparison is unfinished. The approval owner remains unknown.

[The decision brief](../work-products/knowledge-pilot/decision-brief.md) uses that current state. It stays draft and recommends finishing the source review before approval. Its `supporting` links follow evidence; its `related` links connect broader work context.

That is the purpose of just-in-time reporting: answer the current question from connected records, rather than treating an old status slide as the source of truth. This brief is authored, not model-generated during the demo.

## Try the read-only mechanics

```bash
knowledge-demo --validate
knowledge-demo --query 'Why was audio deferred?'
knowledge-demo --query 'source comparison' --lineage pilot-brief --person 'Park, Rowan'
```

The output includes search ranks, source lineage and person context. The source chain includes both raw records, both curated records, the selected atomic note and the partial process run. It excludes the goal and backlog item from evidentiary lineage even though graph context can reach them.

Through MCP, use `list_records(record_type="work-item", status="in-progress")`, `read_note(note_id="pilot-brief")` and `source_lineage(note_id="pilot-brief")`. The server does not write a report, finish the task or publish anything.

## 7. Treat sharing as another boundary

The existence of a polished brief does not imply permission to share its sources. `published/manifests/`, `published/exports/` and `published/consumers/` document the intended boundary. There is no approved export in this example and no claim that a folder name enforces access control.
