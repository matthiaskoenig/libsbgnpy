"""Create SBGN documents from scratch and write them to files.

```bash
python examples/write.py
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
    Point,
    Port,
    Sbgn,
    write_sbgn_to_file,
)


def write_glyph(f: Path) -> Sbgn:
    """Create a map with a single macromolecule glyph.

    Args:
        f: path of the SBGN file to write

    Returns:
        The SBGN document.
    """
    map = Map(id="glyph", language=MapLanguage.PROCESS_DESCRIPTION)
    sbgn = Sbgn(map=[map])

    map.glyph.append(
        Glyph(
            id="glyph1",
            class_value=GlyphClass.MACROMOLECULE,
            label=Label(text="P53"),
            bbox=Bbox(x=125, y=60, w=100, h=40),
        )
    )

    write_sbgn_to_file(sbgn, f)
    return sbgn


def write_process(f: Path) -> Sbgn:
    """Create the alcohol dehydrogenase reaction as a process description.

    The process glyph carries the two ports the consumption and production arcs
    are attached to.

    Args:
        f: path of the SBGN file to write

    Returns:
        The SBGN document.
    """
    map = Map(
        id="process",
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
            ),
            Glyph(
                id="nad",
                class_value=GlyphClass.SIMPLE_CHEMICAL,
                label=Label(text="NAD+"),
                bbox=Bbox(x=40, y=190, w=60, h=60),
            ),
            Glyph(
                id="nadh",
                class_value=GlyphClass.SIMPLE_CHEMICAL,
                label=Label(text="NADH"),
                bbox=Bbox(x=300, y=150, w=60, h=60),
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
    return sbgn


def write_annotation(f: Path) -> Sbgn:
    """Create a map with an annotation glyph pointing at a macromolecule.

    Args:
        f: path of the SBGN file to write

    Returns:
        The SBGN document.
    """
    map = Map(id="annotation", language=MapLanguage.PROCESS_DESCRIPTION)
    sbgn = Sbgn(map=[map])

    map.glyph.extend(
        [
            Glyph(
                id="g1",
                class_value=GlyphClass.MACROMOLECULE,
                label=Label(text="LABEL"),
                bbox=Bbox(x=90, y=160, w=380, h=210),
            ),
            Glyph(
                id="g2",
                class_value=GlyphClass.ANNOTATION,
                label=Label(text="INFO"),
                bbox=Bbox(x=5, y=5, w=220, h=125),
                callout=Glyph.Callout(target="g1", point=Point(x=160, y=200)),
            ),
        ]
    )

    write_sbgn_to_file(sbgn, f)
    return sbgn


if __name__ == "__main__":
    write_glyph(Path("glyph.sbgn"))
    write_process(Path("process.sbgn"))
    write_annotation(Path("annotation.sbgn"))
