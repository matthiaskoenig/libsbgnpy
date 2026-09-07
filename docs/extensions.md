# Notes and extensions

Every SBGN element inherits from `Sbgnbase` and therefore carries two containers for content the schema does not describe itself:

- **`notes`** — a human readable description of the element, as XHTML, see the [SBGN-ML notes](https://github.com/sbgn/sbgn/wiki/SBGN-ML_Notes),
- **`extension`** — machine readable content, as arbitrary XML, see the [SBGN-ML extensions](https://github.com/sbgn/sbgn/wiki/SBGN-ML_Extensions).

Both hold XML which the bindings do not interpret. It is **set as a string** and **read back as an element tree**, so the two directions are not symmetric.

## Writing

The content is set as a string, one entry per element:

```python
from libsbgnpy import (
    Bbox,
    Glyph,
    GlyphClass,
    Label,
    Map,
    MapLanguage,
    Sbgn,
    Sbgnbase,
)

glyph = Glyph(
    id="g1",
    class_value=GlyphClass.MACROMOLECULE,
    label=Label(text="INSR"),
    bbox=Bbox(x=100, y=100, w=80, h=40),
    notes=Sbgnbase.Notes(
        w3_org_1999_xhtml_element=[
            '<body xmlns="http://www.w3.org/1999/xhtml">The insulin receptor.</body>',
        ]
    ),
)
```

An extension is set the same way, on any element:

```python
map = Map(id="m", language=MapLanguage.PROCESS_DESCRIPTION)
map.extension = Sbgnbase.Extension(
    any_element=[
        '<annotation xmlns="http://www.sbml.org/2001/ns/libsbml/annotation">'
        "..."
        "</annotation>",
    ]
)
```

The strings are parsed and written as markup when the document is serialized, so the result is well formed XML and more than one entry can be stored. The document which is passed in is not modified.

!!! warning "The XML has to be well formed"

    A string which is not well formed XML raises an `lxml.etree.XMLSyntaxError` when the document is written. Every entry is a single element, with its namespace declared on it.

## Reading

Reading a document turns each entry into an `AnyElement` tree, since the bindings do not know the schema of the content. `element_to_string` serializes such an entry back to XML:

```python
from pathlib import Path

from libsbgnpy import element_to_string, read_sbgn_from_file

sbgn = read_sbgn_from_file(Path("map.sbgn"))

for glyph in sbgn.map[0].glyph:
    if glyph.notes is None:
        continue
    for element in glyph.notes.w3_org_1999_xhtml_element:
        print(element_to_string(element))
        # <html:body xmlns:html="http://www.w3.org/1999/xhtml">The insulin receptor.</html:body>
```

The counterpart is `element_from_string`, which parses XML into such an entry. It is applied automatically when a document is written, so it is only needed to work with the entries directly.

Render information stored in an extension is read back with `read_render_from_extension`, see [Render information](render.md).

## Examples

| example | what it shows |
| --- | --- |
| [`notes.py`](https://github.com/matthiaskoenig/libsbgnpy/blob/develop/examples/notes.py) | write and read notes |
| [`extension.py`](https://github.com/matthiaskoenig/libsbgnpy/blob/develop/examples/extension.py) | write and read extensions |
