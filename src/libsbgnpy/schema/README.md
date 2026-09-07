# Generating the python bindings with xsdata

`libsbgnpy.sbgn` and `libsbgnpy.render` are generated from the XML schemas in
this folder with [xsdata](https://github.com/tefra/xsdata) and should not be
edited by hand. The current schemas are published with
[sbgn/libsbgn](https://github.com/sbgn/libsbgn) in the `resources` folder.

## Generate

```bash
uvx --with "xsdata[cli,lxml,soap]" xsdata generate SBGN.xsd --package libsbgn
```

Copy the generated modules to `src/libsbgnpy/` and merge the content of the
generated `__init__` into `src/libsbgnpy/__init__.py`.

## Manual fixes

The following changes are applied to the generated code, they are lost when the
modules are regenerated:

- the module docstrings at the top of `sbgn.py` and `render.py`
- in `render.py` the namespace of the attributes is commented out, they are
  written without a namespace:

  ```python
  id: str = field(
      metadata={
          "type": "Attribute",
          # "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
          "required": True,
      }
  )
  ```

Run `ruff format` and `ruff check --fix` afterwards, the generated modules are
neither formatted nor on current python syntax.

## Open points

- [ ] the documentation of the schema is copied into the docstrings with its
      namespace prefixes, e.g., `<ns1:p xmlns:ns1="...">`
- [ ] the plurals of the list attributes: `map`, `glyph`, `arc` instead of
      `maps`, `glyphs`, `arcs`
