"""
Example tests.
"""

import pytest

import libsbgnpy.libsbgn as libsbgn
from libsbgnpy.libsbgnTypes import ArcClass, GlyphClass, Language, Orientation


@pytest.fixture
def sbgn():
    """Fixture provides sbgn test data via sbgn argument."""
    # create empty sbgn
    sbgn = libsbgn.sbgn()
    # create map, set language and set in sbgn
    sbgn_map = libsbgn.map()
    sbgn_map.set_language(Language.PD)
    sbgn.set_map(sbgn_map)

    # create a bounding box for map
    box = libsbgn.bbox(x=0, y=0, w=363, h=253)
    sbgn_map.set_bbox(box)

    # create some glyphs
    # class attribute is named 'class_' ! in glyphs and arcs

    # glyphs with labels
    g = libsbgn.glyph(class_=GlyphClass.SIMPLE_CHEMICAL, id="glyph1")
    g.set_label(libsbgn.label(text="Ethanol"))
    g.set_bbox(libsbgn.bbox(x=40, y=120, w=60, h=60))
    sbgn_map.add_glyph(g)

    # glyph with ports (process)
    g = libsbgn.glyph(
        class_=GlyphClass.PROCESS, id="pn1", orientation=Orientation.HORIZONTAL
    )
    g.set_bbox(libsbgn.bbox(x=148, y=168, w=24, h=24))
    g.add_port(libsbgn.port(x=136, y=180, id="pn1.1"))
    g.add_port(libsbgn.port(x=184, y=180, id="pn1.2"))
    sbgn_map.add_glyph(g)

    # arcs
    # create arcs and set the start and end points
    a = libsbgn.arc(
        class_=ArcClass.CONSUMPTION, source="glyph1", target="pn1.1", id="a01"
    )
    a.set_start(libsbgn.startType(x=98, y=160))
    a.set_end(libsbgn.endType(x=136, y=180))
    sbgn_map.add_arc(a)
    return sbgn


def test_sbgn_exists(sbgn):
    assert sbgn is not None


def test_map_exists(sbgn):
    assert sbgn.get_map() is not None


def test_map_language(sbgn):
    sbgn_map = sbgn.get_map()
    assert sbgn_map.get_language() == Language.PD


def test_map_box_exists(sbgn):
    assert sbgn.get_map().get_bbox() is not None


def test_map_box_x(sbgn):
    bbox = sbgn.get_map().get_bbox()
    assert bbox.get_x() == 0


def test_map_box_y(sbgn):
    bbox = sbgn.get_map().get_bbox()
    assert bbox.get_y() == 0


def test_map_box_w(sbgn):
    bbox = sbgn.get_map().get_bbox()
    bbox.get_w() == 363


def test_map_box_h(sbgn):
    bbox = sbgn.get_map().get_bbox()
    assert bbox.get_h() == 253


def test_glyph_exists(sbgn):
    glyphs = sbgn.get_map().get_glyph()
    assert len(glyphs) == 2


def test_glyph_ids(sbgn):
    glyphs = sbgn.get_map().get_glyph()
    assert glyphs[0].get_id() == "glyph1"
    assert glyphs[1].get_id() == "pn1"


def test_glyph_classes(sbgn):
    glyphs = sbgn.get_map().get_glyph()
    assert glyphs[0].get_class() == GlyphClass.SIMPLE_CHEMICAL
    assert glyphs[1].get_class() == GlyphClass.PROCESS


def test_glyph_labels(sbgn):
    glyphs = sbgn.get_map().get_glyph()
    assert glyphs[0].get_label().get_text() == "Ethanol"


def test_glyph_bboxes(sbgn):
    glyphs = sbgn.get_map().get_glyph()
    bbox = glyphs[0].get_bbox()
    assert bbox.get_x() == 40
    assert bbox.get_y() == 120
    assert bbox.get_w() == 60
    assert bbox.get_h() == 60

    bbox = glyphs[1].get_bbox()
    assert bbox.get_x() == 148
    assert bbox.get_y() == 168
    assert bbox.get_w() == 24
    assert bbox.get_h() == 24


def test_glyph_ports(sbgn):
    glyphs = sbgn.get_map().get_glyph()
    ports = glyphs[1].get_port()
    assert ports[0].get_x() == 136
    assert ports[0].get_y() == 180
    assert ports[0].get_id() == "pn1.1"

    assert ports[1].get_x() == 184
    assert ports[1].get_y() == 180
    assert ports[1].get_id() == "pn1.2"


def test_arc_exists(sbgn):
    arcs = sbgn.get_map().get_arc()
    assert len(arcs) == 1


def test_arc_start(sbgn):
    start = sbgn.get_map().get_arc()[0].get_start()
    assert start is not None
    assert start.get_x() == 98
    assert start.get_y() == 160


def test_arc_end(sbgn):
    end = sbgn.get_map().get_arc()[0].get_end()
    assert end is not None
    assert end.get_x() == 136
    assert end.get_y() == 180


def test_glyph_class(sbgn):
    g1 = libsbgn.glyph(class_=GlyphClass.SIMPLE_CHEMICAL, id="glyph1")
    assert g1.get_id() == "glyph1"
    assert g1.get_class() == GlyphClass.SIMPLE_CHEMICAL

    g2 = libsbgn.glyph(id="glyph1")
    g2.set_class(GlyphClass.SIMPLE_CHEMICAL)
    assert g2.get_id() == "glyph1"
    assert g2.get_class() == GlyphClass.SIMPLE_CHEMICAL
