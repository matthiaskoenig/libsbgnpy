"""Display information from SBGN files."""

from pathlib import Path

from libsbgnpy import *


def info_example() -> None:
    """Example demonstrating how to print information from SBGN."""

    # file to process
    f_sgbn: Path = Path(__file__).parent / "sbgn/adh.sbgn"

    # sbgn and map
    console.rule("Map", align="left", style="white")
    console.print(f"file://{f_sgbn}")
    sbgn: Sbgn = read_sbgn_from_file(f_sgbn)
    map: Map = sbgn.map[0]
    console.print(f"Language: {map.language}")

    # get bbox for map
    """<bbox x="0" y="0" w="363" h="253"/>"""
    bbox: Bbox = map.bbox
    console.print(bbox)

    # glyphs
    console.rule("Glyphs", align="left", style="white")
    """
    <glyph class="simple chemical" id="glyph1">
            <label text="Ethanol"/> <!-- fontsize="" etc -->
            <!-- Line breaks are allowed in the text attribute -->
            <bbox x="40" y="120" w="60" h="60"/>
        </glyph>
    """
    glyphs: list[Glyph] = map.glyph
    for g in glyphs:
        # console.print(g)
        console.print(g.id, g.class_value)
        if g.label:
            console.print(g.label.text)
        if g.bbox:
            bbox = g.bbox
            console.print(f"x={bbox.x}, y={bbox.y}, w={bbox.w}, h={bbox.h}")

    # arcs
    console.rule("Arcs", align="left", style="white")
    """
    <arc class="consumption" source="glyph_nad" target="pn1.1" id="a06">
        <start x="95" y="202" />
        <end x="136" y="180" />
    </arc>
    """
    arcs: list[Arc] = map.arc
    for a in arcs:
        # console.print(a)
        console.print(a.id, a.class_value, a.source, a.target)
        console.print(f"start: ({a.start.x}, {a.start.y}")
        console.print(f"end: ({a.end.x}, {a.end.y}")

    console.rule(style="white")


if __name__ == "__main__":
    info_example()
