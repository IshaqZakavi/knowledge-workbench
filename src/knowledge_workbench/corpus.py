"""Read the public template's real layer folders, using its selected schema."""
from dataclasses import dataclass
import json
from pathlib import Path

from jsonschema import Draft202012Validator
import yaml

# Editable repository installation: sources stay in their visible layer folders.
# MCP callers cannot switch this root to another vault.
DATA = Path(__file__).resolve().parents[2]
AREAS = ("notes/raw", "notes/curated", "notes/atomic", "reference", "goals",
         "backlog-items", "work-items", "work-products")


@dataclass(frozen=True)
class Note:
    id: str
    title: str
    tier: str
    date: str
    origin: tuple[str, ...]
    supporting: tuple[str, ...]
    related: tuple[str, ...]
    contributors: tuple[str, ...]
    body: str
    path: str
    metadata: dict


def load_corpus(root: Path = DATA) -> dict[str, Note]:
    """Validate authored records before creating a derived search or graph view."""
    root = root.resolve()
    schema_path = root / "schema/frontmatter.schema.json"
    if not schema_path.is_file():
        raise ValueError("Template schema missing; use an editable repository checkout")
    validator = Draft202012Validator(json.loads(schema_path.read_text()))
    records, path_to_id = {}, {}
    total = 0
    for area in AREAS:
        for path in sorted((root / area).rglob("*.md")):
            if path.name == "README.md" or ".originals" in path.parts:
                continue
            if path.is_symlink() or not path.resolve().is_relative_to(root):
                raise ValueError("Corpus files must not be symlinks or escape the template")
            total += path.stat().st_size
            if path.stat().st_size > 65536 or total > 1048576:
                raise ValueError("Public example size limit exceeded")
            parts = path.read_text(encoding="utf-8").split("---", 2)
            if len(parts) != 3 or parts[0].strip():
                raise ValueError(f"Missing frontmatter in {path.name}")
            meta = yaml.safe_load(parts[1])
            errors = list(validator.iter_errors(meta))
            if errors:
                raise ValueError(f"Invalid frontmatter in {path.name}: {errors[0].message}")
            rel = path.relative_to(root).as_posix()
            note_id = meta.get("id", rel)
            if note_id in records or not note_id:
                raise ValueError("Duplicate or empty record id")
            tier = area.removeprefix("notes/") if area.startswith("notes/") else area
            if tier == "work-products":
                tier = "work-product"
            records[note_id] = (meta, parts[2].strip(), rel, tier)
            path_to_id[rel] = note_id
    if not records:
        raise ValueError("Empty corpus")

    def resolve(ref):
        if ref in records:
            return ref
        if ref in path_to_id:
            return path_to_id[ref]
        raise ValueError("Unresolved local record reference")

    notes = {}
    for note_id, (meta, body, rel, tier) in records.items():
        refs = {}
        for field in ("origin", "supporting", "related", "goal", "goal_id", "parent_goal",
                      "parent_goal_id", "depends_on", "process_id", "used_in_processes"):
            value = meta.get(field, [])
            values = [value] if isinstance(value, str) else value
            refs[field] = tuple(resolve(v) for v in values)
        if tier == "curated":
            expected = rel.replace("notes/curated/", "notes/raw/", 1).replace("-CURATED.md", ".md")
            if meta.get("origin") != expected or expected not in path_to_id:
                raise ValueError("Curated record must mirror and cite its raw source")
        if tier == "atomic" and not refs["origin"]:
            raise ValueError("An extracted atomic note requires its curated origin")
        if tier == "atomic" and any(records[n][3] != "curated" for n in refs["origin"]):
            raise ValueError("Atomic origin must be a curated record")
        metadata = {**meta, "resolved_references": refs}
        notes[note_id] = Note(note_id, meta["title"], tier, meta.get("date", ""),
                              refs["origin"], refs["supporting"], refs["related"],
                              tuple(meta.get("contributors", [])), body, rel, metadata)
    return notes
