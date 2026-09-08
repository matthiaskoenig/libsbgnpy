# Development

Contributions are welcome. The repository is [matthiaskoenig/libsbgnpy](https://github.com/matthiaskoenig/libsbgnpy); development happens against the `develop` branch via pull requests.

## Branch model

Two branches are permanent:

- **`develop`** is the default branch and the branch everything is integrated into. The documentation on [matthiaskoenig.github.io/libsbgnpy](https://matthiaskoenig.github.io/libsbgnpy) is published from it.
- **`main`** tracks the latest published release. It is fast-forwarded to the released commit by the `sync-main` job of the `CI-CD` workflow after the package went to pypi, so `main` and the newest version on pypi always agree. Nothing is developed on `main` and nothing is merged into it by hand.

Work happens on short lived branches off `develop`, which GitHub deletes after the merge. Releases are tagged on `develop`, see [Release](#release).

## Pull requests

Neither branch accepts a direct push, every change goes through a pull request against `develop`. This includes the maintainer, there is no bypass.

A pull request can only be merged once the four required checks are green:

| check   | workflow      | content                                                              |
| ------- | ------------- | -------------------------------------------------------------------- |
| `tests` | `ci-cd.yml`   | the test matrix, linux, macos and windows with python 3.11 to 3.14    |
| `ruff`  | `ruff.yml`    | `ruff check` and `ruff format --check`                                |
| `ty`    | `ty.yml`      | `tox r -e ty`                                                         |
| `docs`  | `docs.yml`    | the zensical build including the api reference and the agent files    |

`tests` aggregates the test matrix into a single job, so the name of the required check stays the same when the matrix changes.

Further rules of a pull request:

- conversations have to be resolved before the merge
- an approval is dismissed when new commits are pushed
- the history stays linear, i.e., a pull request is merged with squash or rebase; merge commits are disabled
- the maintainer is the code owner of the repository (`.github/CODEOWNERS`) and is requested for review on every pull request. A pull request of a contributor is therefore reviewed and merged by the maintainer, who has the only write access. The rulesets themselves do not require an approval: on a personal repository a ruleset cannot ask for an approval only from somebody else, and requiring one would block the pull requests of the maintainer, who cannot approve their own. Once a second person has write access, a ruleset requiring an approving review of a code owner can be added

[Auto-merge](https://docs.github.com/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/automatically-merging-a-pull-request) is enabled for the repository, so a pull request can be queued and is merged as soon as the checks pass and the required approval is there.

### Repository policies { #repository-policies }

The protection is implemented with [repository rulesets](https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets). They are part of the repository in `.github/rulesets/` instead of only living in the web interface, so a change to a policy is reviewed like any other change:

| ruleset                 | applies to | rules                                                                                                                                       |
| ----------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `develop.json`          | `develop`  | pull request required, the four checks above, resolved conversations, linear history, no force push, no deletion. **No bypass, for anybody.** |
| `main.json`             | `main`     | linear history, no force push, no deletion, no bypass. The fast-forward of the release workflow needs none, only a force push or a merge commit would be rejected |
| `tags.json`             | all tags   | a tag cannot be deleted or moved, so a release tag keeps pointing at what was released                                                       |

Changing a policy means changing the json and applying it:

```bash
.github/rulesets/apply.sh
```

The script is idempotent: it updates the rulesets which exist and creates the missing ones. It also sets the merge settings of the repository, i.e., auto-merge, delete branch on merge, and squash and rebase as the only merge methods. It needs the [github cli](https://cli.github.com) authenticated as a user with admin permission on the repository.

## Setup development environment

Development needs [uv](https://docs.astral.sh/uv/) and a checkout of the repository:

```bash
git clone https://github.com/matthiaskoenig/libsbgnpy.git
cd libsbgnpy
```

A single sync creates the virtual environment in `.venv`, installs `libsbgnpy` into it in editable mode and adds the complete tooling:

```bash
uv sync --extra dev
```

The `dev` extra contains everything used below, i.e., pytest, ruff, ty, tox, pre-commit, zensical and bump-my-version, so nothing has to be installed separately. The python version is taken from `.python-version` (currently 3.14); to work against the oldest supported version instead use `uv sync --extra dev --python 3.11`, which replaces the environment.

The tools are then run either with `uv run <command>`, which uses the environment without activating it, or from the activated environment:

```bash
source .venv/bin/activate        # Linux and macOS
.venv\Scripts\activate           # Windows
```

The commands in this document are written without the `uv run` prefix; prepend it if the environment is not activated.

The last step installs the git hook:

```bash
uv run pre-commit install          # install the hook, once per checkout
uv run pre-commit run --all-files  # check the current state of the repository
```

From now on every commit is checked with ruff (lint and format) and ty, i.e., the same checks that run in continuous integration. On a commit only the changed files are looked at, `--all-files` checks the whole repository and is what a newly added hook should be tried with.

## Testing

The tests are written with pytest, tox runs them against every supported python version.

The tox environments are named after the interpreter (`py3.11` to `py3.14`, see `envlist` in `tox.ini`), a single one is run with
```bash
tox r -e py3.14
```
and the complete matrix, including the `ty` environment, in parallel with
```bash
tox run-parallel
```

This needs the interpreters to be available, which uv installs with `uv python install 3.11 3.12 3.13 3.14`. Continuous integration runs the same environments as `uvx --with tox-uv tox -e py3.14`.

To run the tests directly against the development environment use

```bash
pytest                                    # the full suite
pytest tests/test_io.py                   # a single module
pytest tests/test_io.py::test_upconvert   # a single test
```

`tests/data` holds the reference maps of the SBGN specifications, one directory per map language. `tests/test_data.py` reads, writes and validates every one of them, so a change to the bindings or to the io is checked against the whole corpus.

`tests/test_examples.py` runs every example of `examples/` in a temporary working directory, which keeps the examples of the documentation working. The tests of `tests/test_image.py` query the rendering web service and therefore require network access.

## Linting and formatting

Linting and formatting use [ruff](https://docs.astral.sh/ruff/):

```bash
ruff check     # lint
ruff format    # format
```

The generated bindings, `libsbgnpy/sbgn.py` and `libsbgnpy/render.py`, are excluded from the docstring rules, see `[lint.per-file-ignores]` in `.ruff.toml`; their docstrings are the documentation of the schema.

## Type checking

Type checking is performed with [ty](https://docs.astral.sh/ty/):

```bash
tox r -e ty
```
Or directly in the working tree:
```bash
uvx ty check
```

The configuration lives in `[tool.ty]` in `pyproject.toml`. Warnings are treated as errors, so the codebase is kept free of diagnostics. Suppress an unavoidable diagnostic with a rule specific `# ty: ignore[rule-name]` rather than a blanket comment.

## Documentation

The documentation is built with [Zensical](https://zensical.org/), the static site generator of the Material for MkDocs authors. The sources are markdown files in `docs/`, the site is configured in `zensical.toml` in the repository root. Nothing rendered is committed: the site is built by the `documentation` workflow on every push and published to [matthiaskoenig.github.io/libsbgnpy](https://matthiaskoenig.github.io/libsbgnpy) from the `develop` branch.

Build the site into `site/`:

```bash
uv run zensical build --clean
```

For writing, the preview rebuilds on save:

```bash
uv run zensical serve
```

The API reference is rendered from the docstrings by [mkdocstrings](https://mkdocstrings.github.io/); a page in `docs/api/` only contains the module directive:

```markdown
# io

::: libsbgnpy.io
```

Docstrings are therefore the place to document functions and classes, the markdown files provide the narrative around them. Adding a module to the reference means adding such a page and an entry to `nav` in `zensical.toml`.

### Files for agents { #files-for-agents }

Agents and language models read markdown, not rendered html. `scripts/llms_txt.py` writes the files of the [llms.txt convention](https://llmstxt.org/) into the built site, i.e., [llms.txt](https://matthiaskoenig.github.io/libsbgnpy/llms.txt) as an annotated index of all pages, [llms-full.txt](https://matthiaskoenig.github.io/libsbgnpy/llms-full.txt) with the complete documentation in a single file, and the markdown of every page next to its html (`/io.md` for `/io/`). The markdown of the API reference is generated from the docstrings with `inspect`, since the pages themselves only contain the mkdocstrings directive.

```bash
uv run zensical build --clean
uv run python scripts/llms_txt.py
```

The `documentation` workflow runs both steps, so the files are regenerated with every push. `docs/robots.txt` points crawlers at the sitemap and at these files.

## Regenerating the bindings { #regenerating-the-bindings }

`libsbgnpy.sbgn` and `libsbgnpy.render` are generated modules and should not be edited by hand. They are generated from the schemas in `src/libsbgnpy/schema/` with [xsdata](https://github.com/tefra/xsdata); the current schemas are published with [sbgn/libsbgn](https://github.com/sbgn/libsbgn) in the `resources` folder. The procedure and the manual fixes which are applied afterwards are described in `src/libsbgnpy/schema/README.md`.

Run `ruff format` and `ruff check --fix` afterwards, the generated modules are neither formatted nor on current python syntax.

## Work in progress

`libsbgnpy.oven` collects unfinished work: it is not wired into the package, not documented, not part of the public API and not shipped in the release, see `[tool.hatch.build]` in `pyproject.toml`. It currently holds the mapping of SBO terms to SBGN glyphs, groundwork for the conversion of SBML to SBGN, see [issue #52](https://github.com/matthiaskoenig/libsbgnpy/issues/52).

## Release

A release is made from `develop`. Since `develop` only accepts pull requests, the release is prepared on a branch and tagged once that pull request is merged:

1. branch off `develop`: `git switch -c release/x.y.z develop`
2. write the release notes for the version in `release-notes/x.y.z.md`
3. make sure everything passes: `tox run-parallel`, `ruff check`, `tox r -e ty`
4. check the version bump: `uvx bump-my-version bump [major|minor|patch] --dry-run -vv`
5. bump the version: `uvx bump-my-version bump [major|minor|patch]`, which updates `src/libsbgnpy/__init__.py` and `CITATION.cff` and commits. It does not create the tag; a squash or rebase merge would rewrite the commit and leave the tag behind on a commit which is not part of `develop`
6. push the branch, open the pull request against `develop` and merge it once the checks are green
7. tag the merged commit on `develop` and push the tag:

    ```bash
    git switch develop
    git pull
    git tag x.y.z
    git push origin x.y.z
    ```

    This starts the `CI-CD` workflow, which runs the test matrix, publishes to [pypi](https://pypi.org/project/libsbgnpy/), creates the GitHub release from `release-notes/x.y.z.md` and fast-forwards `main` to the tagged commit. Check the version before pushing, a tag cannot be moved or deleted afterwards.

8. test the installation from pypi in a fresh environment:

    ```bash
    uv venv --python 3.14
    uv pip install libsbgnpy
    ```

9. once Zenodo has archived the release, update the citation information: `date-released` and the version DOI in `doi` and `identifiers` of `CITATION.cff`, and the citation and the bibtex entry of the `How to cite` section of `docs/index.md`. `bump-my-version` only updates the version, neither the date nor the DOI, which are only known after the release. The badges and the `README.md` carry the concept DOI, which always resolves to the latest version, and stay as they are. These changes go in through a pull request like everything else
