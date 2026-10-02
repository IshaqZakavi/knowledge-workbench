from pathlib import Path
import shutil

import pytest

from knowledge_workbench.corpus import DATA, load_corpus
from knowledge_workbench.graph import PKMGraph, build_graph
from knowledge_workbench.retrieval import Search, reciprocal_rank_fusion


def test_lineage_follows_evidence_but_not_goal_or_backlog_context():
    graph = build_graph(load_corpus())
    upstream = graph.lineage("pilot-brief")
    assert {n["id"] for n in upstream["nodes"]} == {
        "pilot-brief", "pilot-review", "review-check", "pilot-kickoff",
        "review-check-source", "decision-context", "run-pilot-review"
    }
    assert len(upstream["edges"]) == 9
    assert {n["id"] for n in graph.lineage("pilot-kickoff")["nodes"]} == {"pilot-kickoff"}
    assert all(e["source_path"].endswith(".md") for e in upstream["edges"])
    context = {n["id"] for n in graph.context("pilot-brief", 1)["nodes"]}
    assert {"goal-reviewable-pilot", "backlog-brief"} <= context


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
    assert sorted(a["completed"] for a in actions) == [False, False, False, True, True]
    avery_actions = [b for a, b, e in graph.G.edges(data=True)
                     if a == "person:Stone, Avery" and e["edge_type"] == "owns_action_item"]
    assert len(avery_actions) == 2
    assert all("Owner: Stone, Avery" in graph.get_node(n)["label"] for n in avery_actions)
    assert not any(e["edge_type"] == "owns_risk" for _, _, e in graph.G.edges(data=True))


def test_unregistered_owner_is_not_invented():
    from knowledge_workbench.extraction import _enrich_note_with_structured_items
    graph = PKMGraph()
    graph.add_node("note", "note", "test")
    _enrich_note_with_structured_items(graph, "note", "test", "2026-01-01",
                                     "## Tasks\n- Export. (Owner: Unknown)", lambda name: None)
    assert not any(n["node_type"] == "person" for _, n in graph.G.nodes(data=True))


def test_keyword_matches_a_source_detail_and_reports_mode():
    result = Search(load_corpus()).search("speaker")
    assert result["mode"] == "keyword"
    assert {"pilot-kickoff", "pilot-review", "pilot-brief"} <= {r["id"] for r in result["results"]}
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
            graph.context("pilot-brief", hops)


def copy_template(tmp_path):
    for area in ("schema", "notes", "reference", "goals", "backlog-items", "work-items", "work-products"):
        shutil.copytree(DATA / area, tmp_path / area)
    return tmp_path


def test_visible_folders_and_selective_atomic_branch():
    notes = load_corpus()
    assert len(notes) == 15
    assert sum(n.tier == "raw" for n in notes.values()) == 2
    assert sum(n.tier == "curated" for n in notes.values()) == 2
    assert sum(n.tier == "atomic" for n in notes.values()) == 1
    assert notes["decision-context"].origin == ("pilot-review",)
    assert notes["pilot-brief"].origin == ("pilot-review",)
    assert notes["review-check"].metadata["status"] == "curated"


def test_goal_process_and_person_relationships_are_typed():
    graph = build_graph(load_corpus())
    edges = {(a, b, e["edge_type"]) for a, b, e in graph.G.edges(data=True)}
    assert ("run-pilot-review", "proc-evidence-to-brief", "process_id") in edges
    assert ("task-source-coverage", "goal-reviewable-pilot", "goal") in edges
    assert ("person:Park, Rowan", "task-source-coverage", "owns_record") in edges
    assert graph.get_node("pilot-brief")["status"] == "draft"
    assert graph.get_node("task-source-coverage")["status"] == "in-progress"


def test_corpus_rejects_symlink(tmp_path):
    copy_template(tmp_path)
    (tmp_path / "notes/raw/linked.md").symlink_to(DATA / "README.md")
    with pytest.raises(ValueError, match="symlinks"):
        load_corpus(tmp_path)


def test_corpus_rejects_unresolved_sources(tmp_path):
    copy_template(tmp_path)
    (tmp_path / "notes/raw/transcript-2026-01-12-knowledge-pilot.md").unlink()
    with pytest.raises(ValueError, match="Unresolved"):
        load_corpus(tmp_path)


def test_curation_must_mirror_its_source(tmp_path):
    copy_template(tmp_path)
    p = tmp_path / "notes/curated/email-2026-01-14-review-check-CURATED.md"
    p.rename(p.with_name("unmirrored-CURATED.md"))
    with pytest.raises(ValueError, match="mirror"):
        load_corpus(tmp_path)


def test_schema_rejects_missing_status(tmp_path):
    copy_template(tmp_path)
    p = tmp_path / "notes/raw/email-2026-01-14-review-check.md"
    p.write_text(p.read_text().replace("status: raw\n", ""))
    with pytest.raises(ValueError, match="frontmatter"):
        load_corpus(tmp_path)


def test_original_artifacts_are_not_indexed(tmp_path):
    copy_template(tmp_path)
    p = tmp_path / "notes/raw/.originals/do-not-index.md"
    p.write_text("original material without record metadata")
    assert len(load_corpus(tmp_path)) == 15


def test_atomic_origin_cannot_skip_curation(tmp_path):
    copy_template(tmp_path)
    p = tmp_path / "notes/atomic/keep-decision-context-with-work--b9d40a1.md"
    p.write_text(p.read_text().replace(
        "notes/curated/transcript-2026-01-12-knowledge-pilot-CURATED.md",
        "notes/raw/transcript-2026-01-12-knowledge-pilot.md"))
    with pytest.raises(ValueError, match="Atomic origin"):
        load_corpus(tmp_path)
