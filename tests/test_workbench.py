from pathlib import Path
import shutil

import pytest

from knowledge_workbench.corpus import DATA, load_corpus
from knowledge_workbench.graph import PKMGraph, build_graph
from knowledge_workbench.retrieval import Search, reciprocal_rank_fusion


def test_lineage_follows_only_upstream_sources_and_preserves_diamond():
    graph = build_graph(load_corpus())
    upstream = graph.lineage("release-brief")
    assert {n["id"] for n in upstream["nodes"]} == {
        "release-brief", "session-decisions", "editability-principle", "session-record"
    }
    assert len(upstream["edges"]) == 4
    assert {n["id"] for n in graph.lineage("session-record")["nodes"]} == {"session-record"}


def test_two_predicates_survive_and_traversal_deduplicates_nodes():
    graph = PKMGraph()
    for name in "abcd":
        graph.add_node(name, "note", name)
    for a, b in (("a", "b"), ("a", "c"), ("b", "d"), ("c", "d")):
        graph.add_edge(a, b, "related", source_path=a)
    graph.add_edge("a", "b", "origin", source_path="a")
    graph.add_edge("a", "b", "origin", source_path="a")
    result = graph.context("a", 2)
    assert len(result["nodes"]) == 4
    assert len(result["edges"]) == 5
    assert next(n for n in result["nodes"] if n["id"] == "d")["distance"] == 2


def test_action_state_and_owner_do_not_leak_to_other_items():
    graph = build_graph(load_corpus())
    actions = [n for _, n in graph.G.nodes(data=True) if n["node_type"] == "action_item"]
    assert [a["completed"] for a in actions] == [False, False, True]
    avery_actions = [b for a, b, e in graph.G.edges(data=True)
                     if a == "person:Avery" and e["edge_type"] == "owns_action_item"]
    assert len(avery_actions) == 2
    assert all("Owner: Avery" in graph.get_node(n)["label"] for n in avery_actions)
    assert not any(e["edge_type"] == "owns_risk" for _, _, e in graph.G.edges(data=True))


def test_unregistered_owner_is_not_invented():
    from knowledge_workbench.extraction import _enrich_note_with_structured_items
    graph = PKMGraph()
    graph.add_node("note", "note", "test")
    _enrich_note_with_structured_items(graph, "note", "test", "2026-01-01",
                                     "## Tasks\n- Export. (Owner: Unknown)", lambda name: None)
    assert not any(n["node_type"] == "person" for _, n in graph.G.nodes(data=True))


def test_keyword_matches_revision_and_reports_mode():
    result = Search(load_corpus()).search("LS-014")
    assert result["mode"] == "keyword"
    assert {r["id"] for r in result["results"]} == {"session-record", "session-decisions"}
    assert all(r["ranks"] == {"keyword": i + 1} for i, r in enumerate(result["results"]))


def test_rank_fusion_records_channels_and_does_not_double_count():
    result = reciprocal_rank_fusion({"keyword": ["a", "a", "b"], "semantic": ["b", "c"]})
    assert result[0]["id"] == "b"
    assert result[0]["ranks"] == {"keyword": 2, "semantic": 1}
    assert result[0]["score"] == pytest.approx(1 / 62 + 1 / 61)
    assert next(r for r in result if r["id"] == "a")["score"] == pytest.approx(1 / 61)


def test_cyclic_lineage_rejected():
    graph = PKMGraph()
    for name in "ab":
        graph.add_node(name, "note", name)
    graph.add_edge("a", "b", "origin")
    graph.add_edge("b", "a", "origin")
    with pytest.raises(ValueError, match="cycle"):
        graph.lineage("a")


def test_invalid_query_and_graph_bounds():
    for query in ("", " " * 5, "x" * 1025):
        with pytest.raises(ValueError):
            Search(load_corpus()).search(query)
    graph = build_graph(load_corpus())
    for hops in (-1, 4):
        with pytest.raises(ValueError):
            graph.context("release-brief", hops)


def test_corpus_rejects_symlink(tmp_path):
    (tmp_path / "linked.md").symlink_to(DATA / "01-session-record.md")
    with pytest.raises(ValueError, match="symlinks"):
        load_corpus(tmp_path)


def test_corpus_rejects_unresolved_sources(tmp_path):
    shutil.copyfile(DATA / "02-session-decisions.md", tmp_path / "single.md")
    with pytest.raises(ValueError, match="Unresolved"):
        load_corpus(tmp_path)
