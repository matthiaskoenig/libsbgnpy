# Schemas and rules of SBGN-ML

This folder holds the XML schemas the python bindings are generated from and `validate_xsd` validates against, and the schematron rules `validate_schematron` checks. All of them come from [sbgn/libsbgn](https://github.com/sbgn/libsbgn), which is licensed under the LGPL 2.1 or later or the Apache License 2.0, see `LICENSE-libsbgn.txt`; `libsbgnpy` uses them under the Apache License 2.0, the changes are listed below.

## Generating the python bindings with xsdata

`libsbgnpy.sbgn` and `libsbgnpy.render` are generated from the XML schemas in this folder with [xsdata](https://github.com/tefra/xsdata) and must not be edited by hand. The current schemas are published with [sbgn/libsbgn](https://github.com/sbgn/libsbgn) in the `resources` folder.

### Generate

```bash
uv sync --extra dev
uv run python scripts/generate_bindings.py
```

The script is the single source of truth for the generation, `xsdata[cli]` is a dev dependency. `tests/test_bindings.py` runs `scripts/generate_bindings.py --check`, which fails if the committed bindings differ from freshly generated ones; a hand edit of the modules, an update of the schemas or of xsdata therefore requires a regeneration.

### Changes to the upstream schema

`SBGN.xsd` is the schema of [sbgn/libsbgn](https://github.com/sbgn/libsbgn) with one change, marked with a comment in the schema: the `version` of a map allows the identifiers of PD L1V2.1 and PD L1V2.0. The upstream schema lacks both, although the SBGN-ML 0.3 specification lists PD L1V2.0; PD L1V2.1 is the latest PD specification (2026). `validate_xsd` validates against this file, so the change is made in the schema itself and not by the generation script.

### Fixes applied by the script

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

### Open points

- [ ] the plurals of the list attributes: `map`, `glyph`, `arc` instead of `maps`, `glyphs`, `arcs`; changing them breaks the API

## Schematron rules

`sbgn_pd.sch`, `sbgn_er.sch` and `sbgn_af.sch` are the rules of the SBGN languages in `validation/rules` of [sbgn/libsbgn](https://github.com/sbgn/libsbgn) at commit [`2aae05b`](https://github.com/sbgn/libsbgn/tree/2aae05b). The Java library runs them with Saxon, an XSLT 2.0 processor; `libsbgnpy` runs them with `lxml.isoschematron`, which implements XSLT 1.0 and XPath 1.0. Three expressions of the rules are XPath 2.0, they are rewritten into XPath 1.0 and marked with a `libsbgnpy:` comment:

- `sbgn_pd.sch`, rule `pd10133`: `count(distinct-values(//sbgn:arc[@source = $port-id-N]/@target))` counts the distinct targets of the arcs leaving a port; `count(//sbgn:arc[@source = $port-id-N][@target][not(@target = preceding::sbgn:arc[@source = $port-id-N]/@target)])` counts the arcs with a target which no earlier arc of the port has, which is the same number (N = 1, 2); `test_pd10133` pins the rewrite, libsbgn has no test files for the rule,
- `sbgn_er.sch`, rule `er20001`: `../local-name()` becomes `local-name(..)`.

With these changes the rules report the same rule failures as the Java library on the test files of libsbgn and on `tests/data`. Besides, the line endings are converted to LF and trailing whitespace is removed, the conventions of the repository.

The rules do not follow the ISO Schematron grammar in every detail (pattern ids which are no XML names, `let` after `assert`, a `name` on an `assert`), so they are compiled without checking the grammar. Only the `basic` phase is run, as in Java; the `sanity` phase is a single assertion which always fails and uses XPath 2.0.

`tests/data/schematron` holds the matching test files of `validation/error-test-files`, one file which breaks a rule (`*-fail.sbgn`) and one which does not (`*-pass.sbgn`) per rule.

### Update

Copy the rules of a newer commit, normalize the whitespace, reapply the rewrites of the XPath 2.0 expressions, update the commit above and run `pytest tests/test_schematron.py`: `test_rules_compile_with_xslt1` fails while an XPath 2.0 expression remains which XSLT 1.0 cannot compile, the test files fail for expressions which only fail when they are evaluated.
