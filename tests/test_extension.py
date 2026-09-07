"""Test extensions on SBGN elements."""

from pathlib import Path

from libsbgnpy import (
    Map,
    MapLanguage,
    Sbgn,
    Sbgnbase,
    element_to_string,
    read_render_from_extension,
    read_sbgn_from_file,
    write_sbgn_to_file,
)

RENDER_INFORMATION = """<renderInformation id="example" programName="libsbgnpy"
 programVersion="1.0.0"
 xmlns="http://www.sbml.org/sbml/level3/version1/render/version1">
  <listOfColorDefinitions>
    <colorDefinition id="color0" value="#969696"/>
    <colorDefinition id="color1" value="#ff9900"/>
  </listOfColorDefinitions>
  <listOfGradientDefinitions/>
  <listOfStyles>
    <style idList="glyph1">
      <g stroke="color0" stroke-width="5" fill="color1"/>
    </style>
  </listOfStyles>
</renderInformation>"""


def _sbgn_with_extension() -> Sbgn:
    """Create a map with render information in the extension."""
    map = Map(id="extension", language=MapLanguage.PROCESS_DESCRIPTION)
    map.extension = Sbgnbase.Extension(any_element=[RENDER_INFORMATION])
    return Sbgn(map=[map])


def test_create_extension() -> None:
    """The extension is set on a map."""
    extension = _sbgn_with_extension().map[0].extension

    assert extension is not None
    assert "renderInformation" in element_to_string(extension.any_element[0])


def test_extension_roundtrip(tmp_path: Path) -> None:
    """The extension survives writing and reading."""
    f_sbgn = tmp_path / "test.sbgn"
    write_sbgn_to_file(_sbgn_with_extension(), f_sbgn)

    extension = read_sbgn_from_file(f_sbgn).map[0].extension
    assert extension is not None

    xml_str = element_to_string(extension.any_element[0])
    assert "renderInformation" in xml_str
    assert "colorDefinition" in xml_str


def test_read_render_from_extension(tmp_path: Path) -> None:
    """The render information is read back from the extension."""
    f_sbgn = tmp_path / "test.sbgn"
    write_sbgn_to_file(_sbgn_with_extension(), f_sbgn)

    render_info = read_render_from_extension(
        read_sbgn_from_file(f_sbgn).map[0].extension
    )
    assert render_info is not None
    assert render_info.id == "example"
    assert len(render_info.list_of_color_definitions.color_definition) == 2
    assert render_info.list_of_styles.style[0].g.stroke_width == 5


def test_read_render_from_extension_without_render() -> None:
    """A map without render information returns `None`."""
    assert read_render_from_extension(None) is None
    assert read_render_from_extension(Sbgnbase.Extension()) is None
