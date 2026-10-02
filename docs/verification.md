# Checks and observed limits

Checked locally on October 2, 2026 with Python 3.12.14. The fifteen fictional
records load from the visible repository folders, not a package-internal corpus.

## Automated checks

Seventeen tests pass, including a real stdio MCP client/server exchange:

- Mirrored curation, required schema fields and curated origins for atomic notes.
- Two sources and curated records, with one selective atomic branch.
- Directed source lineage through origin and supporting evidence, excluding related goals and backlog context.
- Multiple graph predicates, explicit ownership and open/completed action states.
- Goal, active work and process-run links without merging their meanings.
- Original-artifact exclusion, symlink rejection and unresolved-reference rejection.
- Keyword results, one-based rank-fusion contributions, source-cycle and query/traversal bounds.
- All five read-only MCP tools, including filtered work listing and rejection of arbitrary paths/URLs by the note reader.

Run `python -m pytest -q` after the editable installation. The tests need no
model or network access once dependencies are installed. They verify selected
mechanics, not factual accuracy, complete access control or a full agent runtime.

## Actual local semantic run

The semantic adapter ran with cached `all-MiniLM-L6-v2` weights at the revision
pinned in `retrieval.py`, with model downloads disabled:

```bash
knowledge-demo --semantic --local-only --query 'What prevents approval of the pilot brief?'
```

| Result | Keyword rank | Semantic rank | Fused rank |
| --- | --- | --- | --- |
| pilot-brief | 1 | 3 | 1 |
| backlog-brief | 3 | 2 | 2 |
| goal-reviewable-pilot | 7 | 1 | 3 |
| pilot-review | 4 | 4 | 4 |
| pilot-kickoff | 2 | 7 | 5 |

The draft brief appears first. The latest curated update does not appear in the
top five. That is an important limit: a plausible ranking is not a complete
answer about current state. Following the brief's declared supporting sources
reaches that update and the partial process run. A reporting workflow must read
those sources and check dates before answering.

This small adapter does not apply the larger system's tier or recency policies.
The lexical index counts common words and the semantic model has no calibrated
relevance threshold here. One query is an observed run, not a benchmark. No
recall improvement, productivity gain or production-scale performance is claimed.

## Scope of the release review

The selected public tree was checked for broken local links, accidental private
paths, common credential patterns, client terms and non-allowlisted files. The
records are newly authored fiction. Pattern checks supplement manual review;
they cannot establish ownership or guarantee that every sensitive string would
be detected in a different corpus.
