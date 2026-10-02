# Checks and observed limits

Checked locally on October 2, 2026 with Python 3.12.14, NetworkX 3.7, PyYAML 6.0.3,
MCP Python SDK 1.30.0, pytest 9.1.1 and Sentence Transformers 5.7.0.
The MCP SDK is intentionally constrained to the supported v1 interface used by
the source template; this sample has not been migrated to v2.

## Automated checks

The test suite covers eleven cases, including a real stdio MCP client/server
exchange rather than mocked tool calls:

- Directed source lineage, including two paths to the same upstream note.
- Multiple predicates between the same graph nodes and deduplicated traversal.
- Explicit ownership and checked/open action state without inferring an owner.
- Exact identifier retrieval and channel-by-channel rank-fusion contributions.
- Cyclic source rejection, traversal bounds and invalid query rejection.
- Symlink and unresolved-source rejection during corpus loading.
- All four MCP tools and rejection of path/URL inputs to the note reader.

Run `python -m pytest -q` to repeat them. These tests do not require a model or
network access after dependencies are installed.

## Actual local embedding run

The semantic adapter was also run with cached `all-MiniLM-L6-v2` weights at the
revision pinned in `retrieval.py`, with model downloads disabled.

Query: **Why retain the ability to adjust individual musical parts?**

| Result | Keyword rank | Semantic rank | Fused rank |
| --- | --- | --- | --- |
| editability-principle | 1 | 1 | 1 |
| session-decisions | 2 | 3 | 2 |
| room-observation | 5 | 2 | 3 |
| session-record | 3 | 4 | 4 |
| export-checklist | 4 | 6 | 5 |

The first two results are useful for the question. The room observation is not
good evidence for the decision, despite ranking third. Similar language can
still produce an unhelpful match. The lexical index also counts common words.

This observation is a reason to inspect sources and evaluate with a larger
permitted query set, not a reason to claim perfect hybrid retrieval. There is no
calibrated relevance threshold, measured recall improvement or production-scale
performance claim in this example. The graph's explicit source links help a
reader check provenance; they cannot make an irrelevant search result correct.
