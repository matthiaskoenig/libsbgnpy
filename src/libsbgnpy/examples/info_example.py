# -*- coding: utf-8 -*-
"""
Display information from SBGN files.
"""

from pathlib import Path

import libsbgnpy.libsbgn as libsbgn  # import the bindings
from libsbgnpy.utils import print_bbox  # some additional helpers


def info_example() -> None:
    """Example demonstrating how to print information from SBGN."""
    print(libsbgn.__all__)

    # file to process
    f_sgbn: Path = Path(__file__).parent / "sbgn/adh.sbgn"

    # sbgn and map
    sbgn = libsbgn.parse(f_sgbn)
    map = sbgn.get_map()
    print("Language:", map.get_language())

    # get bbox for map
    """<bbox x="0" y="0" w="363" h="253"/>"""
    box = map.get_bbox()
    print("x, y, w, h : ", box.get_x(), box.get_y(), box.get_w(), box.get_h())

    # glyphs
    """
    <glyph class="simple chemical" id="glyph1">
            <label text="Ethanol"/> <!-- fontsize="" etc -->
            <!-- Line breaks are allowed in the text attribute -->
            <bbox x="40" y="120" w="60" h="60"/>
        </glyph>
    """
    glyphs = map.get_glyph()
    for g in glyphs:
        cls = g.get_class()
        print(cls, g.get_id())
        label = g.get_label()
        if cls == "simple chemical":
            print("label: ", label.get_text())

        if cls == "process":
            for p in g.get_port():
                print("port ", p.get_id(), p.get_x(), p.get_y())

        box = g.get_bbox()
        print_bbox(box)
        print

    # arcs
    """
        <arc class="consumption" source="glyph_nad" target="pn1.1" id="a06">
            <start x="95" y="202" />
            <end x="136" y="180" />
        </arc>
    """
    arcs = map.get_arc()
    for a in arcs:
        print(a.get_class(), a.get_source(), a.get_target(), a.get_id())
        start = a.get_start()
        print(start.x, start.y)
        end = a.get_end()
        print(end.x, end.y)


if __name__ == "__main__":
    info_example()
