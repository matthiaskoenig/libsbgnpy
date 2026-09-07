"""Read an SBGN document and display its content.

```bash
python examples/read.py
```
"""

from pathlib import Path

from libsbgnpy import Map, Sbgn, read_sbgn_from_file
from libsbgnpy.console import console

SBGN_DIR = Path(__file__).parent / "sbgn"


def read_sbgn(f: Path) -> Sbgn:
    """Read an SBGN file and print the map, its glyphs and its arcs.

    Args:
        f: path of the SBGN file

    Returns:
        The SBGN document.
    """
    sbgn: Sbgn = read_sbgn_from_file(f)
    map: Map = sbgn.map[0]

    console.rule("Map", align="left", style="white")
    console.print(f"file://{f}")
    console.print(f"language: {map.language}")
    console.print(map.bbox)

    console.rule("Glyphs", align="left", style="white")
    for glyph in map.glyph:
        label = glyph.label.text if glyph.label else None
        console.print(f"'{glyph.id}' of class '{glyph.class_value}', label '{label}'")
        if glyph.bbox:
            bbox = glyph.bbox
            console.print(f"  bbox: x={bbox.x}, y={bbox.y}, w={bbox.w}, h={bbox.h}")

    console.rule("Arcs", align="left", style="white")
    for arc in map.arc:
        console.print(
            f"'{arc.id}' of class '{arc.class_value}': '{arc.source}' -> '{arc.target}'"
        )
        if arc.start and arc.end:
            console.print(
                f"  ({arc.start.x}, {arc.start.y}) -> ({arc.end.x}, {arc.end.y})"
            )

    console.rule(style="white")
    return sbgn


if __name__ == "__main__":
    for filename in ["adh.sbgn", "adh_0.3.sbgn", "glycolysis.sbgn"]:
        read_sbgn(SBGN_DIR / filename)
