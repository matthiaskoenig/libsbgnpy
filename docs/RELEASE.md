# Release information
Information on steps to make a release.

## make release
* update release notes in `release-notes` with commit
* make sure all tests run (`tox -p`)
* check formating and linting (`ruff check`)
* test bump version (`bump-my-version bump [major|minor|patch] --dry-run -vv`)
* bump version (`uvx bump-my-version bump [major|minor|patch] --python 3.13`)
* `git push --tags` (triggers release)
* `git push`
* test installation in virtualenv from pypi
```bash
uv venv --python 3.13
uv pip install libsbgnpy
```
