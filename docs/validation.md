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

## An invalid document

[`examples/sbgn/invalid.sbgn`](https://github.com/matthiaskoenig/libsbgnpy/blob/develop/examples/sbgn/invalid.sbgn) breaks the schema in three ways, one per kind of error the validation reports:

```xml
<sbgn xmlns="http://sbgn.org/libsbgn/0.3">
  <map language="process description">                            <!-- no id -->
    <bbox x="0" y="0" w="363" h="253"/>
    <glyph class="simple chemcial" id="glyph_ethanol">             <!-- typo -->
      <label text="Ethanol"/>
      <bbox x="40" y="120" w="60" h="60"/>
    </glyph>
    ...
    <arc class="consumption" source="glyph_ethanol" target="pn1.1" id="a01">
      <start x="98" y="160"/>                                 <!-- no end -->
    </arc>
  </map>
</sbgn>
```

`validate_xsd` returns the three errors:

```python
from pathlib import Path

from libsbgnpy import validate_xsd

for error in validate_xsd(Path("examples/sbgn/invalid.sbgn")):
    print(error)
```

- a required attribute is missing, the `id` of the map:

    ```
    SCHEMAV_CVC_COMPLEX_TYPE_4: Element '{http://sbgn.org/libsbgn/0.3}map':
    The attribute 'id' is required but missing.
    ```

- an attribute carries a value which is not in the enumeration, `simple chemcial` is not an SBGN glyph class. The error lists every class the schema allows, which is the fastest way to find the correct spelling:

    ```
    SCHEMAV_CVC_ENUMERATION_VALID: Element '{http://sbgn.org/libsbgn/0.3}glyph',
    attribute 'class': [facet 'enumeration'] The value 'simple chemcial' is not
    an element of the set {'unspecified entity', 'simple chemical', ...}.
    ```

- a required child element is missing, an arc needs an `end` point:

    ```
    SCHEMAV_ELEMENT_CONTENT: Element '{http://sbgn.org/libsbgn/0.3}arc':
    Missing child element(s). Expected is one of
    ( {http://sbgn.org/libsbgn/0.3}next, {http://sbgn.org/libsbgn/0.3}end ).
    ```

The line number in front of every error, e.g. `<string>:13:0:`, is the line of the *upconverted* document, which is what the validation sees, see [Which schema is used](#which-schema-is-used). For a 0.3 document it is the line of the file; for a 0.1 or 0.2 document only the namespace of the root element changes, so the lines still match.

!!! note

    A document which does not validate can still be read. `read_sbgn_from_file` parses without validating, so the invalid classes end up in the bindings as they are written. Validate first if a document comes from somewhere else.

## Which schema is used

The packaged schema is the SBGN-ML 0.3 schema. Documents in the earlier namespaces are upconverted before they are validated, exactly as they are when they are read, see [Older SBGN-ML versions](io.md#older-sbgn-ml-versions). A 0.1 or 0.2 document is therefore validated against the 0.3 schema, which is what `libsbgnpy` reads it as.

## What is not checked

An XSD schema checks the structure of a document: which elements may occur where, which attributes are required, and which values an enumeration allows. It does not check the rules of the SBGN languages, e.g., that a consumption arc starts at an entity pool node and ends at a process, or that a process has at most one arc per port. Those rules are the validation rules of the SBGN specifications; they are not implemented, see [issue #60](https://github.com/matthiaskoenig/libsbgnpy/issues/60).

## Examples

| example | what it shows |
| --- | --- |
| [`validate.py`](https://github.com/matthiaskoenig/libsbgnpy/blob/develop/examples/validate.py) | validate the documents in `examples/sbgn/` and report the errors |

```bash
python examples/validate.py
```

```
valid: adh.sbgn
valid: adh_0.3.sbgn
valid: glycolysis.sbgn
invalid: invalid.sbgn
  <string>:11:0:ERROR:SCHEMASV:SCHEMAV_CVC_COMPLEX_TYPE_4: ...
  <string>:13:0:ERROR:SCHEMASV:SCHEMAV_CVC_ENUMERATION_VALID: ...
  <string>:22:0:ERROR:SCHEMASV:SCHEMAV_ELEMENT_CONTENT: ...
valid: neuronal_muscle_signalling_color.sbgn

4/5 documents are valid
invalid: invalid.sbgn
```
