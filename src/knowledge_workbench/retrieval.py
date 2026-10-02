"""Inspectable lexical + optional local semantic retrieval with rank fusion."""
from collections import Counter
from math import log
import re

from .corpus import Note

MODEL = "sentence-transformers/all-MiniLM-L6-v2"
REVISION = "c9745ed1d9f207416be6d2e6f8de32d1f16199bf"


def tokens(text: str) -> list[str]:
    return re.findall(r"[\w]+(?:-[\w]+)*", text.casefold())


def reciprocal_rank_fusion(rankings: dict[str, list[str]], k: int = 60) -> list[dict]:
    """Adapted from the template merger: 1-based ranks, no implicit tier/time boost."""
    if k < 1:
        raise ValueError("k must be positive")
    scores, ranks = {}, {}
    for channel, ids in rankings.items():
        for rank, note_id in enumerate(dict.fromkeys(ids), start=1):
            scores[note_id] = scores.get(note_id, 0) + 1 / (k + rank)
            ranks.setdefault(note_id, {})[channel] = rank
    return [{"id": n, "score": scores[n], "ranks": ranks[n]}
            for n in sorted(scores, key=lambda n: (-scores[n], n))]


class Search:
    def __init__(self, notes: dict[str, Note], semantic: bool = False, local_only: bool = False):
        self.notes = notes
        self.ids = sorted(notes)
        texts = [notes[n].title + "\n" + notes[n].body for n in self.ids]
        self.counts = {n: Counter(tokens(text)) for n, text in zip(self.ids, texts)}
        self.model = None
        if semantic:
            from sentence_transformers import SentenceTransformer
            # Only model weights may download. Embedding inference runs locally.
            self.model = SentenceTransformer(MODEL, revision=REVISION, device="cpu", local_files_only=local_only)
            self.vectors = self.model.encode(texts, normalize_embeddings=True)

    def keyword(self, query: str) -> list[str]:
        scores = {}
        for note_id, counts in self.counts.items():
            score = 0.0
            for term in set(tokens(query)):
                if term not in counts:
                    continue
                df = sum(term in counter for counter in self.counts.values())
                score += (1 + log(counts[term])) * log(1 + len(self.ids) / df)
            if score:
                scores[note_id] = score
        return sorted(scores, key=lambda n: (-scores[n], n))

    def search(self, query: str, limit: int = 5) -> dict:
        if not query.strip() or len(query) > 1024 or not 1 <= limit <= 20:
            raise ValueError("Use a query of 1-1024 characters and a limit of 1-20")
        rankings = {"keyword": self.keyword(query)[:20]}
        if self.model is not None:
            vector = self.model.encode([query], normalize_embeddings=True)[0]
            similarity = self.vectors @ vector
            rankings["semantic"] = [self.ids[i] for i in sorted(range(len(self.ids)), key=lambda i: (-float(similarity[i]), self.ids[i]))[:20]]
        results = reciprocal_rank_fusion(rankings)[:limit]
        for result in results:
            note = self.notes[result["id"]]
            result.update(title=note.title, tier=note.tier, source=note.path, snippet=note.body[:360])
        return {
            "mode": "hybrid" if self.model is not None else "keyword",
            "model": MODEL if self.model is not None else None,
            "results": results,
        }
