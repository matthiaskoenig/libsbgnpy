"""Tests of core functionality."""

import pytest

from libsbgnpy import *


@pytest.fixture
def sbgn() -> Sbgn:
    """Fixture provides sbgn test data via sbgn argument."""
    # create map with bounding box
    map = Map(
        language=MapLanguage.PROCESS_DESCRIPTION,
        bbox=Bbox(x=0, y=0, w=363, h=253),
    )
    sbgn = Sbgn(map=[map])

    # create some glyphs
    map.glyph = [
        # simple glyph
        Glyph(
            class_value=GlyphClass.SIMPLE_CHEMICAL,
            id="glyph1",
            label=Label(text="Ethanol"),
            bbox=Bbox(x=40, y=120, w=60, h=60),
        ),
        # glyph with ports (process)
        Glyph(
            class_value=GlyphClass.PROCESS,
            id="pn1",
            orientation=GlyphOrientation.HORIZONTAL,
            bbox=Bbox(x=148, y=168, w=24, h=24),
            port=[
                Port(x=136, y=180, id="pn1.1"),
                Port(x=184, y=180, id="pn1.2"),
            ],
        ),
    ]

    # arcs
    # create arcs and set the start and end points
    map.arc = [
        Arc(
            class_value=ArcClass.CONSUMPTION,
            source="glyph1",
            target="pn1.1",
            id="a01",
            start=Arc.Start(x=98, y=160),
            end=Arc.End(x=136, y=180),
        )
    ]
    return sbgn


def test_sbgn_exists(sbgn: Sbgn) -> None:
    assert sbgn is not None


def test_map_exists(sbgn: Sbgn) -> None:
    assert sbgn.map[0] is not None


def test_map_language(sbgn: Sbgn) -> None:
    map = sbgn.map[0]
    assert map.language == MapLanguage.PROCESS_DESCRIPTION


def test_map_box_exists(sbgn: Sbgn) -> None:
    assert sbgn.map[0].bbox is not None


def test_map_box_x(sbgn: Sbgn) -> None:
    bbox = sbgn.map[0].bbox
    assert bbox.x == 0


def test_map_box_y(sbgn: Sbgn) -> None:
    bbox = sbgn.map[0].bbox
    assert bbox.y == 0


def test_map_box_w(sbgn: Sbgn) -> None:
    bbox = sbgn.map[0].bbox
    assert bbox.w == 363


def test_map_box_h(sbgn: Sbgn) -> None:
    bbox = sbgn.map[0].bbox
    assert bbox.h == 253


def test_glyph_exists(sbgn: Sbgn) -> None:
    glyphs = sbgn.map[0].glyph
    assert len(glyphs) == 2


def test_glyph_ids(sbgn: Sbgn) -> None:
    glyphs = sbgn.map[0].glyph
    assert glyphs[0].id == "glyph1"
    assert glyphs[1].id == "pn1"


def test_glyph_classes(sbgn: Sbgn) -> None:
    glyphs = sbgn.map[0].glyph
    assert glyphs[0].class_value == GlyphClass.SIMPLE_CHEMICAL
    assert glyphs[1].class_value == GlyphClass.PROCESS


def test_glyph_labels(sbgn: Sbgn) -> None:
    glyphs = sbgn.map[0].glyph
    assert glyphs[0].label.text == "Ethanol"


def test_glyph_bboxes(sbgn: Sbgn) -> None:
    glyphs = sbgn.map[0].glyph
    bbox = glyphs[0].bbox
    assert bbox.x == 40
    assert bbox.y == 120
    assert bbox.w == 60
    assert bbox.h == 60

    bbox = glyphs[1].bbox
    assert bbox.x == 148
    assert bbox.y == 168
    assert bbox.w == 24
    assert bbox.h == 24


def test_glyph_ports(sbgn: Sbgn) -> None:
    glyphs = sbgn.map[0].glyph
    ports = glyphs[1].port
    assert ports[0].x == 136
    assert ports[0].y == 180
    assert ports[0].id == "pn1.1"

    assert ports[1].x == 184
    assert ports[1].y == 180
    assert ports[1].id == "pn1.2"


def test_arc_exists(sbgn: Sbgn) -> None:
    arcs = sbgn.map[0].arc
    assert len(arcs) == 1


def test_arc_start(sbgn: Sbgn) -> None:
    arc = sbgn.map[0].arc[0]
    start = arc.start
    assert start is not None
    assert start.x == 98
    assert start.y == 160


def test_arc_end(sbgn: Sbgn) -> None:
    arc = sbgn.map[0].arc[0]
    end = arc.end
    assert end is not None
    assert end.x == 136
    assert end.y == 180


def test_glyph_class(sbgn: Sbgn) -> None:
    g1 = Glyph(class_value=GlyphClass.SIMPLE_CHEMICAL, id="glyph1")
    assert g1.id == "glyph1"
    assert g1.class_value == GlyphClass.SIMPLE_CHEMICAL

    g2 = Glyph(id="glyph1")
    g2.class_value = GlyphClass.SIMPLE_CHEMICAL
    assert g2.id == "glyph1"
    assert g2.class_value == GlyphClass.SIMPLE_CHEMICAL
