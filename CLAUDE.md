# CLAUDE.md

This file provides guidance when working with code in this repository.

## Project

`libsbgnpy` is a python library for the Systems Biology Graphical Notation (SBGN): the python bindings of the SBGN-ML schema plus reading, writing, validation and image rendering of SBGN documents. Pure library, no CLI entry points. Requires python >= 3.11, packaged with hatchling (version is read from `src/libsbgnpy/__init__.py`). Runtime dependencies are `xsdata` (XML binding), `lxml` (schema validation), `requests` (rendering web service) and `rich` (output of the examples).

## Commands

```bash
# environment (uv based)
uv sync --extra dev
uv run pre-commit install

# tests
pytest                                    # all tests
pytest tests/test_io.py                   # single file
pytest tests/test_io.py::test_upconvert   # single test
tox r -e py3.14                           # single tox env (py3.11-3.14 available)
tox run-parallel                          # full matrix + ty

# lint / format / types
ruff check
ruff format
tox -e ty                       # ty type check (config in [tool.ty] in pyproject.toml)
uvx ty check                    # same check, straight from the working tree

# examples, they are scripts and not part of the package
python examples/read.py
```

Release steps are in `docs/development.md`; version bumps go through `uvx bump-my-version bump [major|minor|patch]` (updates `src/libsbgnpy/__init__.py` and `CITATION.cff`), and pushing the tag triggers the PyPI release workflow.

Documentation is [Zensical](https://zensical.org/): markdown sources in `docs/`, configured in `zensical.toml`, built into the gitignored `site/` (`uv run zensical build --clean`, `uv run zensical serve` for the preview). The API reference is rendered from the docstrings by mkdocstrings; a page in `docs/api/` is just `::: libsbgnpy.<module>`, so nothing is generated into the repository. `scripts/llms_txt.py` runs after the build and writes the agent facing files (`llms.txt`, `llms-full.txt` and the markdown of every page) into `site/`. The `documentation` workflow runs both and publishes the site from `develop`.

## Architecture

**`sbgn.py` and `render.py` are generated code.** They are the bindings of `schema/SBGN.xsd` and `schema/render.xsd`, generated with xsdata; do not hand-edit them. The classes are keyword-only dataclasses which mirror the schema: `Sbgn` holds `Map` objects, a map holds `Glyph`, `Arc` and `Arcgroup` objects, glyphs nest (a compartment or a complex holds its content, auxiliary units are glyphs), a `Glyph` of class `PROCESS` carries the `Port` objects the arcs attach to, and `Bbox` plus the `start`/`end`/`next` points of an arc carry the layout. `class_value` is the SBGN class, `class` being a keyword. Every element inherits from `Sbgnbase`, which carries `notes` and `extension`. Regeneration and the manual fixes applied afterwards are documented in `src/libsbgnpy/schema/README.md`.

**`io.py` — reading and writing.** The entry points of the package. `read_sbgn_from_file`/`read_sbgn_from_string` parse (without validating) and apply `upconvert`, which rewrites the SBGN-ML 0.1 and 0.2 namespaces to 0.3, so older documents are read as 0.3 documents. `write_sbgn_to_file`/`write_sbgn_to_string` serialize into the 0.3 namespace.

The subtle part is the raw XML of `notes` and `extension`: the schema allows arbitrary content there, so the bindings type it as `list[object]`. It is *set* as a string and *read back* as an `AnyElement` tree. `write_sbgn_to_string` therefore deep-copies the document and converts every raw string into an element tree (`_with_parsed_raw_xml` → `element_from_string`) before serializing, because the serializer escapes a string as text and writes only the first entry of such a list inside the element. `element_to_string` is the inverse for reading, and `read_render_from_extension` uses it to find and parse the `renderInformation` of a map. The conversion between `AnyElement` and XML goes through lxml (`_element_to_node`, `_node_to_element`).

**`validator.py` — schema validation.** `validate_xsd` validates against the packaged `schema/SBGN.xsd` and returns the errors as a list of strings, empty for a valid document; it upconverts first, so 0.1 and 0.2 documents validate as well. It logs, it does not print. Only the structure is checked, not the validation rules of the SBGN specifications.

**`image.py` — rendering.** `render_sbgn` posts the document to the rendering web service at `RENDER_URL` and writes the returned PNG; it needs network access and is the only module which does.

`console.py` (rich console, for scripts and examples) and `log.py` provide the shared output/logging. Modules get their logger from the standard library with `logging.getLogger(__name__)`. The package never configures logging: no handlers, no levels, only a `NullHandler` on the `libsbgnpy` logger; `log.enable_rich_logging()` is the opt-in for scripts. Library code logs, it does not print, and log calls use lazy `%s` formatting rather than f-strings (enforced by ruff `G`).

**`oven/`** holds unfinished work which is deliberately undocumented and untested: it is not wired into the package and excluded from the build, see `[tool.hatch.build]` in `pyproject.toml`. It currently holds the SBO to SBGN mapping, groundwork for an SBML to SBGN conversion (#52).

## Conventions

- Type checking is done with [ty](https://docs.astral.sh/ty/) (mypy was removed in 0.6.0). `[tool.ty.terminal] error-on-warning = true` means warnings fail the check, so the tree must stay at zero diagnostics; the checked python version is inferred from `project.requires-python`. Suppress a diagnostic with a rule-specific `# ty: ignore[rule-name]`, never a blanket `# type: ignore`. ty also runs as a pre-commit hook (`--extra dev`).
- Every module, class and function carries full type annotations and a google-style docstring. The generated bindings are exempt from the docstring rules, see `[lint.per-file-ignores]` in `.ruff.toml`.
- `examples/` at the top level holds the runnable usage examples, they are not part of the package and every one of them is run by `tests/test_examples.py` in a temporary working directory. `examples/sbgn/` holds the documents they read. Only `examples/ethanol.py` needs network access.
- `tests/data/` holds the reference maps of the SBGN specifications, one directory per map language (`AF`, `ER`, `PD`); `tests/test_data.py` reads, writes and validates all of them.
- Markdown carries no hard line wraps: a paragraph, a list item or a table row is a single line and the wrapping is left to the editor.
- Release notes go in `release-notes/` as part of a release commit.
