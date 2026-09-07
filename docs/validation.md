# Validation

Reading a document parses it, it does not check that it follows the SBGN-ML schema. `validate_xsd` performs that check against the packaged schema, `libsbgnpy/schema/SBGN.xsd`:

```python
from pathlib import Path

from libsbgnpy import validate_xsd

errors = validate_xsd(Path("map.sbgn"))
if errors:
    for error in errors:
        print(error)
else:
    print("valid")
```

The function returns the errors as a list of strings, which is empty for a valid document, so a check is `if validate_xsd(f):`. Nothing is written to stdout or stderr; a summary is logged at info level, see [Logging](installation.md#logging).

An error names the line, the element and what is wrong with it:

```
<string>:3:0:ERROR:SCHEMASV:SCHEMAV_CVC_COMPLEX_TYPE_4:
Element '{http://sbgn.org/libsbgn/0.3}map': The attribute 'id' is required but missing.
```

A file which is no well formed XML is reported as a single error rather than raising, so a corrupt file and an invalid one are handled the same way.

## Which schema is used

The packaged schema is the SBGN-ML 0.3 schema. Documents in the earlier namespaces are upconverted before they are validated, exactly as they are when they are read, see [Older SBGN-ML versions](io.md#older-sbgn-ml-versions). A 0.1 or 0.2 document is therefore validated against the 0.3 schema, which is what `libsbgnpy` reads it as.

## What is not checked

An XSD schema checks the structure of a document: which elements may occur where, which attributes are required, and which values an enumeration allows. It does not check the rules of the SBGN languages, e.g., that a consumption arc starts at an entity pool node and ends at a process, or that a process has at most one arc per port. Those rules are the validation rules of the SBGN specifications; they are not implemented, see [issue #60](https://github.com/matthiaskoenig/libsbgnpy/issues/60).

## Examples

| example | what it shows |
| --- | --- |
| [`validate.py`](https://github.com/matthiaskoenig/libsbgnpy/blob/develop/examples/validate.py) | validate documents and report the errors |
