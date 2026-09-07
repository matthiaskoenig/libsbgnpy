"""Test the SBGN bindings."""

import pytest

from libsbgnpy import (
    Arc,
    ArcClass,
    Bbox,
    Glyph,
    GlyphClass,
    GlyphOrientation,
    Label,
    Map,
    MapLanguage,
    Port,
    Sbgn,
)


@pytest.fixture
def sbgn() -> Sbgn:
    """Map with a simple chemical, a process and a consumption arc."""
    map = Map(
        id="map_test",
        language=MapLanguage.PROCESS_DESCRIPTION,
        bbox=Bbox(x=0, y=0, w=363, h=253),
    )
    sbgn = Sbgn(map=[map])

    map.glyph = [
        Glyph(
            id="glyph1",
            class_value=GlyphClass.SIMPLE_CHEMICAL,
            label=Label(text="Ethanol"),
            bbox=Bbox(x=40, y=120, w=60, h=60),
        ),
        Glyph(
            id="pn1",
            class_value=GlyphClass.PROCESS,
            orientation=GlyphOrientation.HORIZONTAL,
            bbox=Bbox(x=148, y=168, w=24, h=24),
            port=[
                Port(id="pn1.1", x=136, y=180),
                Port(id="pn1.2", x=184, y=180),
            ],
        ),
    ]
    map.arc = [
        Arc(
            id="a01",
            class_value=ArcClass.CONSUMPTION,
            source="glyph1",
            target="pn1.1",
            start=Arc.Start(x=98, y=160),
            end=Arc.End(x=136, y=180),
        )
    ]
    return sbgn


def test_map(sbgn: Sbgn) -> None:
    """The document contains a single process description map."""
    assert len(sbgn.map) == 1
    assert sbgn.map[0].id == "map_test"
    assert sbgn.map[0].language == MapLanguage.PROCESS_DESCRIPTION


def test_map_bbox(sbgn: Sbgn) -> None:
    """The map has a bounding box."""
    bbox = sbgn.map[0].bbox

    assert bbox is not None
    assert (bbox.x, bbox.y, bbox.w, bbox.h) == (0, 0, 363, 253)


def test_glyphs(sbgn: Sbgn) -> None:
    """The map has the two glyphs with their ids and classes."""
    glyphs = sbgn.map[0].glyph

    assert len(glyphs) == 2
    assert [g.id for g in glyphs] == ["glyph1", "pn1"]
    assert glyphs[0].class_value == GlyphClass.SIMPLE_CHEMICAL
    assert glyphs[1].class_value == GlyphClass.PROCESS


def test_glyph_label(sbgn: Sbgn) -> None:
    """The simple chemical is labeled."""
    label = sbgn.map[0].glyph[0].label
    assert label is not None
    assert label.text == "Ethanol"


def test_glyph_bbox(sbgn: Sbgn) -> None:
    """The glyphs have bounding boxes."""
    bbox = sbgn.map[0].glyph[0].bbox
    assert (bbox.x, bbox.y, bbox.w, bbox.h) == (40, 120, 60, 60)

    bbox = sbgn.map[0].glyph[1].bbox
    assert (bbox.x, bbox.y, bbox.w, bbox.h) == (148, 168, 24, 24)


def test_glyph_ports(sbgn: Sbgn) -> None:
    """The process glyph carries the ports the arcs are attached to."""
    ports = sbgn.map[0].glyph[1].port

    assert [(p.id, p.x, p.y) for p in ports] == [
        ("pn1.1", 136, 180),
        ("pn1.2", 184, 180),
    ]


def test_glyph_orientation(sbgn: Sbgn) -> None:
    """The process glyph is oriented."""
    assert sbgn.map[0].glyph[1].orientation == GlyphOrientation.HORIZONTAL


def test_arc(sbgn: Sbgn) -> None:
    """The arc connects the simple chemical with a port of the process."""
    arcs = sbgn.map[0].arc

    assert len(arcs) == 1
    assert arcs[0].id == "a01"
    assert arcs[0].class_value == ArcClass.CONSUMPTION
    assert arcs[0].source == "glyph1"
    assert arcs[0].target == "pn1.1"


def test_arc_start_end(sbgn: Sbgn) -> None:
    """The arc has a start and an end point."""
    arc = sbgn.map[0].arc[0]

    assert (arc.start.x, arc.start.y) == (98, 160)
    assert (arc.end.x, arc.end.y) == (136, 180)
