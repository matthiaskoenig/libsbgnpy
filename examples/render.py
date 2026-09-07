"""Write and read render information.

Render information colours the glyphs and arcs of a map. It is stored as an
extension of the map, using the SBML render extension vocabulary, see
<https://github.com/sbgn/sbgn/wiki/SBGN-ML_Rendering>.

```bash
python examples/render.py
```
"""

from pathlib import Path

from libsbgnpy import (
    Bbox,
    ColorDefinition,
    G,
    Glyph,
    GlyphClass,
    Label,
    LinearGradient,
    ListOfColorDefinitions,
    ListOfGradientDefinitions,
    ListOfStyles,
    Map,
    MapLanguage,
    RenderInformation,
    Sbgn,
    Sbgnbase,
    Style,
    read_render_from_extension,
    read_sbgn_from_file,
    write_render_to_string,
    write_sbgn_to_file,
)
from libsbgnpy.console import console


def write_render(f: Path) -> Sbgn:
    """Write a map with render information in the extension.

    Args:
        f: path of the SBGN file to write

    Returns:
        The SBGN document.
    """
    map = Map(id="render", language=MapLanguage.PROCESS_DESCRIPTION)
    sbgn = Sbgn(map=[map])

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
            style=[
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

    # the render information is stored as XML in the extension of the map
    map.extension = Sbgnbase.Extension(
        any_element=[write_render_to_string(render_info)]
    )

    write_sbgn_to_file(sbgn, f)
    return sbgn


def read_render(f: Path) -> RenderInformation | None:
    """Read the render information from the extension of a map.

    Args:
        f: path of the SBGN file

    Returns:
        The render information, or `None` if the map carries none.
    """
    sbgn = read_sbgn_from_file(f)
    render_info = read_render_from_extension(sbgn.map[0].extension)
    console.print(render_info)
    return render_info


if __name__ == "__main__":
    f_sbgn = Path("render.sbgn")
    write_render(f_sbgn)
    read_render(f_sbgn)
