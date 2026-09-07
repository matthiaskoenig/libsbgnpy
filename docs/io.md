# Reading and writing

SBGN-ML documents are read and written with the functions of `libsbgnpy.io`, which use [xsdata](https://github.com/tefra/xsdata) to map the XML onto the classes of [`libsbgnpy.sbgn`](maps.md).

## Reading

`read_sbgn_from_file` reads a document from a path, `read_sbgn_from_string` from a string:

```python
from pathlib import Path

from libsbgnpy import read_sbgn_from_file

sbgn = read_sbgn_from_file(Path("examples/sbgn/adh.sbgn"))
map = sbgn.map[0]

for glyph in map.glyph:
    print(glyph.id, glyph.class_value)
for arc in map.arc:
    print(arc.id, arc.class_value, arc.source, "->", arc.target)
```

Reading does not validate the document against the schema, it only parses it. To check that a document follows the schema see [Validation](validation.md).

A file which is no well formed XML raises an `xsdata.exceptions.ParserError`, and the path of the file is logged:

```python
from xsdata.exceptions import ParserError

try:
    sbgn = read_sbgn_from_file(Path("broken.sbgn"))
except ParserError as err:
    print(f"not an SBGN document: {err}")
```

### Older SBGN-ML versions

The bindings are generated from the SBGN-ML 0.3 schema. Documents in the earlier namespaces `http://sbgn.org/libsbgn/0.1` and `http://sbgn.org/libsbgn/0.2` are upconverted while reading, i.e., they are read like a 0.3 document and written back as one. The conversion is `upconvert`, which is applied by the reader and by the validator:

```python
from libsbgnpy.io import upconvert

upconvert('<sbgn xmlns="http://sbgn.org/libsbgn/0.2"/>')
# '<sbgn xmlns="http://sbgn.org/libsbgn/0.3"/>'
```

## Writing

`write_sbgn_to_file` writes a document to a path, `write_sbgn_to_string` returns it as a string:

```python
from pathlib import Path

from libsbgnpy import write_sbgn_to_file, write_sbgn_to_string

write_sbgn_to_file(sbgn, Path("map.sbgn"))
xml_str = write_sbgn_to_string(sbgn)
```

The document is written in the SBGN-ML 0.3 namespace, indented with two spaces, with an XML declaration and in UTF-8. Characters which have to be escaped in XML are escaped, so a label like `a < b` survives the round trip:

```python
from libsbgnpy import read_sbgn_from_string, write_sbgn_to_string

sbgn2 = read_sbgn_from_string(write_sbgn_to_string(sbgn))
```

The raw XML of the `notes` and `extension` elements is written as markup rather than as escaped text, see [Notes and extensions](extensions.md).

## Examples

| example | what it shows |
| --- | --- |
| [`read.py`](https://github.com/matthiaskoenig/libsbgnpy/blob/develop/examples/read.py) | read a document and display its content |
| [`write.py`](https://github.com/matthiaskoenig/libsbgnpy/blob/develop/examples/write.py) | create documents from scratch and write them |
