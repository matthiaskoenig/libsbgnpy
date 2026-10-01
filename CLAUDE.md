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
pytest -m network                         # tests querying the rendering web service (deselected by default)
tox r -e py3.14                           # single tox env (py3.11-3.15 available)
tox run-parallel                          # full matrix + ty

# lint / format / types
ruff check
ruff format
tox -e ty                       # ty type check (config in [tool.ty] in pyproject.toml)
uvx ty check                    # same check, straight from the working tree

# examples, they are scripts and not part of the package
python examples/read.py
```

`develop` is the default branch and takes every change through a pull request; direct pushes are rejected by the rulesets in `.github/rulesets/` (applied with `.github/rulesets/apply.sh`), which require the `tests`, `ruff`, `ty` and `docs` checks. `main` only tracks the latest release and is fast-forwarded by the `sync-main` job of the release workflow, never by hand.

Release steps are in `docs/development.md`: the release is prepared on a branch, `uvx bump-my-version bump [major|minor|patch]` updates `src/libsbgnpy/__init__.py` and `CITATION.cff` and commits without tagging (`tag = false`, a squash merge would rewrite the commit), and the tag is created on `develop` after the pull request was merged, which triggers the PyPI release workflow.

Documentation is [Zensical](https://zensical.org/): markdown sources in `docs/`, configured in `zensical.toml`, built into the gitignored `site/` (`uv run zensical build --clean`, `uv run zensical serve` for the preview). The API reference is rendered from the docstrings by mkdocstrings; a page in `docs/api/` is just `::: libsbgnpy.<module>`, so nothing is generated into the repository. `scripts/llms_txt.py` runs after the build and writes the agent facing files (`llms.txt`, `llms-full.txt` and the markdown of every page) into `site/`. The `documentation` workflow runs both and publishes the site from `develop`.

## Architecture

**`sbgn.py` and `render.py` are generated code.** They are the bindings of `schema/SBGN.xsd` and `schema/render.xsd`, generated with xsdata; do not hand-edit them. The classes are keyword-only dataclasses which mirror the schema: `Sbgn` holds `Map` objects, a map holds `Glyph`, `Arc` and `Arcgroup` objects, glyphs nest (a compartment or a complex holds its content, auxiliary units are glyphs), a `Glyph` of class `PROCESS` carries the `Port` objects the arcs attach to, and `Bbox` plus the `start`/`end`/`next` points of an arc carry the layout. `class_value` is the SBGN class, `class` being a keyword. Every element inherits from `Sbgnbase`, which carries `notes` and `extension`. They are regenerated with `uv run python scripts/generate_bindings.py`, which applies every fix to the xsdata output (see `src/libsbgnpy/schema/README.md`); `tests/test_bindings.py` fails when the committed modules differ from a fresh generation.

**`io.py` — reading and writing.** The entry points of the package. `read_sbgn_from_file`/`read_sbgn_from_string` parse with `parse_xml` (untrusted input: no entity resolution, no network; a file is decoded with its declared encoding), move the SBGN-ML 0.1 and 0.2 namespaces to 0.3 with `upconvert_tree` (only element and attribute names change, never values), reject a root other than `sbgn` and bind the lxml tree with xsdata; every failure is an `xsdata.exceptions.ParserError`. They do not validate. `write_sbgn_to_file`/`write_sbgn_to_string` serialize into the 0.3 namespace.

The subtle part is the raw XML of `notes` and `extension`: the schema allows arbitrary content there, so the bindings type it as `list[object]`. It is *set* as a string and *read back* as an `AnyElement` tree. `write_sbgn_to_string` therefore deep-copies the document and converts every raw string into an element tree (`_with_parsed_raw_xml` → `element_from_string`) before serializing, because the serializer escapes a string as text and writes only the first entry of such a list inside the element. `element_to_string` is the inverse for reading, and `read_render_from_extension` uses it to find and parse the `renderInformation` of a map. The conversion between `AnyElement` and XML goes through lxml (`_element_to_node`, `_node_to_element`).

**`specification.py` - the SBGN specifications.** What the specifications add on top of the schema, as data: `SPECIFICATIONS` (every `MapVersion` to its language, level, version, year, DOI), `LATEST` (latest version per language, PD L1V2.1, ER L1V2.0, AF L1V1.2), `GLYPH_CLASSES`/`ARC_CLASSES` per language and `DEPRECATED_GLYPH_CLASSES`. `map_language` takes the language from `version`, falling back to the deprecated `language`; `check_map`/`check_sbgn` return the errors (language declared, `version` and `language` agree, classes belong to the language), deprecated classes are logged. The tables of `docs/specifications.md` are generated from this data by `scripts/specification_docs.py`, `tests/test_specification_docs.py` fails when they are outdated. The packaged `schema/SBGN.xsd` deviates from upstream libsbgn by the PD L1V2.0 and L1V2.1 version identifiers, see `src/libsbgnpy/schema/README.md`.

**`validator.py` - validation.** `validate_xsd` validates against the packaged `schema/SBGN.xsd` and returns the errors as a list of strings, empty for a valid document; it upconverts first, so 0.1 and 0.2 documents validate as well. `validate` adds the errors of `check_sbgn` for a readable document. It logs, it does not print.

**`schematron.py` - schematron rules.** `validate_schematron` checks a document against the schematron rules of libsbgn (`schema/sbgn_{pd,er,af}.sch`, `basic` phase as in Java) and returns `Issue` objects (severity, rule id, message, element id), separate from `validate`, since the rules are partly outdated and some reference maps break them. Every map is checked in a copy of the document without the other maps (the rules look up ids document wide) with the rules of its language (`specification.language_of` on the raw attributes). lxml runs XSLT 1.0 only, so the three XPath 2.0 expressions of the upstream rules are rewritten and marked with `libsbgnpy:` comments, see `src/libsbgnpy/schema/README.md`; the rules are compiled without the ISO grammar check, they deviate from it. `tests/data/schematron/` holds the upstream test files of the rules; the issues of the reference maps are pinned in `tests/test_schematron.py` and match Saxon, the processor of the Java library.

Reading keeps a value outside of an enumeration (an unknown glyph class or version) as a string and logs the xsdata `ConverterWarning` instead of emitting it.

**`image.py` — rendering.** `render_sbgn` posts the document to the rendering web service at `RENDER_URL` and writes the returned PNG; it needs network access and is the only module which does.

`console.py` (rich console, for scripts and examples) and `log.py` provide the shared output/logging. Modules get their logger from the standard library with `logging.getLogger(__name__)`. The package never configures logging: no handlers, no levels, only a `NullHandler` on the `libsbgnpy` logger; `log.enable_rich_logging()` is the opt-in for scripts. Library code logs, it does not print, and log calls use lazy `%s` formatting rather than f-strings (enforced by ruff `G`).

**`oven/`** holds unfinished work which is deliberately undocumented and untested: it is not wired into the package and excluded from the build, see `[tool.hatch.build]` in `pyproject.toml`. It currently holds the SBO to SBGN mapping, groundwork for an SBML to SBGN conversion (#52).

## Conventions

- Type checking is done with [ty](https://docs.astral.sh/ty/) (mypy was removed in 0.6.0). `[tool.ty.terminal] error-on-warning = true` means warnings fail the check, so the tree must stay at zero diagnostics; the checked python version is inferred from `project.requires-python`. Suppress a diagnostic with a rule-specific `# ty: ignore[rule-name]`, never a blanket `# type: ignore`. ty also runs as a pre-commit hook (`--extra dev`).
- Every module, class and function carries full type annotations and a google-style docstring. The generated bindings are exempt from the docstring rules, see `[lint.per-file-ignores]` in `.ruff.toml`.
- `examples/` at the top level holds the runnable usage examples, they are not part of the package and every one of them is run by `tests/test_examples.py` in a temporary working directory. `examples/sbgn/` holds the documents they read. Only `examples/ethanol.py` needs network access, it is marked as `network` like `test_render_sbgn` and only runs with `pytest -m network`.
- `tests/data/` holds the reference maps of the SBGN specifications, one directory per map language (`AF`, `ER`, `PD`); `tests/test_data.py` reads, writes and validates all of them. `tests/data/schematron/` holds the test files of the schematron rules, they break the rules on purpose and are not part of the corpus.
- Markdown carries no hard line wraps: a paragraph, a list item or a table row is a single line and the wrapping is left to the editor.
- Release notes go in `release-notes/` as part of a release commit.
