# Installation

`libsbgnpy` requires python >= 3.11 and is available from [pypi](https://pypi.python.org/pypi/libsbgnpy).

## With uv

[uv](https://docs.astral.sh/uv/) is the recommended way to install the package. In a project it is added as a dependency, which resolves and locks it together with the rest of the environment:

```bash
uv add libsbgnpy
```

Into an existing virtual environment it is installed through the pip interface of uv:

```bash
uv venv
uv pip install libsbgnpy
```

## With pip

```bash
pip install libsbgnpy
```

## Development version

The current state of the `develop` branch is installed directly from GitHub:

```bash
uv add "libsbgnpy @ git+https://github.com/matthiaskoenig/libsbgnpy.git@develop"
```

or, with pip,

```bash
pip install git+https://github.com/matthiaskoenig/libsbgnpy.git@develop
```

To work on the repository itself, with the test and documentation tooling, see [Development](development.md).

## Dependencies

The package depends on [xsdata](https://github.com/tefra/xsdata), which reads and writes the SBGN-ML documents, [lxml](https://lxml.de/), which validates them against the schema, [requests](https://requests.readthedocs.io/), which queries the rendering web service, and [rich](https://rich.readthedocs.io/), which formats the output of the examples. `lxml` ships wheels for all common platforms, so no compiler is needed.

## Logging

`libsbgnpy` does not configure logging. It logs to loggers below the `libsbgnpy` logger and leaves handlers, levels and formatting to the application, so the messages of the package stay under your control:

```python
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger("libsbgnpy").setLevel(logging.WARNING)
```

For scripts and interactive work the rich output of the package can be turned on explicitly:

```python
from libsbgnpy import log

log.enable_rich_logging()
```
