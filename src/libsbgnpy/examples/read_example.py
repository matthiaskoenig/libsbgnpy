import libsbgnpy.libsbgn as libsbgn


def read_sbgn_01(f):
    """Read example file and display content.

    :param f: SBGN file to read
    :return: sbgn
    """
    sbgn = libsbgn.parse(f)

    # map is a container for the glyphs and arcs
    map = sbgn.get_map()

    # we can get a list of glyphs (nodes) in this map with getGlyph()
    for g in map.get_glyph():
        # print the sbgn class of this glyph
        print(" Glyph with class", g.get_id())

        # if there is a label, print it as well
        if g.get_label():
            print(", and label ", g.get_label().get_text())
        else:
            print(", without label")

    # we can get a list of arcs (edges) in this map with getArc()
    for a in map.get_arc():
        # print the class of this arc
        print(" Arc with class ", a.get_class())

    return sbgn


if __name__ == "__main__":
    read_sbgn_01("sbgn/adh.sbgn")
