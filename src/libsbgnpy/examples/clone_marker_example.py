from libsbgnpy import *


def clone_marker_example() -> Sbgn:
    """Clone marker example."""
    # create new map
    map = Map(
        language=MapLanguage.PROCESS_DESCRIPTION,
        bbox=Bbox(x=0, y=0, w=363, h=253),
    )
    # add map to new sbgn
    sbgn = Sbgn(map=[map])

    # create glyphs and add to map
    map.glyph.extend(
        [
            Glyph(
                class_value=GlyphClass.SIMPLE_CHEMICAL,
                id="glyph1",
                label=Label(text="Ethanol"),
                bbox=Bbox(x=40, y=120, w=60, h=60),
            ),
            Glyph(
                class_value=GlyphClass.SIMPLE_CHEMICAL,
                id="glyph_ethanal",
                label=Label(text="Ethanal"),
                bbox=Bbox(x=220, y=110, w=60, h=60),
            ),
            Glyph(
                class_value=GlyphClass.MACROMOLECULE,
                id="glyph_adh1",
                label=Label(text="ADH1"),
                bbox=Bbox(x=106, y=20, w=108, h=60),
            ),
            Glyph(
                class_value=GlyphClass.SIMPLE_CHEMICAL,
                id="glyph_h",
                label=Label(text="H+"),
                bbox=Bbox(x=220, y=190, w=60, h=60),
                clone=Glyph.Clone(),  # clone marker
            ),
            Glyph(
                class_value=GlyphClass.SIMPLE_CHEMICAL,
                id="glyph_nad",
                label=Label(text="NAD+"),
                bbox=Bbox(x=40, y=190, w=60, h=60),
                clone=Glyph.Clone(),  # clone marker
            ),
            Glyph(
                class_value=GlyphClass.SIMPLE_CHEMICAL,
                id="glyph_nadh",
                label=Label(text="NADH"),
                bbox=Bbox(x=300, y=150, w=60, h=60),
                clone=Glyph.Clone(),  # clone marker
            ),
            # glyph with ports (process)
            Glyph(
                class_value=GlyphClass.PROCESS,
                id="pn1",
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
                class_value=ArcClass.CONSUMPTION,
                source="glyph1",
                target="pn1.1",
                id="a01",
                start=Arc.Start(x=98, y=160),
                end=Arc.End(x=136, y=180),
            ),
            Arc(
                class_value=ArcClass.PRODUCTION,
                source="pn1.2",
                target="glyph_nadh",
                id="a02",
                start=Arc.Start(x=184, y=180),
                end=Arc.End(x=300, y=180),
            ),
            Arc(
                class_value=ArcClass.CATALYSIS,
                source="glyph_adh1",
                target="pn1",
                id="a03",
                start=Arc.Start(x=160, y=80),
                end=Arc.End(x=160, y=168),
            ),
            Arc(
                class_value=ArcClass.PRODUCTION,
                source="pn1.2",
                target="glyph_h",
                id="a04",
                start=Arc.Start(x=184, y=180),
                end=Arc.End(x=224, y=202),
            ),
            Arc(
                class_value=ArcClass.PRODUCTION,
                source="pn1.2",
                target="glyph_ethanal",
                id="a05",
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
    return sbgn


if __name__ == "__main__":
    sbgn = clone_marker_example()
    console.print(sbgn)
