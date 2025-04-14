# Information for developers
In this section information for developers are provided.

## Install develop dependencies

```bash
# install core dependencies
uv sync
# install dev dependencies
uv pip install -r pyproject.toml --extra dev
```

## Pre-commit hook
For developing please setup the pre-commit hook
```bash
uv pip install pre-commit
uv run pre-commit install
uv run pre-commit run
```

## Testing
Testing is performed with tox. See information on https://github.com/tox-dev/tox-uv
```bash
uv tool install tox --with tox-uv
```
Run single tox target
```bash
tox r -e py312
```
Run all tests in parallel
```bash
tox run-parallel
```

## Documentation
Setup environment
```bash
uv pip install -r pyproject.toml --extra docs
```

To test the documentation use
```bash
mkdocs serve
```

To build the documentation use
```bash
mkdocs build -d _site
```

### Jupyter notebooks
Part of the documentation are jupyter notebooks
To be able to run these the kernel must be installed for jupyter lab
pip install jupyterlab ipykernel

```bash
python -m ipykernel install --user --name=libsbgnpy --display-name="libsbgnpy"
```

## Release
Steps to create a new release:

* update release notes in `release-notes` with commit
* make sure all tests run (`tox -p`)
* check formating and linting (`ruff check`)
* test bump version (`uvx bump-my-version bump [major|minor|patch] --dry-run -vv`)
* bump version (`uvx bump-my-version bump [major|minor|patch] --python 3.13`)
* `git push --tags` (triggers release)
* `git push`
* test installation in virtualenv from pypi
```bash
uv venv --python 3.13
uv pip install libsbgnpy
```
