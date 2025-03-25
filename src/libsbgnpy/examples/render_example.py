"""
Example on writing and reading Render information.
"""

from pathlib import Path

from libsbgnpy import *


def write_map_render(f: Path) -> None:
    """Example for writing render information on a map."""
    map = Map(language=MapLanguage.PROCESS_DESCRIPTION)
    sbgn = Sbgn(map=[map])

    # create glyph
    map.glyph = [
        Glyph(
            id="glyph1",
            class_value=GlyphClass.MACROMOLECULE,
            label=Label(text="INSR"),
            bbox=Bbox(x=100, y=100, w=80, h=40),
        ),
        Glyph(
            id="glyph2",
            class_value=GlyphClass.SIMPLE_CHEMICAL,
            label=Label(text="ATP"),
            bbox=Bbox(x=200, y=100, w=80, h=40),
        ),
        Glyph(
            id="glyph3",
            class_value=GlyphClass.SIMPLE_CHEMICAL,
            label=Label(text="glucose"),
            bbox=Bbox(x=300, y=100, w=80, h=40),
        ),
    ]

    """
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

    render_info = RenderInformation(
        id="example",
        program_name="libsbgnpy",
        program_version="1.0.0",
        list_of_color_definitions=ListOfColorDefinitions(
            color_definition=[
                ColorDefinition(id="color0", value="#969696"),
                ColorDefinition(id="color1", value="#ff9900"),
            ]
        ),
        list_of_gradient_definitions=ListOfGradientDefinitions(
            linear_gradient=[
                LinearGradient(
                    id="gradient0",
                    x1="0%",
                    y1="0%",
                    x2="100%",
                    y2="0%",
                    stop=[
                        LinearGradient.Stop(offset="0%", stop_color="#ccffff"),
                        LinearGradient.Stop(offset="100%", stop_color="#ffffff"),
                    ],
                )
            ]
        ),
        list_of_styles=ListOfStyles(
            [
                Style(
                    id_list="glyph1 glyph2",
                    g=G(stroke="color0", stroke_width=5, fill="color1"),
                ),
                Style(
                    id_list="glyph3",
                    g=G(stroke="color1", stroke_width=2, fill="gradient0"),
                ),
            ]
        ),
    )
    # console.print(render_info)

    # set extension
    xml_str = write_render_to_string(render_info=render_info)
    console.print(xml_str)
    map.extension = Sbgn.Extension([xml_str])

    # console.print(write_sbgn_to_string(sbgn))
    write_sbgn_to_file(sbgn=sbgn, f=f)


def read_map_render(f: Path) -> None:
    """Read notes from glyphs example."""
    sbgn = read_sbgn_from_file(f=f)
    map: Map = sbgn.map[0]
    xml_str = str(map.extension.any_element[0])
    render_info = read_render_from_string(xml_str=xml_str)
    console.print(render_info)


if __name__ == "__main__":
    from libsbgnpy import sbgn_examples_dir

    f: Path = sbgn_examples_dir / "render.sbgn"
    write_map_render(f=f)
    console.rule(style="white")
    read_map_render(f=f)
