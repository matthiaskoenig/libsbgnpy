from libsbgnpy import *


def glucokinase_all() -> Sbgn:
    """Create glucokinase example."""
    map = Map(
        language=MapLanguage.PROCESS_DESCRIPTION,
        bbox=Bbox(x=0, y=0, w=363, h=253),
    )
    sbgn = Sbgn(map=[map])

    # create glyphs and add to map
    map.glyph.extend(
        [
            Glyph(
                class_value=GlyphClass.SIMPLE_CHEMICAL,
                id="glc",
                label=Label(text="Glucose"),
                bbox=Bbox(x=40, y=120, w=60, h=60),
            ),
            Glyph(
                class_value=GlyphClass.SIMPLE_CHEMICAL,
                id="glc6p",
                label=Label(text="Glucose-6P"),
                bbox=Bbox(x=220, y=110, w=60, h=60),
            ),
            Glyph(
                class_value=GlyphClass.SIMPLE_CHEMICAL,
                id="atp",
                label=Label(text="ATP"),
                bbox=Bbox(x=70, y=190, w=30, h=30),
                clone=Glyph.Clone(),
            ),
            Glyph(
                class_value=GlyphClass.SIMPLE_CHEMICAL,
                id="adp",
                label=Label(text="ADP"),
                bbox=Bbox(x=300, y=150, w=30, h=30),
                clone=Glyph.Clone(),
            ),
            Glyph(
                class_value=GlyphClass.MACROMOLECULE,
                id="gk",
                label=Label(text="GK"),
                bbox=Bbox(x=106, y=20, w=108, h=60),
            ),
            # glyph with ports (process)
            Glyph(
                class_value=GlyphClass.PROCESS,
                id="gk_process",
                orientation=GlyphOrientation.HORIZONTAL,
                bbox=Bbox(x=148, y=168, w=24, h=24),
                port=[
                    Port(x=136, y=180, id="pn1.1"),
                    Port(x=184, y=180, id="pn1.2"),
                ],
            ),
        ]
    )

    # arcs
    # create arcs and set the start and end points
    map.arc.extend(
        [
            Arc(
                id="a01",
                class_value=ArcClass.CONSUMPTION,
                source="glc",
                target="pn1.1",
                start=Arc.Start(x=98, y=160),
                end=Arc.End(x=136, y=180),
            ),
            Arc(
                id="a02",
                class_value=ArcClass.PRODUCTION,
                source="pn1.2",
                target="glc6p",
                start=Arc.Start(x=184, y=180),
                end=Arc.End(x=300, y=180),
            ),
            Arc(
                id="a03",
                class_value=ArcClass.CATALYSIS,
                source="glyph_adh1",
                target="pn1",
                start=Arc.Start(x=160, y=80),
                end=Arc.End(x=160, y=168),
            ),
            Arc(
                id="a04",
                class_value=ArcClass.PRODUCTION,
                source="pn1.2",
                target="adp",
                start=Arc.Start(x=184, y=180),
                end=Arc.End(x=224, y=154),
            ),
            Arc(
                class_value=ArcClass.CONSUMPTION,
                source="glyph_nad",
                target="pn1.1",
                id="a06",
                start=Arc.Start(x=95, y=202),
                end=Arc.End(x=136, y=180),
            ),
        ]
    )
    render_info = RenderInformation(
        id="glucokinase_render_info",
        program_name="libsbgnpy",
        program_version="0.4.0",
        list_of_color_definitions=ListOfColorDefinitions(
            color_definition=[
                ColorDefinition(id="blue", value="#1f77b4"),
                ColorDefinition(id="orange", value="#ff7f0e"),
                ColorDefinition(id="white", value="#000000"),
                ColorDefinition(id="grey", value="#cccccc"),
                ColorDefinition(id="black", value="#ffffff"),
            ]
        ),
        list_of_styles=ListOfStyles(
            [
                Style(
                    id_list="glc glc6p",
                    g=G(stroke="black", stroke_width=2, fill="blue"),
                ),
                Style(
                    id_list="gk",
                    g=G(stroke="black", stroke_width=2, fill="orange"),
                ),
                Style(
                    id_list="atp adp",
                    g=G(stroke="black", stroke_width=1, fill="grey"),
                ),
            ]
        ),
    )
    # console.print(render_info)

    # set extension
    xml_str = write_render_to_string(render_info=render_info)
    console.print(xml_str)

    map.extension = Sbgn.Extension([xml_str])

    return sbgn


if __name__ == "__main__":
    sbgn = glucokinase_all()
    console.print(write_sbgn_to_string(sbgn))
    render_sbgn(sbgn, "glucokinase_all.png")
