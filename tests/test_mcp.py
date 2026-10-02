import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def test_stdio_search_read_graph_and_lineage():
    async def run():
        params = StdioServerParameters(command=sys.executable, args=["-m", "knowledge_workbench.server"])
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as client:
                await client.initialize()
                tools = (await client.list_tools()).tools
                assert {t.name for t in tools} == {"search_notes", "read_note", "graph_context", "source_lineage"}
                assert all(t.annotations.readOnlyHint and not t.annotations.destructiveHint for t in tools)
                for name, args in (
                    ("search_notes", {"query": "LS-014"}),
                    ("read_note", {"note_id": "session-record"}),
                    ("graph_context", {"node_id": "person:Avery", "hops": 2}),
                    ("source_lineage", {"note_id": "release-brief"}),
                ):
                    response = await client.call_tool(name, args)
                    assert not response.isError
                    assert response.structuredContent
                for value in ("../../README.md", "/etc/passwd", "https://example.com"):
                    response = await client.call_tool("read_note", {"note_id": value})
                    assert response.isError
                    assert "Unknown note id" in str(response.content)
    asyncio.run(run())
