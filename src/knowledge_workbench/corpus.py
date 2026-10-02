"""Load the bundled fictional corpus. No remote sources or arbitrary MCP file reads."""
from dataclasses import dataclass
from pathlib import Path
import re

import yaml

DATA = Path(__file__).parent / "data"
ID = re.compile(r"^[a-z][a-z0-9-]{0,79}$")
TIERS = {"raw", "curated", "atomic", "work-product"}
FIELDS = {"id", "title", "tier", "date", "origin", "related", "contributors"}


@dataclass(frozen=True)
class Note:
    id: str
    title: str
    tier: str
    date: str
    origin: tuple[str, ...]
    related: tuple[str, ...]
    contributors: tuple[str, ...]
    body: str
    path: str


def load_corpus(root: Path = DATA) -> dict[str, Note]:
    notes = {}
    total = 0
    for path in sorted(root.glob("*.md")):
        if path.is_symlink():
            raise ValueError("Corpus files must not be symlinks")
        size = path.stat().st_size
        total += size
        if size > 65536 or total > 1048576:
            raise ValueError("Demo corpus size limit exceeded")
        text = path.read_text(encoding="utf-8")
        parts = text.split("---", 2)
        if len(parts) != 3 or parts[0].strip():
            raise ValueError(f"Missing frontmatter in {path.name}")
        meta = yaml.safe_load(parts[1])
        if not isinstance(meta, dict) or set(meta) != FIELDS:
            raise ValueError(f"Unexpected metadata fields in {path.name}")
        for key in ("id", "title", "tier", "date"):
            if not isinstance(meta[key], str) or not meta[key]:
                raise ValueError(f"{key} must be a nonempty string")
        if not ID.fullmatch(meta["id"]) or meta["tier"] not in TIERS:
            raise ValueError("Invalid note id or tier")
        for key in ("origin", "related", "contributors"):
            values = meta[key]
            if not isinstance(values, list) or any(not isinstance(x, str) or not x for x in values):
                raise ValueError(f"{key} must be a list of nonempty strings")
            if len(set(values)) != len(values):
                raise ValueError(f"Duplicate {key}")
            meta[key] = tuple(values)
        if meta["id"] in notes:
            raise ValueError("Duplicate note id")
        notes[meta["id"]] = Note(**meta, body=parts[2].strip(), path=path.name)
    if not notes:
        raise ValueError("Empty corpus")
    for note in notes.values():
        if any(ref not in notes for ref in (*note.origin, *note.related)):
            raise ValueError(f"Unresolved source reference on {note.id}")
    return notes
