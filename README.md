# Knowledge Workbench

**Why did we make that decision, who is doing the next step, and where is the source?**

This small Python example makes those questions inspectable. It searches notes,
connects people to explicitly recorded actions, and follows a summary back to its
source. It is adapted from my personal agentic knowledge-system template.

The six bundled notes describe a **fictional music-production session**. No client
records, personal conversations, recordings or private vault content are included.

Start with the [five-minute walkthrough](docs/walkthrough.md), or read
[the design and its limits](docs/design.md). The [provenance note](docs/provenance.md)
distinguishes existing template code from work added for this public example.
See [verification and an observed retrieval miss](docs/verification.md) for the
checks performed and what they do not establish.

## What you can inspect

| Question | Mechanism | Evidence returned |
| --- | --- | --- |
| Where is revision `LS-014` mentioned? | Keyword search | Exact matching notes and ranks |
| Why retain the ability to change individual parts? | Optional local vector search + rank fusion | Results with separate keyword and semantic ranks |
| What is Avery responsible for? | Typed relationship graph | Explicit owner annotations, action state and source note |
| What supports the listening-copy status? | Directed source-lineage traversal | Work product, interpretation and original record |

Keyword and semantic ranks combine through reciprocal rank fusion. Graph
traversal is a separate, complementary operation. A relationship is not treated
as an extra similarity score or automatic proof of a claim.

## Run it

Python 3.11 or newer:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
knowledge-demo --query 'LS-014'
python -m pytest -q
```

That path uses keyword retrieval and the graph, with **no model or API key**.
The output explicitly says `"mode": "keyword"`.

For actual hybrid retrieval:

```bash
python -m pip install -e '.[semantic]'
knowledge-demo --semantic --query 'Why retain the ability to adjust individual musical parts?'
```

The first semantic run downloads the pinned `all-MiniLM-L6-v2` model from
Hugging Face. Embeddings are computed locally on CPU. Model files are not part of
this repository. Once cached, add `--local-only` to prohibit model downloads.
There is no cloud inference service or generated-answer step in this demo.

## Use it through MCP

After installation, configure an MCP client to launch the absolute path to the
virtual environment's `knowledge-mcp` executable. This is a **stdio** server.
It does not open an HTTP endpoint.

```json
{
  "mcpServers": {
    "knowledge-workbench-demo": {
      "command": "/absolute/path/to/knowledge-workbench/.venv/bin/knowledge-mcp",
      "args": []
    }
  }
}
```

To enable hybrid search, install the semantic extra and use
`"args": ["--semantic", "--local-only"]` after caching the model.

Four read-only tools are available:

- `search_notes(query, limit)` returns ranked notes and rank provenance.
- `read_note(note_id)` reads a known bundled note ID, never an arbitrary path.
- `graph_context(node_id, hops)` explores up to three hops of explicit relationships.
- `source_lineage(note_id)` follows upstream `origin` links only.

Try asking a connected assistant:

> Find the decision about separate stems, identify the remaining actions and
> their owners, and trace the decision to its original source. Distinguish open
> tasks from completed ones. Cite note IDs and do not infer release permission.

The assistant supplies the language-model behavior. This server supplies the
records. Retrieved text remains untrusted data, even when it comes from a note.

## Boundaries

This is a public code sample, not a production knowledge platform or a music
generation product. It demonstrates a narrow part of a larger personal system.
It does not implement tenant authentication, comprehensive sharing enforcement,
recording ingestion, automatic social inference, a goal scheduler or a publish
approval workflow. Six invented notes are not a retrieval benchmark.

The full template uses a persistent search index. This small example uses an
in-memory lexical index, optional local vectors and a NetworkX graph so the
behavior is easy to inspect. See [design tradeoffs](docs/design.md).

## Repository map

```text
src/knowledge_workbench/
  data/           Six fictional notes, with explicit source references
  extraction.py   Selected and adapted structured-note extraction functions
  graph.py        Typed relationships and directional lineage
  retrieval.py    Keyword search, optional embeddings and rank fusion
  server.py       Four read-only MCP tools
  cli.py          Reproducible walkthrough output
tests/            Retrieval, lineage, action ownership and real MCP transport checks
docs/             Walkthrough, design and adaptation provenance
```

Publicly viewable source by Ishaq Zakavi. No open-source license is granted by
this release; see [COPYRIGHT](COPYRIGHT). Third-party dependencies retain their
own licenses. No model weights or third-party tutorial text are redistributed.
