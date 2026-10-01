# Validation

Reading a document parses it, it does not check that it follows SBGN-ML. Three functions perform that check:

- `validate_xsd` validates against the packaged schema, `libsbgnpy/schema/SBGN.xsd`, i.e., the structure of the document,
- `validate` adds the rules of the SBGN specifications which the schema cannot express, see [What the specifications add](#what-the-specifications-add),
- `validate_schematron` checks the validation rules of the SBGN languages, e.g., that a consumption arc starts at an entity pool node, see [Schematron rules](#schematron-rules).

```python
from pathlib import Path

from libsbgnpy import validate

errors = validate(Path("map.sbgn"))
if errors:
    for error in errors:
        print(error)
else:
    print("valid")
```

`validate_xsd` and `validate` return the errors as a list of strings, which is empty for a valid document, so a check is `if validate(f):`. Nothing is written to stdout or stderr; a summary is logged at info level, see [Logging](installation.md#logging).

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

    A document which does not validate can often still be read. `read_sbgn_from_file` parses without validating, so an invalid class ends up in the bindings as the string it is written as, and a warning is logged. Only a document which lacks a required element or attribute, like the missing `end` of the arc above, cannot be read, it raises a `ParserError`. Validate first if a document comes from somewhere else.

## Which schema is used

The packaged schema is the SBGN-ML 0.3 schema. Documents in the earlier namespaces are upconverted before they are validated, exactly as they are when they are read, see [Older SBGN-ML versions](io.md#older-sbgn-ml-versions). A 0.1 or 0.2 document is therefore validated against the 0.3 schema, which is what `libsbgnpy` reads it as. The schema is the one of [sbgn/libsbgn](https://github.com/sbgn/libsbgn) with the versions PD L1V2.0 and L1V2.1 added, which the published schema lacks, see [The version of a map](specifications.md#the-version-of-a-map).

## What the specifications add

The schema has a single enumeration of glyph classes and of arc classes for all languages, and it cannot require one of two attributes. `validate` therefore checks, after the schema, the rules of the specifications which the schema lacks, see [SBGN specifications](specifications.md#checking-a-map):

- a map declares its language with a `version` or a `language`, SBGN-ML 0.3 requires one of them,
- the `version` and the `language` of a map name the same language,
- every glyph and every arc has a class of the language of the map, e.g., a `biological activity` is no glyph of a process description.

```
map 'm': glyph 'g1' has the class 'biological activity', which is no glyph class of process description
```

A deprecated class, e.g., the `perturbation` activity node of an activity flow map, is no error, it is logged as a warning. The checks are also available on a document which was read or created in python, as `check_sbgn` and `check_map`. A document which cannot be read is only validated against the schema.

## Schematron rules

The specifications of the SBGN languages define validation rules beyond the vocabulary of a map, e.g., that a consumption arc starts at an entity pool node and ends at a process, or that a process has at least one input and one output. The Java library [libSBGN](https://github.com/sbgn/libsbgn) implements them as Schematron rules, one set per map language, and `libsbgnpy` packages these rules: `validate_schematron` checks a document against them with the results of the Java library.

```python
from pathlib import Path

from libsbgnpy import validate_schematron

for issue in validate_schematron(Path("examples/sbgn/invalid.sbgn")):
    print(issue.rule_id, issue.element_id)
    print(f"  {issue.message}")
```

Every broken rule is reported as an `Issue`:

| attribute | meaning |
| --- | --- |
| `severity` | the role of the rule, `error` for all rules which are checked |
| `rule_id` | the rule, the language followed by its number, e.g., `pd10101` |
| `message` | what the rule requires |
| `element_id` | the id of the glyph or arc which breaks the rule, `None` if the rule does not name it |

The typo `simple chemcial` of [`invalid.sbgn`](#an-invalid-document) makes the source of the consumption arc no entity pool node, and the process loses its input:

```
pd10101 a01
  Arc with class consumption must have source reference to glyph of EPN classes
pd10141 pn1
  All process nodes should have at least one input and at least one ouput pointing to the arcs
```

The document is read like `validate_xsd` reads it, a 0.1 or 0.2 document is upconverted first. Every map is checked on its own with the rules of its language, which is taken from its `version` or else its `language`; a map of an unknown language is not checked, which `validate` reports. The rules do not check the structure of the document, so validate it against the schema as well, and a file which is no well-formed XML raises an `lxml.etree.XMLSyntaxError`.

!!! note

    The rules were written for the earlier specifications, e.g., PD L1V1.3, and some of the reference maps of the current specifications break them. Rule `pd10131`, for example, requires every entity pool node to be connected to an arc, which the maps showing glyphs on their own break. The issues are therefore kept apart from the errors of `validate`; review them rather than rejecting a document because of them. The rules are the ones of libSBGN with three XPath 2.0 expressions rewritten for the XSLT 1.0 processor of lxml, see [`libsbgnpy/schema/README.md`](https://github.com/matthiaskoenig/libsbgnpy/blob/develop/src/libsbgnpy/schema/README.md).

## Examples

| example | what it shows |
| --- | --- |
| [`validate.py`](https://github.com/matthiaskoenig/libsbgnpy/blob/develop/examples/validate.py) | validate the documents in `examples/sbgn/` and report the errors and the broken rules |

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
  pd10101 'a01'
    Arc with class consumption must have source reference to glyph of EPN classes
  pd10141 'pn1'
    All process nodes should have at least one input and at least one ouput pointing to the arcs
valid: neuronal_muscle_signalling_color.sbgn

4/5 documents are valid
invalid: invalid.sbgn
```
