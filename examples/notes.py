"""Write and read notes.

Notes are XHTML elements stored in the `notes` of any SBGN element, see
<https://github.com/sbgn/sbgn/wiki/SBGN-ML_Notes>.

```bash
python examples/notes.py
```
"""

from pathlib import Path

from libsbgnpy import (
    Bbox,
    Glyph,
    GlyphClass,
    Label,
    Map,
    MapLanguage,
    Sbgn,
    Sbgnbase,
    element_to_string,
    read_sbgn_from_file,
    write_sbgn_to_file,
)
from libsbgnpy.console import console


def write_notes(f: Path) -> Sbgn:
    """Write a map with two notes on a glyph.

    Args:
        f: path of the SBGN file to write

    Returns:
        The SBGN document.
    """
    map = Map(id="notes", language=MapLanguage.PROCESS_DESCRIPTION)
    sbgn = Sbgn(map=[map])

    glyph = Glyph(
        id="g1",
        class_value=GlyphClass.MACROMOLECULE,
        label=Label(text="INSR"),
        bbox=Bbox(x=100, y=100, w=80, h=40),
        notes=Sbgnbase.Notes(
            w3_org_1999_xhtml_element=[
                '<body xmlns="http://www.w3.org/1999/xhtml">'
                "This is an example note describing the INSR glyph."
                "</body>",
                '<body xmlns="http://www.w3.org/1999/xhtml">'
                "A second note with more information."
                "</body>",
            ]
        ),
    )
    map.glyph.append(glyph)

    write_sbgn_to_file(sbgn, f)
    return sbgn


def read_notes(f: Path) -> None:
    """Read the notes of every glyph of a map.

    The notes are read back as XML elements, `element_to_string` serializes
    them again.

    Args:
        f: path of the SBGN file
    """
    sbgn = read_sbgn_from_file(f)
    for glyph in sbgn.map[0].glyph:
        if glyph.notes is None:
            continue
        console.rule(glyph.id, align="left", style="white")
        for element in glyph.notes.w3_org_1999_xhtml_element:
            console.print(element_to_string(element))


if __name__ == "__main__":
    f_sbgn = Path("notes.sbgn")
    write_notes(f_sbgn)
    read_notes(f_sbgn)
