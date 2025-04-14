"""Example how to handle special characters in labels.

See discussion and documentation in https://github.com/matthiaskoenig/libsbgnpy/issues/38
"""

from libsbgnpy import *


def special_character_example() -> str:
    """Example demonstrating how to encode special characters in SBGN files."""

    map = Map(
        language=MapLanguage.PROCESS_DESCRIPTION,
        bbox=Bbox(x=0, y=0, w=600, h=200),
    )
    sbgn = Sbgn(map=[map])

    # create some glyphs
    map.glyph = [
        # simple glyph
        Glyph(
            class_value=GlyphClass.MACROMOLECULE,
            id="glyph1",
            label=Label(text="α/β hydrolase"),
            bbox=Bbox(x=5, y=70, w=160, h=60),
        ),
        Glyph(
            class_value=GlyphClass.MACROMOLECULE,
            id="glyph2",
            label=Label(text="5′-3′; exoribonuclease"),
            bbox=Bbox(x=435, y=70, w=160, h=60),
        ),
        Glyph(
            class_value=GlyphClass.PROCESS,
            id="glyph3",
            bbox=Bbox(x=300, y=90, w=20, h=20),
            port=[
                Port(id="glyph3.1", x=285, y=100),
                Port(id="glyph3.2", x=315, y=100),
            ],
        ),
    ]
    map.arc = [
        Arc(
            id="arc1",
            class_value=ArcClass.CONSUMPTION,
            source="glyph1",
            target="glyph3.1",
            start=Arc.Start(x=165, y=100),
            end=Arc.End(x=285, y=100),
        ),
        Arc(
            id="arc2",
            class_value=ArcClass.PRODUCTION,
            source="glyph3.2",
            target="glyph2",
            start=Arc.Start(x=315, y=100),
            end=Arc.End(x=435, y=100),
        ),
    ]

    xml_str = write_sbgn_to_string(sbgn=sbgn)
    return xml_str


if __name__ == "__main__":
    xml_str = special_character_example()
    console.print(xml_str)
