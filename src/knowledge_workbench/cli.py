import argparse
import json

from .corpus import load_corpus
from .graph import build_graph
from .retrieval import Search


def main():
    parser = argparse.ArgumentParser(description="Inspect the public knowledge-work template and its fictional pilot records.")
    parser.add_argument("--query", default="Why was audio deferred?")
    parser.add_argument("--semantic", action="store_true")
    parser.add_argument("--local-only", action="store_true")
    parser.add_argument("--lineage", default="pilot-brief")
    parser.add_argument("--person", default="Stone, Avery")
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()
    notes = load_corpus()
    graph = build_graph(notes)
    if args.validate:
        print(json.dumps({"valid": True, "records": len(notes),
                          "layers": sorted({n.tier for n in notes.values()}),
                          "source_cycles": False}, indent=2))
        return
    result = {
        "search": Search(notes, args.semantic, args.local_only).search(args.query),
        "lineage": graph.lineage(args.lineage),
        "person_context": graph.context("person:" + args.person),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
