"""
Some examples for the creation of SBGN files from scratch.
"""

from pathlib import Path
import libsbgnpy.libsbgn as libsbgn
from libsbgnpy.libsbgnTypes import ArcClass, GlyphClass, Language, Orientation


def write_sbgn_01(f: Path) -> None:
    """Create SBGN and write to file.

    Macromolecule box with label.

    :param f: file to write to
    :return:
    """
    sbgn = libsbgn.sbgn()
    map = libsbgn.map()
    map.set_language(Language.PD)
    sbgn.set_map(map)

    # create a glyph with an id and class "macromolecule"
    g1 = libsbgn.glyph()
    g1.set_id("glyph1")
    g1.set_class(GlyphClass.MACROMOLECULE)

    # add the glyph to the map
    map.add_glyph(g1)

    # define the bounding box of the glyph
    bbox1 = libsbgn.bbox(x=125, y=60, w=100, h=40)
    g1.set_bbox(bbox1)

    # define a label for this glyph
    label1 = libsbgn.label()
    label1.set_text("P53")

    # now write everything to disk
    sbgn.write_file(f)


def write_sbgn_02(f: Path) -> None:
    """Create SBGN document and write to file.

    :param f:
    :return:
    """
    # create empty sbgn
    sbgn = libsbgn.sbgn()

    # create map, set language and set in sbgn
    map = libsbgn.map()
    map.set_language(Language.PD)
    sbgn.set_map(map)

    # create a bounding box for map
    # <bbox x="0" y="0" w="363" h="253"/>
    # [1] de novo and set all attributes
    # box = libsbgn.bbox()
    # box.set_x(0)
    # box.set_y(0)
    # box.set_w(363)
    # box.set_h(253)
    # [2] de novo with attributes at creation
    box = libsbgn.bbox(x=0, y=0, w=363, h=253)
    map.set_bbox(box)

    # create some glyphs
    # class attribute is named 'class_' ! in glyphs and arcs
    """
        <glyph class="simple chemical" id="glyph1">
            <label text="Ethanol"/> <!-- fontsize="" etc -->
            <!-- Line breaks are allowed in the text attribute -->
            <bbox x="40" y="120" w="60" h="60"/>
        </glyph>
    """
    # glyphs with labels
    g = libsbgn.glyph(class_=GlyphClass.SIMPLE_CHEMICAL, id="glyph1")
    g.set_label(libsbgn.label(text="Ethanol"))
    g.set_bbox(libsbgn.bbox(x=40, y=120, w=60, h=60))
    map.add_glyph(g)

    g = libsbgn.glyph(class_=GlyphClass.SIMPLE_CHEMICAL, id="glyph_ethanal")
    g.set_label(libsbgn.label(text="Ethanal"))
    g.set_bbox(libsbgn.bbox(x=220, y=110, w=60, h=60))
    map.add_glyph(g)

    g = libsbgn.glyph(class_=GlyphClass.MACROMOLECULE, id="glyph_adh1")
    g.set_label(libsbgn.label(text="ADH1"))
    g.set_bbox(libsbgn.bbox(x=106, y=20, w=108, h=60))
    map.add_glyph(g)

    g = libsbgn.glyph(class_=GlyphClass.SIMPLE_CHEMICAL, id="glyph_h")
    g.set_label(libsbgn.label(text="H+"))
    g.set_bbox(libsbgn.bbox(x=220, y=190, w=60, h=60))
    map.add_glyph(g)

    g = libsbgn.glyph(class_=GlyphClass.SIMPLE_CHEMICAL, id="glyph_nad")
    g.set_label(libsbgn.label(text="NAD+"))
    g.set_bbox(libsbgn.bbox(x=40, y=190, w=60, h=60))
    map.add_glyph(g)

    g = libsbgn.glyph(class_=GlyphClass.SIMPLE_CHEMICAL, id="glyph_nadh")
    g.set_label(libsbgn.label(text="NADH"))
    g.set_bbox(libsbgn.bbox(x=300, y=150, w=60, h=60))
    map.add_glyph(g)

    # glyph with ports (process)
    g = libsbgn.glyph(
        class_=GlyphClass.PROCESS, id="pn1", orientation=Orientation.HORIZONTAL
    )
    g.set_bbox(libsbgn.bbox(x=148, y=168, w=24, h=24))
    g.add_port(libsbgn.port(x=136, y=180, id="pn1.1"))
    g.add_port(libsbgn.port(x=184, y=180, id="pn1.2"))
    map.add_glyph(g)

    # arcs
    # create arcs and set the start and end points
    a = libsbgn.arc(
        class_=ArcClass.CONSUMPTION, source="glyph1", target="pn1.1", id="a01"
    )
    a.set_start(libsbgn.startType(x=98, y=160))
    a.set_end(libsbgn.endType(x=136, y=180))
    map.add_arc(a)

    a = libsbgn.arc(
        class_=ArcClass.PRODUCTION, source="pn1.2", target="glyph_nadh", id="a02"
    )
    a.set_start(libsbgn.startType(x=184, y=180))
    a.set_end(libsbgn.endType(x=300, y=180))
    map.add_arc(a)

    a = libsbgn.arc(
        class_=ArcClass.CATALYSIS, source="glyph_adh1", target="pn1", id="a03"
    )
    a.set_start(libsbgn.startType(x=160, y=80))
    a.set_end(libsbgn.endType(x=160, y=168))
    map.add_arc(a)

    a = libsbgn.arc(
        class_=ArcClass.PRODUCTION, source="pn1.2", target="glyph_h", id="a04"
    )
    a.set_start(libsbgn.startType(x=184, y=180))
    a.set_end(libsbgn.endType(x=224, y=202))
    map.add_arc(a)

    a = libsbgn.arc(
        class_=ArcClass.PRODUCTION, source="pn1.2", target="glyph_ethanal", id="a05"
    )
    a.set_start(libsbgn.startType(x=184, y=180))
    a.set_end(libsbgn.endType(x=224, y=154))
    map.add_arc(a)

    a = libsbgn.arc(
        class_=ArcClass.CONSUMPTION, source="glyph_nad", target="pn1.1", id="a06"
    )
    a.set_start(libsbgn.startType(x=95, y=202))
    a.set_end(libsbgn.endType(x=136, y=180))
    map.add_arc(a)

    # write to file
    sbgn.write_file(f)


