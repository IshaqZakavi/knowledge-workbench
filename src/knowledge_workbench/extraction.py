"""Selected note-extraction functions from the personal template.

See docs/provenance.md for the adaptation boundary. Section headings and
explicit owner annotations are cues, not a model-based inference of intent.
"""
import logging
import re
from collections import defaultdict

logger = logging.getLogger(__name__)

_SECOND_LEVEL_SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


_LIST_ITEM_RE = re.compile(r"^\s*(?:[-*]|\d+\.)\s+(.*\S)\s*$")


_OWNER_PATTERNS = [
    re.compile(r"\((?:Owner|Owners|Assigned to):\s*([^)]+)\)", re.IGNORECASE),
    re.compile(r"\[(?:Owner|Owners|Assigned to):\s*([^\]]+)\]", re.IGNORECASE),
    re.compile(r"(?:^|[;,.]\s*)(?:Owner|Owners|Assigned to)\s*[:\-]\s*([^.;]+)", re.IGNORECASE),
]


_PEOPLE_SPLIT_RE = re.compile(r"\s*(?:;|/|\band\b|\|)\s*", re.IGNORECASE)


_TYPED_ITEM_PREFIX_PATTERNS = [
    (
        re.compile(r"^(?:decision|decided|direction|recommendation)\s*[:\-]\s*(.+)$", re.IGNORECASE),
        "decision",
    ),
    (
        re.compile(r"^(?:risk|concern|blocker|issue|dependency)\s*[:\-]\s*(.+)$", re.IGNORECASE),
        "risk",
    ),
    (
        re.compile(r"^(?:action|action item|next step|next steps|follow-up|follow up|todo|to do|task)\s*[:\-]\s*(.+)$", re.IGNORECASE),
        "action_item",
    ),
]


def _strip_markdown_inline(text: str) -> str:
    """Lightweight markdown cleanup for structured note items."""
    cleaned = re.sub(r"^\[[ xX]\]\s*", "", text.strip())
    cleaned = re.sub(r"\*\*(.*?)\*\*", r"\1", cleaned)
    cleaned = re.sub(r"`([^`]+)`", r"\1", cleaned)
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip(" -")


def _structured_section_kind(heading: str) -> str:
    lowered = heading.strip().lower()
    if any(token in lowered for token in ("action item", "next step", "follow-up", "follow up", "todo", "to do", "task")):
        return "action_item"
    if any(token in lowered for token in ("decision", "direction", "recommendation")):
        return "decision"
    if any(token in lowered for token in ("risk", "concern", "blocker", "issue", "dependency")):
        return "risk"
    return ""


def _iter_second_level_sections(body: str) -> list[tuple[str, str]]:
    """Return (heading, section body) for each second-level markdown section."""
    matches = list(_SECOND_LEVEL_SECTION_RE.finditer(body))
    sections = []
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(body)
        sections.append((match.group(1).strip(), body[start:end].strip()))
    return sections


_CHECKBOX_RE = re.compile(r"^\[([xX ])\]\s*")


def _extract_section_items(section_body: str) -> list[tuple[str, bool | None]]:
    """Extract actionable list items from a section, falling back to paragraphs.

    Returns list of (cleaned_text, completed) tuples.
    completed is True for [x], False for [ ], None when no checkbox present.
    """
    items: list[tuple[str, bool | None]] = []
    for line in section_body.splitlines():
        match = _LIST_ITEM_RE.match(line)
        if not match:
            continue
        raw = match.group(1).strip()
        cb = _CHECKBOX_RE.match(raw)
        if cb:
            completed: bool | None = cb.group(1).lower() == "x"
        else:
            completed = None
        cleaned = _strip_markdown_inline(raw)
        if cleaned:
            items.append((cleaned, completed))
    if items:
        return items

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", section_body) if p.strip()]
    return [
        (_strip_markdown_inline(p), None)
        for p in paragraphs
        if _strip_markdown_inline(p)
    ]


def _extract_structured_people(text: str, resolve_entity) -> list[str]:
    """Extract explicit owner annotations from a list item."""
    people = []
    seen = set()
    for pattern in _OWNER_PATTERNS:
        for match in pattern.finditer(text):
            raw_blob = match.group(1).strip()
            for candidate in _PEOPLE_SPLIT_RE.split(raw_blob):
                candidate = candidate.strip()
                if not candidate:
                    continue
                canonical = resolve_entity(candidate)
                if canonical and canonical not in seen:
                    people.append(canonical)
                    seen.add(canonical)
    return people


def _typed_item_kind_and_text(text: str, default_kind: str = "") -> tuple[str, str]:
    """Infer item kind from explicit prefixes or the section's default kind."""
    cleaned = _strip_markdown_inline(text)
    if not cleaned:
        return "", ""

    for pattern, kind in _TYPED_ITEM_PREFIX_PATTERNS:
        match = pattern.match(cleaned)
        if match:
            return kind, _strip_markdown_inline(match.group(1))

    return default_kind, cleaned


def _enrich_note_with_structured_items(
    graph: "PKMGraph",
    rel_path: str,
    title: str,
    note_date: str,
    body: str,
    resolve_entity,
) -> int:
    """Extract typed note items such as decisions, risks, and action items."""
    edge_count = 0
    created_items = 0
    if not body.strip():
        return created_items

    relation_map = {
        "decision": ("captures_decision", "assigned_decision"),
        "risk": ("captures_risk", "owns_risk"),
        "action_item": ("captures_action_item", "owns_action_item"),
    }
    ordinal_by_kind = defaultdict(int)

    sections = _iter_second_level_sections(body)
    if not sections:
        sections = [("Body", body)]

    for heading, section_body in sections:
        default_kind = _structured_section_kind(heading)
        items = _extract_section_items(section_body)
        for item, completed in items:
            kind, typed_text = _typed_item_kind_and_text(item, default_kind)
            if not kind or not typed_text:
                continue
            ordinal_by_kind[kind] += 1
            node_id = f"{kind}:{rel_path}:{ordinal_by_kind[kind]}"
            note_edge_type, person_edge_type = relation_map[kind]
            extra: dict = dict(
                note_path=rel_path,
                date=note_date,
                section_heading=heading,
                source_note_title=title,
            )
            if kind == "action_item" and completed is not None:
                extra["completed"] = completed
            graph.add_node(node_id, kind, typed_text, **extra)
            graph.add_edge(
                rel_path,
                node_id,
                note_edge_type,
                source_path=rel_path,
                context=f"{title} {kind.replace('_', ' ')} from {heading}",
                created_date=note_date,
            )
            edge_count += 1
            created_items += 1

            for person in _extract_structured_people(item, resolve_entity):
                if not graph.has_node(person):
                    graph.add_node(person, "person", person)
                graph.add_edge(
                    person,
                    node_id,
                    person_edge_type,
                    source_path=rel_path,
                    context=f"{person} linked to {kind.replace('_', ' ')} in {title}",
                    created_date=note_date,
                )
                edge_count += 1

    if created_items:
        logger.info(
            "_enrich_note_with_structured_items: %s - %d typed items, %d edges",
            rel_path,
            created_items,
            edge_count,
        )
    return created_items
