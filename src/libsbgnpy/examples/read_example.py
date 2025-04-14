"""Example for reading and displaying SBGN content."""

from pathlib import Path

from libsbgnpy import *
from libsbgnpy.console import console
from libsbgnpy.io import read_sbgn_from_file


def read_sbgn_01(f: Path) -> Sbgn:
    """Read example file and display content."""

    # Map
    sbgn: Sbgn = read_sbgn_from_file(f)
    map = sbgn.map[0]

    # Glyphs
    for g in map.glyph:
        console.print(
            f"Glyph '{g.id}' of class '{g.class_value}' and label '{g.label}'."
        )

    # Arcs
    for a in map.arc:
        console.print(f"Arc '{a.id}' with class '{a.class_value}'.")

    return sbgn


if __name__ == "__main__":
    sbgn_dir = Path(__file__).parent / "sbgn"
    for fname in [
        "test-output-01.sbgn",
        "test-output-02.sbgn",
        "test-output-03.sbgn",
        "adh.sbgn",
        "adh_0.3.sbgn",
    ]:
        console.rule(fname)
        sbgn = read_sbgn_01(sbgn_dir / fname)