def write_sbgn_03(f: Path) -> None:
    """Create SBGN with annotation and write to file.

    :param f: file to write
    :return:
    """
    from libsbgnpy.libsbgn import bbox, calloutType, glyph, label, map, point, sbgn

    doc = sbgn()
    m = map()
    m.set_language(Language.PD)
    doc.set_map(m)

    # create a glyph with an id and class "macromolecule"
    g1 = glyph()
    g1.set_id("g1")
    g1.set_class(GlyphClass.MACROMOLECULE)

    # create a glyph with an id and class "annotation"
    g2 = glyph()
    g2.set_id("g2")
    g2.set_class(GlyphClass.ANNOTATION)

    co = calloutType()
    co.set_target(g1)

    p = point(x=160, y=200)
    co.set_point(p)
    g2.set_callout(co)

    # add the glyph to the map
    m.add_glyph(g1)
    m.add_glyph(g2)

    # define the bounding box of the glyph
    bbox1 = bbox(x=90, y=160, w=380, h=210)
    g1.set_bbox(bbox1)

    # define the bounding box of the annotation
    bbox2 = bbox(x=5, y=5, w=220, h=125)
    g2.set_bbox(bbox2)

    # define a label for this glyph
    label1 = label(text="LABEL")
    g1.set_label(label1)

    # define a label for this annotation
    label2 = label(text="INFO")
    g2.set_label(label2)

    # now write everything to disk
    doc.write_file(f)


if __name__ == "__main__":
    write_sbgn_01("sbgn/test-output-01.sbgn")
    write_sbgn_02("sbgn/test-output-02.sbgn")
    write_sbgn_03("sbgn/test-output-03.sbgn")
