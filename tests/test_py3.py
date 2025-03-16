from pathlib import Path
from libsbgnpy import libsbgn
from libsbgnpy.libsbgnTypes import ArcClass, GlyphClass, Language


def test_basestring_issue(tmpdir: Path) -> None:
    """
    This tests issue: https://github.com/matthiaskoenig/libsbgnpy/issues/4
    """
    # create empty sbgn
    sbgn = libsbgn.sbgn()

    # create map, set language and set in sbgn
    sbgn_map = libsbgn.map()
    sbgn_map.set_language(Language.PD)
    sbgn.set_map(sbgn_map)

    # create a bounding box for the map
    box = libsbgn.bbox(0, 0, 100, 100)
    sbgn_map.set_bbox(box)

    # glyphs with labels
    for comp in ("Cytoplasm",):
        c_id = comp
        c_name = comp
        (x, y), (w, h) = (10, 10), (90, 90)
        g = libsbgn.glyph(class_=GlyphClass.COMPARTMENT, id=c_id)
        g.set_label(libsbgn.label(text=c_name, bbox=libsbgn.bbox(x, y, w, h)))
        g.set_bbox(libsbgn.bbox(x, y, w, h))
        sbgn_map.add_glyph(g)

    s2xy = {"H2": (20, 20), "O2": (20, 80), "H2O": (80, 60)}
    for species, (x, y) in s2xy.items():
        s_id = species
        s_name = species
        glyph_type = GlyphClass.UNSPECIFIED_ENTITY
        glyph_type = GlyphClass.SIMPLE_CHEMICAL

        (w, h) = (5, 5)
        g = libsbgn.glyph(class_=glyph_type, id=s_id, compartmentRef="Cytoplasm")
        g.set_label(
            libsbgn.label(
                text=s_name,
                bbox=libsbgn.bbox(x + w * 0.1, y + h * 0.1, w * 0.8, h * 0.8),
            )
        )
        g.set_bbox(libsbgn.bbox(x, y, w, h))
        sbgn_map.add_glyph(g)

    # glyph with ports (process)
    r_id = "Water"
    (x, y), (w, h) = (60, 60), (4, 4)
    g = libsbgn.glyph(class_=GlyphClass.PROCESS, id=r_id)
    g.set_bbox(libsbgn.bbox(x, y, w, h))

    in_port = None
    for s_id in ("O2", "H2"):
        if not in_port:
            port_x, port_y = (61, 62)
            in_port = libsbgn.port(x=port_x, y=port_y, id="%s__in" % r_id)
            g.add_port(in_port)

        sref_id = s_id
        a = libsbgn.arc(
            class_=ArcClass.CONSUMPTION,
            target=in_port.get_id(),
            source=sref_id,
            id="a_%s_%s" % (s_id, r_id),
        )
        s_x, s_y = s2xy[s_id]
        a.set_start(libsbgn.startType(x=s_x, y=s_y))
        a.set_end(libsbgn.endType(x=in_port.get_x(), y=in_port.get_y()))
        sbgn_map.add_arc(a)
    out_port = None
    for s_id in ("H2O",):
        if not out_port:
            port_x, port_y = (63, 62)
            out_port = libsbgn.port(x=port_x, y=port_y, id="%s__out" % r_id)
            g.add_port(out_port)
        sref_id = s_id
        a = libsbgn.arc(
            class_=ArcClass.PRODUCTION,
            target=sref_id,
            source=out_port.get_id(),
            id="a_%s_%s" % (r_id, s_id),
        )
        s_x, s_y = s2xy[s_id]
        a.set_end(libsbgn.startType(x=s_x, y=s_y))
        a.set_start(libsbgn.endType(x=out_port.get_x(), y=out_port.get_y()))
        sbgn_map.add_arc(a)
    sbgn_map.add_glyph(g)

    # write everything to a file
    sbgn.write_file(tmpdir / "test.sbgn")
