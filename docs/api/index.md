# API reference

The API reference is generated from the docstrings of the package.

## The SBGN bindings

The python bindings of the SBGN-ML schemas, generated with [xsdata](https://github.com/tefra/xsdata), see [SBGN maps](../maps.md). The classes mirror the schemas, so the SBGN specifications are the reference for what an element means.

| module | description |
| --- | --- |
| [sbgn](sbgn.md) | maps, glyphs, arcs and their classes |
| [render](render.md) | colors, gradients and styles of a map |

## Working with SBGN documents

| module | description |
| --- | --- |
| [io](io.md) | reading and writing of SBGN documents |
| [specification](specification.md) | versions and vocabularies of the SBGN specifications, the checks beyond the schema |
| [validator](validator.md) | validation against the schema and the SBGN specifications |
| [image](image.md) | rendering of a map as an image |

## Output of the package

| module | description |
| --- | --- |
| [console](console.md) | shared rich console for scripts and examples |
| [log](log.md) | logging of the package |
