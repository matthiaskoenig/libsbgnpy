# -*- coding: utf-8 -*-
"""
Write and read notes information.
Notes must be XML elements in a <notes>Tag</notes>
"""

from libsbgnpy import Language, Notes, libsbgn, utils


def write_glyph_notes(f):
    """Set notes on element.

    :return: None
    """
    sbgn = libsbgn.sbgn()
    map = libsbgn.map()
    map.set_language(Language.PD)
    sbgn.set_map(map)

    # create a glyph with an id and class "macromolecule"
    g = libsbgn.glyph()
    g.set_id("g1")

    # define a label for this glyph
    label = libsbgn.label()
    label.set_text("INSR")

    bbox = libsbgn.bbox(x=100, y=100, w=80, h=40)
    g.set_bbox(bbox)
    map.add_glyph(g)

    notes = Notes(
        """
    <body xmlns="http://www.w3.org/1999/xhtml">
        This is an example note describing the INSR glyph.
    </body>"""
    )
    g.set_notes(notes)

    print(utils.write_to_string(sbgn))
    utils.write_to_file(sbgn=sbgn, f=f)


def read_glyph_notes(f):
    """Read notes from glyphs.

    :return: None
    """
    sbgn = utils.read_from_file(f=f)

    # map is a container for the glyphs and arcs
    map = sbgn.get_map()

    glyphs = map.get_glyph()
    for g in glyphs:
        notes = g.get_notes()
        if notes:
            print(g.get_id())
            print(notes)


if __name__ == "__main__":
    f = "sbgn/notes.sbgn"
    write_glyph_notes(f)
    print("_" * 80, "\n")
    read_glyph_notes(f)
