"""
Example on writing and reading Notes information.
Notes must be XML elements in a <notes>Tag</notes>
"""

from pathlib import Path

from libsbgnpy import *


def write_glyph_notes(f: Path) -> None:
    """Example for writing Notes on a glyph."""
    map = Map(language=MapLanguage.PROCESS_DESCRIPTION)
    sbgn = Sbgn(map=[map])

    # create glyph
    g = Glyph(
        id="g1",
        class_value=GlyphClass.MACROMOLECULE,
        label=Label(text="INSR"),
        bbox=Bbox(x=100, y=100, w=80, h=40),
    )
    map.glyph.append(g)

    # set notes
    g.notes = Sbgnbase.Notes(
        w3_org_1999_xhtml_element=[
            """<body xmlns="http://www.w3.org/1999/xhtml">
    This is an example note describing the INSR glyph.
</body>""",
            """<body xmlns="http://www.w3.org/1999/xhtml">
    A second note with more information
</body>""",
        ]
    )

    print(write_sbgn_to_string(sbgn))
    write_sbgn_to_file(sbgn=sbgn, f=f)


def read_glyph_notes(f: Path):
    """Read notes from glyphs example."""
    sbgn = read_sbgn_from_file(f=f)
    map: Map = sbgn.map[0]
    for g in map.glyph:
        notes = g.notes
        if notes:
            console.print(g.id)
            console.print(notes)


if __name__ == "__main__":
    from libsbgnpy import sbgn_examples_dir

    f: Path = sbgn_examples_dir / "notes_new.sbgn"
    write_glyph_notes(f=f)
    console.rule(style="white")
    read_glyph_notes(f)
