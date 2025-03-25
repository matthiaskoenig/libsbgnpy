"""Test SBGN Notes."""

from pathlib import Path

from libsbgnpy import *
from libsbgnpy.examples import notes_example


def test_create_notes() -> None:
    g = Glyph(id="g1")
    notes = Sbgnbase.Notes(
        """
       <body xmlns="http://www.w3.org/1999/xhtml">
           This is an example note describing the INSR glyph.
       </body>"""
    )
    g.notes = notes
    assert g.notes is not None

    notes_str = str(g.notes)
    assert "<body" in notes_str


def test_read_notes(tmpdir: Path) -> None:
    map = Map(language=MapLanguage.PROCESS_DESCRIPTION)
    sbgn = Sbgn(map=[map])

    text = """
           <body xmlns="http://www.w3.org/1999/xhtml">
               This is an example note describing the map.
           </body>
           """
    map.notes = Sbgnbase.Notes(text)
    assert map.notes is not None

    f_sbgn = tmpdir / "test.sbgn"
    write_sbgn_to_file(sbgn, f_sbgn)
    del map, sbgn

    sbgn2 = read_sbgn_from_file(f_sbgn)
    _ = write_sbgn_to_string(sbgn2)

    map2 = sbgn2.map[0]
    notes2 = map2.notes
    assert notes2 is not None
    assert "<body" in str(notes2)


def test_notes_example(tmpdir: Path) -> None:
    f_sbgn = tmpdir / "test.sbgn"
    notes_example.write_glyph_notes(f_sbgn)
    notes_example.read_glyph_notes(f_sbgn)
