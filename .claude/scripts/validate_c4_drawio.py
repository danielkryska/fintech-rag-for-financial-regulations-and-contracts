#!/usr/bin/env python3
"""Validate a C4 draw.io XML drawing against the project drawing standard.

This is a mechanical checker. It does not replace the semantic review by
`c4-reviewer`; it catches the rules that can be checked from the XML:

- file naming and level
- one well-formed <mxfile> with one <diagram> page
- unique cell IDs; every edge has a source, a target, and a label
- Level 2/3 edges carry a [protocol] tag and an action description
- Level 2/3 have the three bands in order: Representation, Business logic, Repository
- Level 2/3 boxes in a band carry a generic [technology] tag
- business-logic boxes carry bullet points
- Level 1/2 labels do not leak vendor or cloud service names
- queue/broker/event-stream services are edge labels, not boxes
- no overlapping boxes, no edge crossings, no edge through an unrelated box
- no orphan boxes (except title, legend-*, note-*)
- a title block with a version and status

Usage:
    python .claude/scripts/validate_c4_drawio.py FILE --level {1,2,3} [--json]

Exit codes:
    0  no Blocking findings (Major/Minor may remain)
    1  at least one Blocking finding
    2  the file could not be parsed or arguments are invalid
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional
import xml.etree.ElementTree as ET

EPS = 1e-6
BAND_IDS = {
    "band-representation": ("Representation", "representation"),
    "band-business": ("Business logic", "business"),
    "band-repository": ("Repository", "repository"),
}
BAND_LABELS = {
    "representation": "Representation",
    "business": "Business logic",
    "repository": "Repository",
}
EXCLUDED_ID_PREFIXES = ("legend-", "note-", "label-")

# Vendor and platform names that must not appear at Level 1 or Level 2.
VENDOR_TERMS = [
    "aws",
    "amazon web services",
    "amazon",
    "azure",
    "microsoft azure",
    "microsoft",
    "gcp",
    "google cloud",
    "bedrock",
    "sagemaker",
    "opensearch",
    "elasticsearch",
    "aurora",
    "dynamodb",
    "s3",
    "sqs",
    "sns",
    "lambda",
    "ec2",
    "ecs",
    "eks",
    "fargate",
    "rds",
    "iam",
    "textract",
    "cognito",
    "kms",
    "cloudwatch",
    "cloudtrail",
    "azure openai",
    "azure ai search",
    "cosmos db",
    "cosmos",
    "blob storage",
    "service bus",
    "event grid",
    "azure functions",
    "entra",
    "key vault",
    "log analytics",
    "vnet",
    "vpc",
    "nsg",
    "security group",
    "nat gateway",
    "qdrant",
    "milvus",
    "weaviate",
    "pgvector",
    "postgres",
    "postgresql",
    "mysql",
    "mongodb",
    "redis",
    "kafka",
    "rabbitmq",
    "pulsar",
    "nats",
    "vllm",
    "ollama",
    "kserve",
    "ray serve",
    "cohere",
    "openai",
    "anthropic",
    "huggingface",
    "pinecone",
    "databricks",
    "kubernetes",
    "k8s",
    "docker",
    "helm",
    "kustomize",
    "keycloak",
    "opa",
    "kyverno",
]
VENDOR_PATTERNS = [
    re.compile(r"\b" + re.escape(term) + r"\b", re.IGNORECASE)
    for term in VENDOR_TERMS
]
QUEUE_PATTERN = re.compile(
    r"\b(queues?|message queues?|brokers?|event streams?|event bus(es)?|message bus(es)?|topics?)\b",
    re.IGNORECASE,
)
TAG_PATTERN = re.compile(r"\[[^\]]+\]")
STATUS_PATTERN = re.compile(r"\b(Draft|In review|Confirmed|Superseded)\b", re.IGNORECASE)
VERSION_PATTERN = re.compile(r"\bv\d+\b", re.IGNORECASE)


@dataclass
class Cell:
    id: str
    value: str = ""
    style: str = ""
    parent: Optional[str] = None
    vertex: bool = False
    edge: bool = False
    source: Optional[str] = None
    target: Optional[str] = None
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0
    points: list[tuple[float, float]] = field(default_factory=list)
    source_point: Optional[tuple[float, float]] = None
    target_point: Optional[tuple[float, float]] = None


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    cell: str = ""


def plain_text(value: str) -> str:
    """Turn a draw.io label (often HTML) into readable text."""
    if not value:
        return ""
    text = html.unescape(value)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</(div|p|li|tr|h[1-6])>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    return text.strip()


def first_line(value: str) -> str:
    for line in plain_text(value).splitlines():
        line = line.strip()
        if line:
            return line
    return ""


def parse_cells(model_root: ET.Element) -> tuple[dict[str, Cell], list[Finding]]:
    findings: list[Finding] = []
    user_labels: dict[str, str] = {}
    for wrapper in model_root.iter("UserObject"):
        for child in wrapper.findall("mxCell"):
            child_id = child.get("id")
            if child_id:
                user_labels[child_id] = wrapper.get("label") or ""
    cells: dict[str, Cell] = {}
    for el in model_root.iter("mxCell"):
        cell_id = el.get("id")
        if not cell_id:
            findings.append(Finding("Blocking", "cell-id", "mxCell without an id"))
            continue
        if cell_id in cells:
            findings.append(Finding("Blocking", "duplicate-id", f"duplicate cell id '{cell_id}'", cell_id))
            continue
        cell = Cell(
            id=cell_id,
            value=el.get("value") or user_labels.get(cell_id, ""),
            style=el.get("style") or "",
            parent=el.get("parent"),
            vertex=el.get("vertex") == "1",
            edge=el.get("edge") == "1",
            source=el.get("source"),
            target=el.get("target"),
        )
        geo = el.find("mxGeometry")
        if geo is not None:
            cell.x = float(geo.get("x") or 0.0)
            cell.y = float(geo.get("y") or 0.0)
            cell.width = float(geo.get("width") or 0.0)
            cell.height = float(geo.get("height") or 0.0)
            points_array = geo.find("Array[@as='points']")
            if points_array is not None:
                for point in points_array.findall("mxPoint"):
                    try:
                        cell.points.append((float(point.get("x") or 0.0), float(point.get("y") or 0.0)))
                    except ValueError:
                        findings.append(
                            Finding("Blocking", "bad-waypoint", f"non-numeric waypoint on '{cell_id}'", cell_id)
                        )
            source_point = geo.find("mxPoint[@as='sourcePoint']")
            target_point = geo.find("mxPoint[@as='targetPoint']")
            if source_point is not None:
                cell.source_point = (
                    float(source_point.get("x") or 0.0),
                    float(source_point.get("y") or 0.0),
                )
            if target_point is not None:
                cell.target_point = (
                    float(target_point.get("x") or 0.0),
                    float(target_point.get("y") or 0.0),
                )
        cells[cell_id] = cell
    return cells, findings


def parent_offset(cell_id: str, cells: dict[str, Cell]) -> tuple[float, float]:
    x = y = 0.0
    parent = cells[cell_id].parent
    seen: set[str] = set()
    while parent and parent in cells and parent not in seen:
        seen.add(parent)
        parent_cell = cells[parent]
        if parent_cell.vertex:
            x += parent_cell.x
            y += parent_cell.y
        parent = parent_cell.parent
    return x, y


def abs_rect(cell: Cell, cells: dict[str, Cell]) -> tuple[float, float, float, float]:
    ox, oy = parent_offset(cell.id, cells)
    return (cell.x + ox, cell.y + oy, cell.width, cell.height)


def rect_center(rect: tuple[float, float, float, float]) -> tuple[float, float]:
    x, y, w, h = rect
    return (x + w / 2.0, y + h / 2.0)


def children_map(cells: dict[str, Cell]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = defaultdict(list)
    for cell in cells.values():
        if cell.parent:
            result[cell.parent].append(cell.id)
    return result


def is_group(cell: Cell, children: dict[str, list[str]], cells: dict[str, Cell]) -> bool:
    return cell.vertex and any(cells[child].vertex for child in children.get(cell.id, []))


def is_excluded_id(cell_id: str) -> bool:
    return cell_id == "title" or cell_id.startswith(EXCLUDED_ID_PREFIXES)


def edge_label(cell: Cell, cells: dict[str, Cell]) -> str:
    labels = [plain_text(cell.value)]
    for other in cells.values():
        if other.parent == cell.id and "edgelabel" in other.style.lower():
            labels.append(plain_text(other.value))
    return " ".join(label for label in labels if label).strip()


def edge_polyline(cell: Cell, cells: dict[str, Cell]) -> Optional[list[tuple[float, float]]]:
    if not cell.source or not cell.target:
        return None
    if cell.source not in cells or cell.target not in cells:
        return None
    if not cells[cell.source].vertex or not cells[cell.target].vertex:
        return None
    start = rect_center(abs_rect(cells[cell.source], cells))
    end = rect_center(abs_rect(cells[cell.target], cells))
    ox, oy = parent_offset(cell.id, cells)
    points = [(x + ox, y + oy) for x, y in cell.points]
    polyline = [start, *points, end]
    # Remove consecutive duplicates.
    cleaned: list[tuple[float, float]] = []
    for point in polyline:
        if not cleaned or abs(point[0] - cleaned[-1][0]) > 0.5 or abs(point[1] - cleaned[-1][1]) > 0.5:
            cleaned.append(point)
    return cleaned if len(cleaned) >= 2 else None


def orient(a: tuple[float, float], b: tuple[float, float], c: tuple[float, float]) -> float:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def point_on_segment(a: tuple[float, float], b: tuple[float, float], p: tuple[float, float]) -> bool:
    return (
        abs(orient(a, b, p)) <= EPS
        and min(a[0], b[0]) - EPS <= p[0] <= max(a[0], b[0]) + EPS
        and min(a[1], b[1]) - EPS <= p[1] <= max(a[1], b[1]) + EPS
    )


def segment_intersection(
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    p4: tuple[float, float],
) -> Optional[tuple[str, tuple[float, float]]]:
    """Return ('point'|'touch', point) when the segments meet."""
    d1 = orient(p3, p4, p1)
    d2 = orient(p3, p4, p2)
    d3 = orient(p1, p2, p3)
    d4 = orient(p1, p2, p4)
    if ((d1 > EPS and d2 < -EPS) or (d1 < -EPS and d2 > EPS)) and (
        (d3 > EPS and d4 < -EPS) or (d3 < -EPS and d4 > EPS)
    ):
        denominator = d1 - d2
        if abs(denominator) > EPS:
            t = d1 / denominator
            return ("point", (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1])))
    touching: list[tuple[float, float]] = []
    for point in (p1, p2):
        if point_on_segment(p3, p4, point):
            touching.append(point)
    for point in (p3, p4):
        if point_on_segment(p1, p2, point):
            touching.append(point)
    if touching:
        return ("touch", touching[0])
    return None


def segment_intersects_rect(
    p1: tuple[float, float],
    p2: tuple[float, float],
    rect: tuple[float, float, float, float],
    shrink: float = 1.0,
) -> bool:
    x, y, w, h = rect
    x += shrink
    y += shrink
    w -= 2 * shrink
    h -= 2 * shrink
    if w <= 0 or h <= 0:
        return False
    corners = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    if x <= p1[0] <= x + w and y <= p1[1] <= y + h:
        return True
    if x <= p2[0] <= x + w and y <= p2[1] <= y + h:
        return True
    for index in range(4):
        if segment_intersection(p1, p2, corners[index], corners[(index + 1) % 4]):
            return True
    return False


def points_close(
    a: tuple[float, float], b: tuple[float, float], tolerance: float = 3.0
) -> bool:
    return abs(a[0] - b[0]) <= tolerance and abs(a[1] - b[1]) <= tolerance


def vendor_hits(text: str) -> list[str]:
    hits: list[str] = []
    seen: set[str] = set()
    for pattern, term in zip(VENDOR_PATTERNS, VENDOR_TERMS):
        if term in seen:
            continue
        if pattern.search(text):
            hits.append(term)
            seen.add(term)
    return hits


def infer_level(filename: str) -> Optional[int]:
    match = re.match(r"^lvl([123])_", os.path.basename(filename))
    return int(match.group(1)) if match else None


def name_findings(filename: str, level: int) -> list[Finding]:
    findings: list[Finding] = []
    base = os.path.basename(filename)
    if level == 3:
        pattern = re.compile(r"^lvl3_v[1-9]\d*_(aws|azure|k8s)_[a-z0-9]+(?:_[a-z0-9]+)*\.xml$")
    else:
        pattern = re.compile(rf"^lvl{level}_v[1-9]\d*_[a-z0-9]+(?:_[a-z0-9]+)*\.xml$")
    if not pattern.match(base):
        expected = (
            "lvl3_v<K>_<aws|azure|k8s>_<drawing_name>.xml"
            if level == 3
            else f"lvl{level}_v<K>_<drawing_name>.xml"
        )
        findings.append(
            Finding("Blocking", "file-name", f"file name '{base}' does not match {expected}")
        )
    return findings


def find_bands(
    cells: dict[str, Cell], children: dict[str, list[str]]
) -> tuple[dict[str, Cell], list[Finding]]:
    findings: list[Finding] = []
    bands: dict[str, Cell] = {}
    for band_id, (label, role) in BAND_IDS.items():
        if band_id in cells and cells[band_id].vertex:
            bands[role] = cells[band_id]
            if label.lower() not in plain_text(cells[band_id].value).lower():
                findings.append(
                    Finding(
                        "Major",
                        "band-label",
                        f"band '{band_id}' should be labelled '{label}'",
                        band_id,
                    )
                )
            continue
        # Fall back to a label match, then report the non-standard ID.
        for cell in cells.values():
            if is_group(cell, children, cells) and label.lower() in plain_text(cell.value).lower():
                bands[role] = cell
                findings.append(
                    Finding(
                        "Major",
                        "band-id",
                        f"band '{label}' must use id '{band_id}'",
                        cell.id,
                    )
                )
                break
        if role not in bands:
            findings.append(
                Finding("Blocking", "band-missing", f"missing band '{label}' (id '{band_id}')")
            )
    return bands, findings


def band_of(
    cell: Cell, cells: dict[str, Cell], bands: dict[str, Cell]
) -> Optional[str]:
    band_ids = {band.id: role for role, band in bands.items()}
    current: Optional[str] = cell.parent
    seen: set[str] = set()
    while current and current in cells and current not in seen:
        seen.add(current)
        if current in band_ids:
            return band_ids[current]
        current = cells[current].parent
    return None


def validate(path: str, level: int) -> tuple[list[Finding], dict[str, int]]:
    findings: list[Finding] = []
    if not os.path.exists(path):
        return [Finding("Blocking", "file-missing", f"file not found: {path}")], {}
    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        return [Finding("Blocking", "xml-parse", f"invalid XML: {exc}")], {}

    root = tree.getroot()
    if root.tag != "mxfile":
        findings.append(Finding("Blocking", "xml-root", "root element must be <mxfile>"))
        return findings, {}
    diagrams = root.findall("diagram")
    if len(diagrams) != 1:
        findings.append(
            Finding("Blocking", "diagram-count", f"expected exactly one <diagram>, found {len(diagrams)}")
        )
    if not diagrams:
        return findings, {}
    model = diagrams[0].find("mxGraphModel")
    if model is None:
        findings.append(Finding("Blocking", "graph-model", "missing <mxGraphModel>"))
        return findings, {}
    model_root = model.find("root")
    if model_root is None:
        findings.append(Finding("Blocking", "graph-root", "missing <root>"))
        return findings, {}

    cells, parse_findings = parse_cells(model_root)
    findings.extend(parse_findings)
    if not cells:
        findings.append(Finding("Blocking", "no-cells", "no mxCell elements found"))
        return findings, {}

    children = children_map(cells)
    leaf_vertices = [
        cell
        for cell in cells.values()
        if cell.vertex
        and not is_group(cell, children, cells)
        and "edgelabel" not in cell.style.lower()
        and not is_excluded_id(cell.id)
    ]
    edges = [cell for cell in cells.values() if cell.edge]

    # Title block.
    title_cells = [
        cell for cell in cells.values() if cell.id == "title" or cell.id.startswith("title-")
    ]
    if not title_cells:
        findings.append(Finding("Major", "title-missing", "missing title cell with id 'title'"))
    else:
        title = plain_text(title_cells[0].value)
        if not title:
            findings.append(Finding("Major", "title-empty", "title cell is empty", title_cells[0].id))
        else:
            if not VERSION_PATTERN.search(title):
                findings.append(
                    Finding("Major", "title-version", "title must include a version such as 'v1'", title_cells[0].id)
                )
            if not STATUS_PATTERN.search(title):
                findings.append(
                    Finding(
                        "Major",
                        "title-status",
                        "title must include a status: Draft, In review, Confirmed, or Superseded",
                        title_cells[0].id,
                    )
                )

    # Empty labels on boxes.
    for cell in leaf_vertices:
        if not plain_text(cell.value):
            findings.append(Finding("Major", "empty-label", f"box '{cell.id}' has no label", cell.id))

    # Edges: endpoints and labels.
    for edge in edges:
        if not edge.source or not edge.target:
            findings.append(
                Finding("Blocking", "edge-endpoints", f"edge '{edge.id}' has no source or target", edge.id)
            )
        else:
            for endpoint, label in ((edge.source, "source"), (edge.target, "target")):
                if endpoint not in cells:
                    findings.append(
                        Finding(
                            "Blocking",
                            "edge-dangling",
                            f"edge '{edge.id}' {label} '{endpoint}' does not exist",
                            edge.id,
                        )
                    )
                elif not cells[endpoint].vertex:
                    findings.append(
                        Finding(
                            "Blocking",
                            "edge-nonvertex",
                            f"edge '{edge.id}' {label} '{endpoint}' is not a box",
                            edge.id,
                        )
                    )
        label = edge_label(edge, cells)
        if not label:
            findings.append(Finding("Blocking", "edge-label", f"edge '{edge.id}' has no label", edge.id))
            continue
        if level in (2, 3):
            if not TAG_PATTERN.search(label):
                findings.append(
                    Finding(
                        "Blocking",
                        "edge-protocol",
                        f"edge '{edge.id}' label must start with a [protocol] tag: '{label}'",
                        edge.id,
                    )
                )
            elif not TAG_PATTERN.sub("", label).strip():
                findings.append(
                    Finding(
                        "Major",
                        "edge-description",
                        f"edge '{edge.id}' needs an action description after the protocol tag",
                        edge.id,
                    )
                )

    # Bands, tags, bullets.
    bands: dict[str, Cell] = {}
    if level in (2, 3):
        bands, band_findings = find_bands(cells, children)
        findings.extend(band_findings)
        if len(bands) == 3:
            rects = {role: abs_rect(cell, cells) for role, cell in bands.items()}
            rep, bus, repo = rects["representation"], rects["business"], rects["repository"]
            if not (rep[1] < bus[1] < repo[1]):
                findings.append(
                    Finding("Blocking", "band-order", "bands must be ordered top to bottom: Representation, Business logic, Repository")
                )
            if rep[1] + rep[3] > bus[1] + 2 or bus[1] + bus[3] > repo[1] + 2:
                findings.append(Finding("Major", "band-overlap", "bands overlap vertically"))
            for role in ("representation", "business", "repository"):
                if abs(rects[role][0] - rep[0]) > 2 or abs(rects[role][2] - rep[2]) > 2:
                    findings.append(
                        Finding("Major", "band-align", f"band '{BAND_LABELS[role]}' is not aligned with the other bands")
                    )
                    break

        for cell in leaf_vertices:
            role = band_of(cell, cells, bands)
            if role is None:
                continue
            if not TAG_PATTERN.search(plain_text(cell.value)):
                findings.append(
                    Finding(
                        "Blocking",
                        "tech-tag",
                        f"box '{cell.id}' in the {BAND_LABELS[role]} band needs a [technology] tag",
                        cell.id,
                    )
                )
            if role == "business":
                raw = cell.value.lower()
                lines = [line for line in plain_text(cell.value).splitlines() if line.strip()]
                has_bullets = "<li" in raw or "•" in cell.value or len(lines) >= 2
                if not has_bullets:
                    findings.append(
                        Finding(
                            "Major",
                            "business-bullets",
                            f"business box '{cell.id}' must list what it does as bullet points",
                            cell.id,
                        )
                    )

        for role, band in bands.items():
            if not any(band_of(cell, cells, bands) == role for cell in leaf_vertices):
                findings.append(
                    Finding(
                        "Major",
                        "band-empty",
                        f"band '{BAND_LABELS[role]}' has no boxes",
                        band.id,
                    )
                )
            band_rect = abs_rect(band, cells)
            start_match = re.search(r"startSize=(\d+)", band.style)
            header = int(start_match.group(1)) if start_match else 0
            for cell in leaf_vertices:
                if band_of(cell, cells, bands) != role:
                    continue
                rect = abs_rect(cell, cells)
                if (
                    rect[0] < band_rect[0] - 2
                    or rect[1] < band_rect[1] + header - 2
                    or rect[0] + rect[2] > band_rect[0] + band_rect[2] + 2
                    or rect[1] + rect[3] > band_rect[1] + band_rect[3] + 2
                ):
                    findings.append(
                        Finding(
                            "Major",
                            "band-containment",
                            f"box '{cell.id}' extends outside the {BAND_LABELS[role]} band",
                            cell.id,
                        )
                    )

    # Vendor leakage at Level 1 and 2.
    if level in (1, 2):
        for cell in [*leaf_vertices, *edges]:
            text = plain_text(cell.value) if cell.vertex else edge_label(cell, cells)
            if not text or is_excluded_id(cell.id):
                continue
            hits = vendor_hits(text)
            if hits:
                findings.append(
                    Finding(
                        "Blocking",
                        "vendor-leak",
                        f"'{cell.id}' names specific technology/vendor ({', '.join(hits)}); use a generic category",
                        cell.id,
                    )
                )

    # Queue/stream/broker services are never boxes, at any level.
    for cell in leaf_vertices:
        title = first_line(cell.value)
        if title and QUEUE_PATTERN.search(title):
            findings.append(
                Finding(
                    "Blocking",
                    "queue-box",
                    f"'{cell.id}' looks like a queue/stream/broker box; show it as [queue message] / [event stream] on the edge",
                    cell.id,
                )
            )

    # Orphans.
    connected: set[str] = set()
    for edge in edges:
        if edge.source:
            connected.add(edge.source)
        if edge.target:
            connected.add(edge.target)
    for cell in leaf_vertices:
        if cell.id not in connected:
            findings.append(
                Finding("Major", "orphan-box", f"box '{cell.id}' is not connected to any edge", cell.id)
            )

    # Overlaps.
    for index, first in enumerate(leaf_vertices):
        first_rect = abs_rect(first, cells)
        for second in leaf_vertices[index + 1 :]:
            second_rect = abs_rect(second, cells)
            overlap_x = min(first_rect[0] + first_rect[2], second_rect[0] + second_rect[2]) - max(
                first_rect[0], second_rect[0]
            )
            overlap_y = min(first_rect[1] + first_rect[3], second_rect[1] + second_rect[3]) - max(
                first_rect[1], second_rect[1]
            )
            if overlap_x > 1.0 and overlap_y > 1.0:
                findings.append(
                    Finding(
                        "Blocking",
                        "box-overlap",
                        f"boxes '{first.id}' and '{second.id}' overlap",
                        first.id,
                    )
                )

    # Edge geometry.
    polylines: dict[str, list[tuple[float, float]]] = {}
    for edge in edges:
        if not edge.source or not edge.target:
            continue
        if edge.source not in cells or edge.target not in cells:
            continue
        if is_group(cells[edge.source], children, cells) or is_group(cells[edge.target], children, cells):
            findings.append(
                Finding(
                    "Minor",
                    "edge-container",
                    f"edge '{edge.id}' attaches to a container; connect leaf boxes instead",
                    edge.id,
                )
            )
            continue
        polyline = edge_polyline(edge, cells)
        if polyline:
            polylines[edge.id] = polyline
        else:
            findings.append(
                Finding("Blocking", "edge-geometry", f"edge '{edge.id}' has no usable geometry", edge.id)
            )

    # Edge crossings and edges through boxes.
    edge_list = [edge for edge in edges if edge.id in polylines]
    for index, first in enumerate(edge_list):
        first_points = polylines[first.id]
        first_segments = list(zip(first_points, first_points[1:]))
        for second in edge_list[index + 1 :]:
            second_points = polylines[second.id]
            same_pair = {first.source, first.target} == {second.source, second.target}
            if same_pair and len(first_points) == len(second_points):
                same_route = all(
                    points_close(a, b) for a, b in zip(first_points, second_points)
                ) or all(
                    points_close(a, b) for a, b in zip(first_points, reversed(second_points))
                )
                if same_route:
                    findings.append(
                        Finding(
                            "Blocking",
                            "edge-overlap",
                            f"edges '{first.id}' and '{second.id}' occupy the same route",
                            first.id,
                        )
                    )
                    continue
            shared_vertices = {
                endpoint
                for endpoint in (first.source, first.target)
                if endpoint and endpoint in (second.source, second.target)
            }
            second_segments = list(zip(second_points, second_points[1:]))
            for first_index, first_segment in enumerate(first_segments):
                if first.source in shared_vertices and first_index == 0:
                    continue
                if first.target in shared_vertices and first_index == len(first_segments) - 1:
                    continue
                for second_index, second_segment in enumerate(second_segments):
                    if second.source in shared_vertices and second_index == 0:
                        continue
                    if second.target in shared_vertices and second_index == len(second_segments) - 1:
                        continue
                    intersection = segment_intersection(*first_segment, *second_segment)
                    if intersection is None:
                        continue
                    _, point = intersection
                    shared_centers = [
                        rect_center(abs_rect(cells[vertex], cells))
                        for vertex in shared_vertices
                        if vertex in cells
                    ]
                    if any(points_close(point, center, 3.0) for center in shared_centers):
                        continue
                    findings.append(
                        Finding(
                            "Blocking",
                            "edge-crossing",
                            f"edge '{first.id}' crosses edge '{second.id}' at ({point[0]:.0f}, {point[1]:.0f})",
                            first.id,
                        )
                    )

    for edge in edge_list:
        if not edge.source or not edge.target:
            continue
        points = polylines[edge.id]
        for segment in zip(points, points[1:]):
            for cell in leaf_vertices:
                if cell.id in (edge.source, edge.target):
                    continue
                if segment_intersects_rect(segment[0], segment[1], abs_rect(cell, cells)):
                    findings.append(
                        Finding(
                            "Blocking",
                            "edge-through-box",
                            f"edge '{edge.id}' passes through box '{cell.id}'",
                            edge.id,
                        )
                    )

    counts = {
        "cells": len(cells),
        "vertices": sum(1 for cell in cells.values() if cell.vertex),
        "edges": len(edges),
        "critical": sum(1 for finding in findings if finding.severity == "Blocking"),
        "major": sum(1 for finding in findings if finding.severity == "Major"),
        "minor": sum(1 for finding in findings if finding.severity == "Minor"),
    }
    return findings, counts


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a C4 draw.io XML drawing.")
    parser.add_argument("file", help="path to the draw.io XML file")
    parser.add_argument("--level", type=int, choices=(1, 2, 3), help="C4 level (inferred from the file name if omitted)")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args()

    inferred = infer_level(args.file)
    level = args.level or inferred
    if level is None:
        print("error: cannot infer the C4 level from the file name; pass --level", file=sys.stderr)
        return 2

    findings = name_findings(args.file, level)
    if args.level and inferred and args.level != inferred:
        findings.append(
            Finding(
                "Blocking",
                "level-mismatch",
                f"--level {args.level} does not match the file name (level {inferred})",
            )
        )
    file_findings, counts = validate(args.file, level)
    findings.extend(file_findings)

    # De-duplicate identical findings.
    seen: set[tuple[str, str, str, str]] = set()
    unique: list[Finding] = []
    for finding in findings:
        key = (finding.severity, finding.code, finding.cell, finding.message)
        if key not in seen:
            seen.add(key)
            unique.append(finding)
    findings = sorted(
        unique,
        key=lambda finding: {"Blocking": 0, "Major": 1, "Minor": 2}[finding.severity],
    )
    counts = {
        "cells": counts.get("cells", 0),
        "vertices": counts.get("vertices", 0),
        "edges": counts.get("edges", 0),
        "critical": sum(1 for finding in findings if finding.severity == "Blocking"),
        "major": sum(1 for finding in findings if finding.severity == "Major"),
        "minor": sum(1 for finding in findings if finding.severity == "Minor"),
    }
    passed = counts["critical"] == 0

    if args.json:
        print(
            json.dumps(
                {
                    "file": args.file,
                    "level": level,
                    "pass": passed,
                    "counts": counts,
                    "findings": [finding.__dict__ for finding in findings],
                },
                indent=2,
            )
        )
    else:
        print(f"C4 draw.io validation: {args.file}")
        print(f"Level: {level}")
        print(
            f"Cells: {counts['cells']} ({counts['vertices']} vertices, {counts['edges']} edges)"
        )
        if not findings:
            print("No findings. PASS.")
        else:
            for severity in ("Blocking", "Major", "Minor"):
                group = [finding for finding in findings if finding.severity == severity]
                if not group:
                    continue
                print(f"\n{severity} ({len(group)})")
                for finding in group:
                    location = f" [{finding.cell}]" if finding.cell else ""
                    print(f"- {finding.code}{location}: {finding.message}")
        print(
            f"\nResult: {'PASS' if passed else 'FAIL'} "
            f"(Blocking {counts['critical']}, Major {counts['major']}, Minor {counts['minor']})"
        )
        if not passed:
            print("Fix every Blocking finding and re-run the validator.")
        elif counts["major"]:
            print("Resolve the Major findings or record why they are accepted before confirmation.")

    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
