# SBGN maps

The classes of `libsbgnpy.sbgn` are the python bindings of the SBGN-ML schema, generated with [xsdata](https://github.com/tefra/xsdata). They mirror the schema, so the [SBGN specifications](https://github.com/sbgn/sbgn/wiki/SBGN_Specifications) are the reference for what an element means; this page describes how the classes are used.

## The document

An SBGN-ML document is an `Sbgn` object holding one or more `Map` objects. A map declares its language, an optional bounding box, and holds the glyphs and arcs it is drawn from:

```python
from libsbgnpy import Bbox, Map, MapLanguage, Sbgn

map = Map(
    id="ethanol",
    language=MapLanguage.PROCESS_DESCRIPTION,
    bbox=Bbox(x=0, y=0, w=363, h=253),
)
sbgn = Sbgn(map=[map])
```

`MapLanguage` is the language of the map, i.e., which vocabulary of glyphs and arcs applies:

| language | what it describes |
| --- | --- |
| `MapLanguage.PROCESS_DESCRIPTION` | what is converted into what |
| `MapLanguage.ENTITY_RELATIONSHIP` | which entity influences which other entity |
| `MapLanguage.ACTIVITY_FLOW` | the flow of activity between the entities |

All classes are keyword only, i.e., `Map(id="ethanol")` works and `Map("ethanol")` does not. Every list attribute (`map`, `glyph`, `arc`, `port`) defaults to an empty list, so it can be extended after the object was created.

## Glyphs

A `Glyph` is a node of the map. It carries its class, an id which the arcs refer to, an optional `Label` and the `Bbox` it is drawn in:

```python
from libsbgnpy import Bbox, Glyph, GlyphClass, Label

map.glyph.append(
    Glyph(
        id="ethanol",
        class_value=GlyphClass.SIMPLE_CHEMICAL,
        label=Label(text="Ethanol"),
        bbox=Bbox(x=40, y=120, w=60, h=60),
    )
)
```

The class of a glyph is the shape it is drawn as, `GlyphClass` has all classes of the three languages, e.g., `SIMPLE_CHEMICAL`, `MACROMOLECULE`, `COMPLEX`, `PROCESS`, `COMPARTMENT`, `BIOLOGICAL_ACTIVITY` or `PHENOTYPE`. The attribute is called `class_value`, since `class` is a python keyword.

!!! note "Coordinates"

    A bounding box is given in the coordinate system of the map: `x` and `y` are the top left corner, `w` and `h` the width and the height. There is no unit, the numbers are pixels of the drawing, and `y` grows downwards.

Glyphs are nested: a compartment or a complex holds the glyphs inside it in its own `glyph` list, and the auxiliary units of an entity, e.g., a state variable or a unit of information, are glyphs as well:

```python
complex = Glyph(
    id="complex1",
    class_value=GlyphClass.COMPLEX,
    bbox=Bbox(x=20, y=20, w=200, h=120),
)
complex.glyph.append(
    Glyph(
        id="subunit1",
        class_value=GlyphClass.MACROMOLECULE,
        label=Label(text="ADH1"),
        bbox=Bbox(x=40, y=40, w=80, h=40),
    )
)
```

A `Glyph.Clone` marks an entity which is drawn more than once in the same map, so that a reader knows the two circles are the same molecule:

```python
Glyph(
    id="nad",
    class_value=GlyphClass.SIMPLE_CHEMICAL,
    label=Label(text="NAD+"),
    bbox=Bbox(x=40, y=190, w=60, h=60),
    clone=Glyph.Clone(),
)
```

## Ports and arcs

An `Arc` connects a source with a target, both given as the id of a glyph or of a port. Its class states what the connection means, and `Arc.Start` and `Arc.End` are the points it is drawn between:

```python
from libsbgnpy import Arc, ArcClass

map.arc.append(
    Arc(
        id="a01",
        class_value=ArcClass.CONSUMPTION,
        source="ethanol",
        target="pn1.1",
        start=Arc.Start(x=98, y=160),
        end=Arc.End(x=136, y=180),
    )
)
```

A process glyph is not connected directly: it carries `Port` objects, one for each side, and the arcs attach to those. This is what makes the direction of a reaction unambiguous:

```python
from libsbgnpy import GlyphOrientation, Port

Glyph(
    id="pn1",
    class_value=GlyphClass.PROCESS,
    orientation=GlyphOrientation.HORIZONTAL,
    bbox=Bbox(x=148, y=168, w=24, h=24),
    port=[
        Port(id="pn1.1", x=136, y=180),
        Port(id="pn1.2", x=184, y=180),
    ],
)
```

`ArcClass` covers the arcs of the three languages, e.g., `CONSUMPTION` and `PRODUCTION` for the substrates and products of a process, `CATALYSIS`, `INHIBITION`, `STIMULATION` and `MODULATION` for the influences on it, and `LOGIC_ARC` for the input of a logical operator.

## Labels

A `Label` is the text drawn on a glyph. The text is unicode, so greek letters, primes and the characters which have to be escaped in XML are written as they are:

```python
Glyph(
    id="glyph1",
    class_value=GlyphClass.MACROMOLECULE,
    label=Label(text="α/β hydrolase"),
    bbox=Bbox(x=5, y=70, w=160, h=60),
)
```

The serializer escapes what has to be escaped, see [Reading and writing](io.md), and the round trip returns the text unchanged. Line breaks in a label are allowed, they are drawn as line breaks.

## Notes and extensions

Every element of a map, from the document down to a single port, inherits from `Sbgnbase` and can therefore carry `notes` with a human readable description and an `extension` with additional machine readable content, see [Notes and extensions](extensions.md).

## Examples

The runnable examples are in [`examples/`](https://github.com/matthiaskoenig/libsbgnpy/tree/develop/examples):

| example | what it shows |
| --- | --- |
| [`write.py`](https://github.com/matthiaskoenig/libsbgnpy/blob/develop/examples/write.py) | create SBGN documents from scratch |
| [`clone_marker.py`](https://github.com/matthiaskoenig/libsbgnpy/blob/develop/examples/clone_marker.py) | mark glyphs which occur more than once |
| [`labels.py`](https://github.com/matthiaskoenig/libsbgnpy/blob/develop/examples/labels.py) | special characters in labels |
