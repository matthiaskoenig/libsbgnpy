![libsbgnpy logo](https://github.com/matthiaskoenig/libsbgnpy/raw/develop/docs/images/libsbgnpy.png)

# libsbgnpy: Python library for SBGN

[![GitHub Actions CI/CD Status](https://github.com/matthiaskoenig/libsbgnpy/workflows/CI-CD/badge.svg)](https://github.com/matthiaskoenig/libsbgnpy/actions/workflows/main.yml)
[![Version](https://img.shields.io/pypi/v/libsbgnpy.svg)](https://pypi.org/project/libsbgnpy/)
[![Python Versions](https://img.shields.io/pypi/pyversions/libsbgnpy.svg)](https://pypi.org/project/libsbgnpy/)
[![MIT License](https://img.shields.io/pypi/l/libsbgnpy.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.597155.svg)](https://doi.org/10.5281/zenodo.597155)

Python library to work with the Systems Biology Graphical Notation ([SBGN](http://sbgn.github.io/sbgn/)). This library is based on the SBGN XML schema and supports reading,
writing and validation of SBGN files.

The initial library was generated using [xsdata](https://github.com/tefra/xsdata). Additional utility functions for reading, writing, and rendering SBGN documents are provided.

Documentation with examples is available at https://matthiaskoenig.github.io/libsbgnpy/.

```python
    map = Map(
        id="ethanol_example",
        language=MapLanguage.PROCESS_DESCRIPTION,
        bbox=Bbox(x=0, y=0, w=363, h=253),
    )
    # add map to new sbgn
    sbgn = Sbgn(map=[map])

    # create glyphs and add to map
    map.glyph.extend(
        [
            Glyph(
                class_value=GlyphClass.SIMPLE_CHEMICAL,
                id="ethanol",
                label=Label(text="Ethanol"),
                bbox=Bbox(x=40, y=120, w=60, h=60),
            ),
            Glyph(
                class_value=GlyphClass.SIMPLE_CHEMICAL,
                id="ethanal",
                label=Label(text="Ethanal"),
                bbox=Bbox(x=220, y=110, w=60, h=60),
            ),
            Glyph(
                class_value=GlyphClass.MACROMOLECULE,
                id="adh1",
                label=Label(text="ADH1"),
                bbox=Bbox(x=106, y=20, w=108, h=60),
            ),

            ...

            # glyph with ports (process)
            Glyph(
                class_value=GlyphClass.PROCESS,
                id="pn1",
                orientation=GlyphOrientation.HORIZONTAL,
                bbox=Bbox(x=148, y=168, w=24, h=24),
                port=[
                    Port(x=136, y=180, id="pn1.1"),
                    Port(x=184, y=180, id="pn1.2"),
                ],
            ),
        ]
    )
    write_sbgn_to_file(sbgn, f"{prefix}_glyphs.sbgn")
    render_sbgn(sbgn, f"{prefix}_glyphs.png")
```

![Example](./docs/images/ethanol_example.png)

# How to cite
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.597155.svg)](https://doi.org/10.5281/zenodo.597155)

# Installation
`libsbgnpy` is available from [pypi](https://pypi.python.org/pypi/libsbgnpy)
```bash
pip install libsbgnpy
```

# License
- Source Code: [MIT](https://opensource.org/license/MIT)
- Documentation: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

# Funding
Matthias König (MK) was supported by the Federal Ministry of Education and Research (BMBF, Germany) within the research network Systems Medicine of the Liver (LiSyM, grant number 031L0054). MK is supported by the Federal Ministry of Education and Research (BMBF, Germany) within ATLAS by grant number 031L0304B and by the German Research Foundation (DFG) within the Research Unit Program FOR 5151 QuaLiPerF (Quantifying Liver Perfusion-Function Relationship in Complex Resection - A Systems Medicine Approach) by grant number 436883643 and by grant number 465194077 (Priority Programme SPP 2311, Subproject SimLivA).

© 2016-2026 Matthias König
