"""Adapted graph primitives; explicit provenance is separate from relatedness."""
from collections import deque

import networkx as nx

from .corpus import Note
from .extraction import _enrich_note_with_structured_items


class PKMGraph:
    def __init__(self):
        self.G = nx.MultiDiGraph()

    def add_node(self, node_id: str, node_type: str, label: str, **metadata):
        self.G.add_node(node_id, node_type=node_type, label=label, **metadata)

    def add_edge(self, source: str, target: str, edge_type: str,
                 source_path: str = "", context: str = "", **kwargs):
        if source not in self.G or target not in self.G:
            raise ValueError("Edges require existing endpoints")
        self.G.add_edge(source, target, key=(edge_type, source_path),
                        edge_type=edge_type, source_path=source_path,
                        context=context, **kwargs)

    def has_node(self, node_id: str) -> bool:
        return node_id in self.G

    def get_node(self, node_id: str) -> dict:
        if node_id not in self.G:
            raise ValueError("Unknown node id")
        return {"id": node_id, **self.G.nodes[node_id]}

    def context(self, start_id: str, hops: int = 1) -> dict:
        """Explore both directions, returning each node once and every visible edge."""
        self.get_node(start_id)
        if not 0 <= hops <= 3:
            raise ValueError("hops must be between 0 and 3")
        seen = {start_id}
        queue = deque([(start_id, 0)])
        depth = {start_id: 0}
        while queue:
            current, distance = queue.popleft()
            if distance == hops:
                continue
            neighbors = set(self.G.successors(current)) | set(self.G.predecessors(current))
            for neighbor in sorted(neighbors):
                if neighbor not in seen:
                    if len(seen) >= 100:
                        raise ValueError("Context exceeds demo node limit; use fewer hops")
                    seen.add(neighbor)
                    depth[neighbor] = distance + 1
                    queue.append((neighbor, distance + 1))
        return {
            "nodes": [{**self.get_node(n), "distance": depth[n]} for n in sorted(seen)],
            "edges": self._edges(self.G.subgraph(seen)),
        }

    @staticmethod
    def _edges(graph) -> list[dict]:
        edges = [{"source": a, "target": b, **data} for a, b, data in graph.edges(data=True)]
        return sorted(edges, key=lambda e: (e["source"], e["target"], e["edge_type"], e["source_path"]))

    def lineage(self, note_id: str) -> dict:
        """Follow child -> origin only. A related note is not automatically a source."""
        self.get_node(note_id)
        origins = nx.DiGraph()
        origins.add_nodes_from(self.G.nodes)
        origins.add_edges_from((a, b) for a, b, d in self.G.edges(data=True) if d["edge_type"] == "origin")
        if not nx.is_directed_acyclic_graph(origins):
            raise ValueError("Source lineage contains a cycle")
        ids = {note_id} | nx.descendants(origins, note_id)
        edges = [e for e in self._edges(self.G.subgraph(ids)) if e["edge_type"] == "origin"]
        return {"nodes": [self.get_node(n) for n in sorted(ids)], "edges": edges}


def build_graph(notes: dict[str, Note]) -> PKMGraph:
    graph = PKMGraph()
    people = {p for note in notes.values() for p in note.contributors}
    for person in sorted(people):
        graph.add_node("person:" + person, "person", person)
    for note in notes.values():
        graph.add_node(note.id, "note", note.title, tier=note.tier, path=note.path, date=note.date)
    for note in notes.values():
        for relation, targets in (("origin", note.origin), ("related", note.related)):
            for target in targets:
                graph.add_edge(note.id, target, relation, source_path=note.id)
        for person in note.contributors:
            graph.add_edge("person:" + person, note.id, "contributed_to", source_path=note.id)
        # Raw records are evidence, not an extra set of interpreted decisions.
        if note.tier == "curated":
            _enrich_note_with_structured_items(
                graph, note.id, note.title, note.date, note.body,
                lambda value: "person:" + value if value in note.contributors else None,
            )
    for note_id in notes:
        graph.lineage(note_id)  # Fail closed on cyclic provenance.
    return graph
