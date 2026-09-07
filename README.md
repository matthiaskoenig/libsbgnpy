![libsbgnpy logo](https://github.com/matthiaskoenig/libsbgnpy/raw/develop/docs/images/libsbgnpy.png)

# libsbgnpy: python library for SBGN

[![GitHub Actions CI/CD Status](https://github.com/matthiaskoenig/libsbgnpy/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/matthiaskoenig/libsbgnpy/actions/workflows/ci-cd.yml)
[![Documentation](https://img.shields.io/badge/docs-libsbgnpy-3f51b5.svg)](https://matthiaskoenig.github.io/libsbgnpy)
[![Version](https://img.shields.io/pypi/v/libsbgnpy.svg)](https://pypi.org/project/libsbgnpy/)
[![Python Versions](https://img.shields.io/pypi/pyversions/libsbgnpy.svg)](https://pypi.org/project/libsbgnpy/)
[![MIT License](https://img.shields.io/pypi/l/libsbgnpy.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.597155.svg)](https://doi.org/10.5281/zenodo.597155)

`libsbgnpy` is a python library to work with the [Systems Biology Graphical Notation (SBGN)](https://sbgn.github.io/). It provides the python bindings of the SBGN-ML schema, generated with [xsdata](https://github.com/tefra/xsdata), and reads, writes, validates and renders SBGN documents.

```python
from pathlib import Path

from libsbgnpy import read_sbgn_from_file, render_sbgn

sbgn = read_sbgn_from_file(Path("map.sbgn"))
render_sbgn(sbgn, Path("map.png"))
```

![Ethanol example](https://github.com/matthiaskoenig/libsbgnpy/raw/develop/docs/images/ethanol_example.png)

## Installation

```bash
pip install libsbgnpy
```

## Documentation

The documentation is at **[matthiaskoenig.github.io/libsbgnpy](https://matthiaskoenig.github.io/libsbgnpy)**:

- [Installation](https://matthiaskoenig.github.io/libsbgnpy/installation/)
- [SBGN maps](https://matthiaskoenig.github.io/libsbgnpy/maps/) — the object model
- [Reading and writing](https://matthiaskoenig.github.io/libsbgnpy/io/), [notes and extensions](https://matthiaskoenig.github.io/libsbgnpy/extensions/), [render information](https://matthiaskoenig.github.io/libsbgnpy/render/), [validation](https://matthiaskoenig.github.io/libsbgnpy/validation/), [images](https://matthiaskoenig.github.io/libsbgnpy/images/)
- [API reference](https://matthiaskoenig.github.io/libsbgnpy/api/)
- [Contributing](https://matthiaskoenig.github.io/libsbgnpy/development/)

Runnable examples are in [`examples/`](./examples), the release notes in [`release-notes/`](./release-notes).

## How to cite

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.597155.svg)](https://doi.org/10.5281/zenodo.597155)

If you use `libsbgnpy` please cite the archived software on Zenodo, see [`CITATION.cff`](./CITATION.cff).

## License

- Source Code: [MIT](https://opensource.org/license/MIT)
- Documentation: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

## Funding

Matthias König (MK) was supported by the Federal Ministry of Education and Research (BMBF, Germany) within the research network Systems Medicine of the Liver (LiSyM, grant number 031L0054). MK is supported by the Federal Ministry of Education and Research (BMBF, Germany) within ATLAS by grant number 031L0304B and by the German Research Foundation (DFG) within the Research Unit Program FOR 5151 QuaLiPerF (Quantifying Liver Perfusion-Function Relationship in Complex Resection - A Systems Medicine Approach) by grant number 436883643 and by grant number 465194077 (Priority Programme SPP 2311, Subproject SimLivA).

© 2016-2026 Matthias König
