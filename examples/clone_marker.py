"""Mark glyphs which occur more than once with a clone marker.

A clone marker states that the entity is drawn several times in the same map,
see the SBGN process description specification.

```bash
python examples/clone_marker.py
```
"""

from pathlib import Path

from libsbgnpy import (
    Arc,
    ArcClass,
    Bbox,
    Glyph,
    GlyphClass,
    GlyphOrientation,
    Label,
    Map,
    MapLanguage,
    Port,
    Sbgn,
    write_sbgn_to_file,
)
from libsbgnpy.console import console


def clone_marker(f: Path) -> Sbgn:
    """Create the alcohol dehydrogenase reaction with cloned cofactors.

    `NAD+`, `NADH` and `H+` occur in many reactions of a map and are therefore
    marked as clones.

    Args:
        f: path of the SBGN file to write

    Returns:
        The SBGN document.
    """
    map = Map(
        id="clone_marker",
        language=MapLanguage.PROCESS_DESCRIPTION,
        bbox=Bbox(x=0, y=0, w=363, h=253),
    )
    sbgn = Sbgn(map=[map])

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

    write_sbgn_to_file(sbgn, f)
    console.print(f"clone markers: {[g.id for g in map.glyph if g.clone]}")
    return sbgn


if __name__ == "__main__":
    clone_marker(Path("clone_marker.sbgn"))
