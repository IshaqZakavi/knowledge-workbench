import argparse
import json

from .corpus import load_corpus
from .graph import build_graph
from .retrieval import Search


def main():
    parser = argparse.ArgumentParser(description="Search a fictional music-session notebook and inspect its source graph.")
    parser.add_argument("--query", default="Why keep separate stems?")
    parser.add_argument("--semantic", action="store_true")
    parser.add_argument("--local-only", action="store_true")
    parser.add_argument("--lineage", default="release-brief")
    parser.add_argument("--person", default="Avery")
    args = parser.parse_args()
    notes = load_corpus()
    graph = build_graph(notes)
    result = {
        "search": Search(notes, args.semantic, args.local_only).search(args.query),
        "lineage": graph.lineage(args.lineage),
        "person_context": graph.context("person:" + args.person),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
