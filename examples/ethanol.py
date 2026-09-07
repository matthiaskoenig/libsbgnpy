"""Build the ethanol map step by step and render it as an image.

The example creates a process description of the alcohol dehydrogenase
reaction: first the glyphs, then the arcs, and finally the render information
which colours the map. Every step is written and rendered, so the three images
show how the map grows.

Rendering requires an internet connection, see `libsbgnpy.image`.

```bash
python examples/ethanol.py
```
"""

from pathlib import Path

from libsbgnpy import (
    Arc,
    ArcClass,
    Bbox,
    ColorDefinition,
    G,
    Glyph,
    GlyphClass,
    GlyphOrientation,
    Label,
    ListOfColorDefinitions,
    ListOfGradientDefinitions,
    ListOfStyles,
    Map,
    MapLanguage,
    Port,
    RenderInformation,
    Sbgn,
    Sbgnbase,
    Style,
    log,
    render_sbgn,
    write_render_to_string,
    write_sbgn_to_file,
)


def ethanol(prefix: str) -> Sbgn:
    """Create the ethanol map and render it after every step.

    Writes `<prefix>_glyphs`, `<prefix>_arcs` and `<prefix>_render` as SBGN and
    as PNG.

    Args:
        prefix: prefix of the files to write

    Returns:
        The SBGN document.
    """
    map = Map(
        id="ethanol",
        language=MapLanguage.PROCESS_DESCRIPTION,
        bbox=Bbox(x=0, y=0, w=363, h=253),
    )
    sbgn = Sbgn(map=[map])

    # 1. the entities and the process
    map.glyph.extend(
        [
            Glyph(
                id="ethanol",
                class_value=GlyphClass.SIMPLE_CHEMICAL,
                label=Label(text="Ethanol"),
                bbox=Bbox(x=40, y=120, w=60, h=60),
            ),
            Glyph(
                id="ethanal",
                class_value=GlyphClass.SIMPLE_CHEMICAL,
                label=Label(text="Ethanal"),
                bbox=Bbox(x=220, y=110, w=60, h=60),
            ),
            Glyph(
                id="adh1",
                class_value=GlyphClass.MACROMOLECULE,
                label=Label(text="ADH1"),
                bbox=Bbox(x=106, y=20, w=108, h=60),
            ),
            Glyph(
                id="h",
                class_value=GlyphClass.SIMPLE_CHEMICAL,
                label=Label(text="H+"),
                bbox=Bbox(x=220, y=190, w=60, h=60),
                clone=Glyph.Clone(),
            ),
            Glyph(
                id="nad",
                class_value=GlyphClass.SIMPLE_CHEMICAL,
                label=Label(text="NAD+"),
                bbox=Bbox(x=40, y=190, w=60, h=60),
                clone=Glyph.Clone(),
            ),
            Glyph(
                id="nadh",
                class_value=GlyphClass.SIMPLE_CHEMICAL,
                label=Label(text="NADH"),
                bbox=Bbox(x=300, y=150, w=60, h=60),
                clone=Glyph.Clone(),
            ),
            Glyph(
                id="pn1",
                class_value=GlyphClass.PROCESS,
                orientation=GlyphOrientation.HORIZONTAL,
                bbox=Bbox(x=148, y=168, w=24, h=24),
                port=[
                    Port(id="pn1.1", x=136, y=180),
                    Port(id="pn1.2", x=184, y=180),
                ],
            ),
        ]
    )
    write_sbgn_to_file(sbgn, Path(f"{prefix}_glyphs.sbgn"))
    render_sbgn(sbgn, Path(f"{prefix}_glyphs.png"))

    # 2. the arcs, attached to the ports of the process
    map.arc.extend(
        [
            Arc(
                id="a01",
                class_value=ArcClass.CONSUMPTION,
                source="ethanol",
                target="pn1.1",
                start=Arc.Start(x=98, y=160),
                end=Arc.End(x=136, y=180),
            ),
            Arc(
                id="a02",
                class_value=ArcClass.PRODUCTION,
                source="pn1.2",
                target="nadh",
                start=Arc.Start(x=184, y=180),
                end=Arc.End(x=300, y=180),
            ),
            Arc(
                id="a03",
                class_value=ArcClass.CATALYSIS,
                source="adh1",
                target="pn1",
                start=Arc.Start(x=160, y=80),
                end=Arc.End(x=160, y=168),
            ),
            Arc(
                id="a04",
                class_value=ArcClass.PRODUCTION,
                source="pn1.2",
                target="h",
                start=Arc.Start(x=184, y=180),
                end=Arc.End(x=224, y=202),
            ),
            Arc(
                id="a05",
                class_value=ArcClass.PRODUCTION,
                source="pn1.2",
                target="ethanal",
                start=Arc.Start(x=184, y=180),
                end=Arc.End(x=224, y=154),
            ),
            Arc(
                id="a06",
                class_value=ArcClass.CONSUMPTION,
                source="nad",
                target="pn1.1",
                start=Arc.Start(x=95, y=202),
                end=Arc.End(x=136, y=180),
            ),
        ]
    )
    write_sbgn_to_file(sbgn, Path(f"{prefix}_arcs.sbgn"))
    render_sbgn(sbgn, Path(f"{prefix}_arcs.png"))

    # 3. the colors, stored as render information in the extension of the map
    render_info = RenderInformation(
        id="ethanol_render_info",
        program_name="libsbgnpy",
        program_version="0.6.0",
        list_of_color_definitions=ListOfColorDefinitions(
            color_definition=[
                ColorDefinition(id="blue", value="#1f77b4bb"),
                ColorDefinition(id="orange", value="#ff7f0ebb"),
                ColorDefinition(id="black", value="#000000"),
                ColorDefinition(id="grey", value="#cccccccc"),
            ]
        ),
        list_of_gradient_definitions=ListOfGradientDefinitions(),
        list_of_styles=ListOfStyles(
            style=[
                Style(
                    id_list="ethanol ethanal",
                    g=G(stroke="black", stroke_width=2, fill="blue"),
                ),
                Style(
                    id_list="adh1",
                    g=G(stroke="black", stroke_width=2, fill="orange"),
                ),
                Style(
                    id_list="nad nadh h",
                    g=G(stroke="black", stroke_width=1, fill="grey"),
                ),
            ]
        ),
    )
    map.extension = Sbgnbase.Extension(
        any_element=[write_render_to_string(render_info)]
    )
    write_sbgn_to_file(sbgn, Path(f"{prefix}_render.sbgn"))
    render_sbgn(sbgn, Path(f"{prefix}_render.png"))

    return sbgn


if __name__ == "__main__":
    log.enable_rich_logging()
    ethanol(prefix="ethanol")
