"""Use special characters in labels.

Labels are unicode, so greek letters and primes are written as they are; the
serializer takes care of the encoding, see
<https://github.com/matthiaskoenig/libsbgnpy/issues/38>.

```bash
python examples/labels.py
```
"""

from libsbgnpy import (
    Arc,
    ArcClass,
    Bbox,
    Glyph,
    GlyphClass,
    Label,
    Map,
    MapLanguage,
    Port,
    Sbgn,
    write_sbgn_to_string,
)
from libsbgnpy.console import console


def labels() -> str:
    """Create a map with special characters in the labels.

    Returns:
        The SBGN-ML document.
    """
    map = Map(
        id="labels",
        language=MapLanguage.PROCESS_DESCRIPTION,
        bbox=Bbox(x=0, y=0, w=600, h=200),
    )
    sbgn = Sbgn(map=[map])

    map.glyph = [
        Glyph(
            id="glyph1",
            class_value=GlyphClass.MACROMOLECULE,
            label=Label(text="α/β hydrolase"),
            bbox=Bbox(x=5, y=70, w=160, h=60),
        ),
        Glyph(
            id="glyph2",
            class_value=GlyphClass.MACROMOLECULE,
            label=Label(text="5′-3′; exoribonuclease"),
            bbox=Bbox(x=435, y=70, w=160, h=60),
        ),
        Glyph(
            id="glyph3",
            class_value=GlyphClass.PROCESS,
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

    return write_sbgn_to_string(sbgn)


if __name__ == "__main__":
    console.print(labels())
