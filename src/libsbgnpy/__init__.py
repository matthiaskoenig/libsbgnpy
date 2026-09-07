"""libsbgnpy - python utilities for working with SBGN.

The package provides the python bindings of the [SBGN-ML](https://sbgn.github.io/)
schema, generated with [xsdata](https://github.com/tefra/xsdata), together with
the functions to read, write, validate and render SBGN documents.
"""

import logging

from libsbgnpy.image import render_sbgn
from libsbgnpy.io import (
    element_from_string,
    element_to_string,
    read_render_from_extension,
    read_render_from_string,
    read_sbgn_from_file,
    read_sbgn_from_string,
    write_render_to_string,
    write_sbgn_to_file,
    write_sbgn_to_string,
)
from libsbgnpy.render import (
    ColorDefinition,
    G,
    LinearGradient,
    ListOfColorDefinitions,
    ListOfGradientDefinitions,
    ListOfStyles,
    RenderInformation,
    Style,
)
from libsbgnpy.sbgn import (
    Arc,
    ArcClass,
    Arcgroup,
    ArcgroupClass,
    Bbox,
    EntityName,
    Glyph,
    GlyphClass,
    GlyphOrientation,
    Label,
    Map,
    MapLanguage,
    MapVersion,
    Point,
    Port,
    Sbgn,
    Sbgnbase,
)
from libsbgnpy.validator import validate_xsd

__author__ = "Matthias Koenig"
__version__ = "0.5.2"

# the package does not configure logging, see `libsbgnpy.log`
logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = [
    "Arc",
    "ArcClass",
    "Arcgroup",
    "ArcgroupClass",
    "Bbox",
    "ColorDefinition",
    "EntityName",
    "G",
    "Glyph",
    "GlyphClass",
    "GlyphOrientation",
    "Label",
    "LinearGradient",
    "ListOfColorDefinitions",
    "ListOfGradientDefinitions",
    "ListOfStyles",
    "Map",
    "MapLanguage",
    "MapVersion",
    "Point",
    "Port",
    "RenderInformation",
    "Sbgn",
    "Sbgnbase",
    "Style",
    "element_from_string",
    "element_to_string",
    "read_render_from_extension",
    "read_render_from_string",
    "read_sbgn_from_file",
    "read_sbgn_from_string",
    "render_sbgn",
    "validate_xsd",
    "write_render_to_string",
    "write_sbgn_to_file",
    "write_sbgn_to_string",
]
