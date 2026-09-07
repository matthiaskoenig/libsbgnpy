"""Test reading and writing of SBGN documents."""

from pathlib import Path

import pytest
from xsdata.exceptions import ParserError

from libsbgnpy import (
    Bbox,
    Glyph,
    GlyphClass,
    Label,
    Map,
    MapLanguage,
    Sbgn,
    read_render_from_string,
    read_sbgn_from_file,
    read_sbgn_from_string,
    write_render_to_string,
    write_sbgn_to_file,
    write_sbgn_to_string,
)
from libsbgnpy.io import SBGN_NAMESPACE, upconvert

#: the SBGN documents the examples read
EXAMPLES_SBGN_DIR = Path(__file__).parent.parent / "examples" / "sbgn"

RENDER_XML = """
<renderInformation id="example" programName="libsbgnpy" programVersion="1.0.0"
 xmlns="http://www.sbml.org/sbml/level3/version1/render/version1">
    <listOfColorDefinitions>
        <colorDefinition id="color0" value="#969696" />
        <colorDefinition id="color1" value="#ff9900" />
    </listOfColorDefinitions>
    <listOfGradientDefinitions>
        <linearGradient x1="0%" y1="0%" x2="100%" y2="0%" id="gradient0">
            <stop offset="0%" stop-color="#ccffff" />
            <stop offset="100%" stop-color="#ffffff" />
        </linearGradient>
    </listOfGradientDefinitions>
    <listOfStyles>
    <style idList="glyph1 glyph2">
        <g stroke="color0" stroke-width="5" fill="color1" />
    </style>
    <style idList="glyph3">
        <g stroke="color1" stroke-width="2" fill="gradient0" />
    </style>
    </listOfStyles>
</renderInformation>
"""


@pytest.fixture
def f_adh() -> Path:
    """ADH example SBGN file."""
    return EXAMPLES_SBGN_DIR / "adh.sbgn"


def test_read_sbgn_from_file(f_adh: Path) -> None:
    """Read an SBGN file."""
    sbgn = read_sbgn_from_file(f_adh)
    assert sbgn.map
    assert sbgn.map[0].language == MapLanguage.PROCESS_DESCRIPTION


def test_read_sbgn_from_string(f_adh: Path) -> None:
    """Read an SBGN document from a string."""
    sbgn = read_sbgn_from_string(f_adh.read_text(encoding="utf-8"))
    assert sbgn.map


def test_read_sbgn_from_string_invalid() -> None:
    """Reading content which is no XML raises."""
    with pytest.raises(ParserError):
        read_sbgn_from_string("this is not xml")


def test_read_sbgn_from_file_invalid(tmp_path: Path) -> None:
    """Reading a file which is no XML raises."""
    f_invalid = tmp_path / "invalid.sbgn"
    f_invalid.write_text("this is not xml", encoding="utf-8")

    with pytest.raises(ParserError):
        read_sbgn_from_file(f_invalid)


def test_write_sbgn_to_file(f_adh: Path, tmp_path: Path) -> None:
    """Write an SBGN document and read it back."""
    sbgn = read_sbgn_from_file(f_adh)
    f_out = tmp_path / "test.sbgn"
    write_sbgn_to_file(sbgn, f_out)

    assert read_sbgn_from_file(f_out).map


def test_write_sbgn_to_string(f_adh: Path) -> None:
    """Serialize an SBGN document."""
    xml_str = write_sbgn_to_string(read_sbgn_from_file(f_adh))

    assert xml_str.startswith("<?xml")
    assert SBGN_NAMESPACE in xml_str


def test_upconvert() -> None:
    """The SBGN-ML 0.1 and 0.2 namespaces are upconverted."""
    for version in ["0.1", "0.2", "0.3"]:
        assert upconvert(f'<sbgn xmlns="http://sbgn.org/libsbgn/{version}"/>') == (
            f'<sbgn xmlns="{SBGN_NAMESPACE}"/>'
        )


def test_read_sbgn_upconverts() -> None:
    """An SBGN-ML 0.2 document is read."""
    sbgn = read_sbgn_from_string(
        '<sbgn xmlns="http://sbgn.org/libsbgn/0.2">'
        '<map id="m" language="process description"/>'
        "</sbgn>"
    )
    assert sbgn.map[0].id == "m"


def test_label_escaping_roundtrip() -> None:
    """Characters which have to be escaped in a label survive the round trip."""
    map = Map(id="m", language=MapLanguage.PROCESS_DESCRIPTION)
    sbgn = Sbgn(map=[map])
    map.glyph.append(
        Glyph(
            id="g1",
            class_value=GlyphClass.MACROMOLECULE,
            label=Label(text="a < b & c > d"),
            bbox=Bbox(x=0, y=0, w=10, h=10),
        )
    )

    label = read_sbgn_from_string(write_sbgn_to_string(sbgn)).map[0].glyph[0].label
    assert label is not None
    assert label.text == "a < b & c > d"


def test_read_render_from_string() -> None:
    """Read render information."""
    render_info = read_render_from_string(RENDER_XML)

    assert render_info.id == "example"
    assert len(render_info.list_of_color_definitions.color_definition) == 2
    assert len(render_info.list_of_styles.style) == 2


def test_render_roundtrip() -> None:
    """Render information survives the round trip."""
    render_info = read_render_from_string(RENDER_XML)
    render_info2 = read_render_from_string(write_render_to_string(render_info))

    assert render_info2 == render_info
