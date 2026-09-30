# Generating the python bindings with xsdata

`libsbgnpy.sbgn` and `libsbgnpy.render` are generated from the XML schemas in this folder with [xsdata](https://github.com/tefra/xsdata) and must not be edited by hand. The current schemas are published with [sbgn/libsbgn](https://github.com/sbgn/libsbgn) in the `resources` folder.

## Generate

```bash
uv sync --extra dev
uv run python scripts/generate_bindings.py
```

The script is the single source of truth for the generation, `xsdata[cli]` is a dev dependency. `tests/test_bindings.py` runs `scripts/generate_bindings.py --check`, which fails if the committed bindings differ from freshly generated ones; a hand edit of the modules, an update of the schemas or of xsdata therefore requires a regeneration.

## Fixes applied by the script

- the html of the schema documentation (`<p>`, `<ul>`, `<li>`, `<a>`) is converted to plain text on a temporary copy of the schemas, otherwise xsdata copies the markup with namespace prefixes into the docstrings
- the docstrings are google style (`--docstring-style Google`), the convention of the package
- the module docstrings at the top of `sbgn.py` and `render.py`
- in `render.py` the namespace of the attributes is commented out: `render.xsd` declares them globally and references them (`<xs:attribute ref="render:id"/>`), which makes them namespace qualified, but they are written without a namespace:

  ```python
  id: str = field(
      metadata={
          "type": "Attribute",
          # "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
      }
  )
  ```

- `ruff check --fix` and `ruff format` with the configuration of the repository

## Open points

- [ ] the plurals of the list attributes: `map`, `glyph`, `arc` instead of `maps`, `glyphs`, `arcs`; changing them breaks the API
