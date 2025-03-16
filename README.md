![libsbgnpy logo](https://github.com/matthiaskoenig/libsbgnpy/raw/develop/docs/images/libsbgnpy.png)

# libsbgnpy: Python library for SBGN

[![GitHub Actions CI/CD Status](https://github.com/matthiaskoenig/libsbgnpy/workflows/CI-CD/badge.svg)](https://github.com/matthiaskoenig/libsbgnpy/actions/workflows/main.yml)
[![Version](https://img.shields.io/pypi/v/libsbgnpy.svg)](https://pypi.org/project/libsbgnpy/)
[![Python Versions](https://img.shields.io/pypi/pyversions/libsbgnpy.svg)](https://pypi.org/project/libsbgnpy/)
[![MIT License](https://img.shields.io/pypi/l/libsbgnpy.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.597155.svg)](https://doi.org/10.5281/zenodo.597155)
[![Documentation Status](https://readthedocs.org/projects/libsbgnpy/badge/?version=latest)](http://libsbgnpy.readthedocs.io/en/latest/?badge=latest)


Python library to work with the Systems Biology Graphical Notation ([SBGN](http://sbgn.github.io/sbgn/)). This library is based on the SBGN XML schema and supports reading,
writing and validation of SBGN files.

The initial library was generated using [generateDS](https://pypi.org/project/generateDS/). Additional utility functions for reading, writing, and rendering SBGN documents are provided.

Documentation with examples is available at https://libsbgnpy.readthedocs.io.

* `libsbgn.py` python library
* `libsbgnTypes.py` SBGN type definitions (GlyphClasses, ArcClasses, Languages)
* `utils.py` SBGN utility function like writing & reading of files
* `render.py` SBGN rendering
* `test/` unittests
* `examples/` python examples
* `validation/` validation of SBGN files


# How to cite
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.597155.svg)](https://doi.org/10.5281/zenodo.597155)

# Installation
`libsbgnpy` is available from [pypi](https://pypi.python.org/pypi/libsbgnpy) and
can be installed via
```bash
pip install libsbgnpy
```

# License
- Source Code: [MIT](https://opensource.org/license/MIT)
- Documentation: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

# Funding
Matthias König (MK) was supported by the Federal Ministry of Education and Research (BMBF, Germany) within the research network Systems Medicine of the Liver (LiSyM, grant number 031L0054). MK is supported by the Federal Ministry of Education and Research (BMBF, Germany) within ATLAS by grant number 031L0304B and by the German Research Foundation (DFG) within the Research Unit Program FOR 5151 QuaLiPerF (Quantifying Liver Perfusion-Function Relationship in Complex Resection - A Systems Medicine Approach) by grant number 436883643 and by grant number 465194077 (Priority Programme SPP 2311, Subproject SimLivA).


# Software using libsbgnpy
* [Mimoza](http://mimoza.bordeaux.inria.fr/) takes a model in SBML format and visualizes it in several formats (downloadable as a COMBINE archive).

# Python Language Bindings
The python language bindings were created from the XML schema using generateDS and than adapted to include GlyphClasses and ArcClasses.
```bash
generateDS.py -o "libsbgn.py" -s "libsbgnSubs.py" SBGN.xsd
```

The necessary constraints for GlyphClasses, ArcClasses and Languages were added and some utility functions created.

© 2016-2025 Matthias König
