"""Test notes on SBGN elements."""

from pathlib import Path

from libsbgnpy import (
    Bbox,
    Glyph,
    GlyphClass,
    Map,
    MapLanguage,
    Sbgn,
    Sbgnbase,
    element_to_string,
    read_sbgn_from_file,
    write_sbgn_to_file,
)

NOTE = (
    '<body xmlns="http://www.w3.org/1999/xhtml">'
    "This is an example note describing the INSR glyph."
    "</body>"
)


def _sbgn_with_notes() -> Sbgn:
    """Create a map with a glyph carrying a note."""
    map = Map(id="notes", language=MapLanguage.PROCESS_DESCRIPTION)
    sbgn = Sbgn(map=[map])
    map.glyph.append(
        Glyph(
            id="g1",
            class_value=GlyphClass.SIMPLE_CHEMICAL,
            bbox=Bbox(x=0, y=0, w=100, h=50),
            notes=Sbgnbase.Notes(w3_org_1999_xhtml_element=[NOTE]),
        )
    )
    return sbgn


def test_create_notes() -> None:
    """Notes are set on a glyph."""
    glyph = _sbgn_with_notes().map[0].glyph[0]

    assert glyph.notes is not None
    assert glyph.notes.w3_org_1999_xhtml_element == [NOTE]


def test_notes_roundtrip(tmp_path: Path) -> None:
    """Notes survive writing and reading."""
    f_sbgn = tmp_path / "test.sbgn"
    write_sbgn_to_file(_sbgn_with_notes(), f_sbgn)

    notes = read_sbgn_from_file(f_sbgn).map[0].glyph[0].notes
    assert notes is not None

    xml_str = element_to_string(notes.w3_org_1999_xhtml_element[0])
    assert "body" in xml_str
    assert "This is an example note describing the INSR glyph." in xml_str


def test_element_to_string_of_string() -> None:
    """A note which was not read back is returned unchanged."""
    assert element_to_string(NOTE) == NOTE
