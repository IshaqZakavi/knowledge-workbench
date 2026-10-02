# MCP tools and the skill layer

Tools provide operations. Skills describe how to use them well. A command can
orchestrate a workflow, and a bounded agent can perform one part of it. These
roles should stay distinguishable from the records they create.

## Public read-only tools

After the editable install, configure a client to launch the absolute path to
`.venv/bin/knowledge-mcp` using stdio:

```json
{
  "mcpServers": {
    "knowledge-work-template": {
      "command": "/absolute/path/to/knowledge-workbench/.venv/bin/knowledge-mcp",
      "args": []
    }
  }
}
```

Use `--semantic --local-only` in `args` only after installing the semantic extra
and caching the model. Default mode needs no model.

| Tool | Purpose |
| --- | --- |
| `search_notes(query, limit)` | Find records, exposing retrieval channel ranks |
| `read_note(note_id)` | Read a known record with its source and state |
| `list_records(record_type, status)` | Inspect goals, work items, processes or notes |
| `graph_context(node_id, hops)` | Follow typed context relationships, up to three hops |
| `source_lineage(note_id)` | Follow origin and declared supporting evidence |

The tools read this checkout. They do not accept a private-vault path, issue
external actions or perform model-based curation.

## Selected skills included

The `.claude/skills/` directory contains portable adaptations of the original
working methods for curation, selective atomization, composition, process
ontology, review/routing and context-aware reporting. They are instructions for
an assistant with appropriate permissions, not proof that an automated pipeline
ran. Their references match the files and commands actually included here.

The broader design separates reusable mechanics from workspace-specific voice,
brand and policies. A thin wrapper supplies those inputs. It should not copy a
private workspace's content or permissions into the shared protocol.

## Example: a current status brief

Ask a connected assistant:

> Read the pilot goal and decision brief. Find the latest curated update,
> inspect the active work and process run, and tell me what is still unresolved.
> Cite record IDs and distinguish a completed artifact from approved sharing.

A good workflow gathers evidence before synthesis, keeps unknowns visible and
checks the audience before preparing an outward-facing version. Search is a
starting point; the latest relevant record and explicit source links matter.
