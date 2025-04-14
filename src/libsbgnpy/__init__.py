__version__ = "0.4.0"
__author__ = "Matthias König"

from pathlib import Path
from .console import console

from .render import (
    ColorDefinition,
    G,
    LinearGradient,
    ListOfColorDefinitions,
    ListOfGradientDefinitions,
    ListOfStyles,
    RenderInformation,
    Style,
)
from .sbgn import (
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

from .io import (
    read_sbgn_from_file,
    write_sbgn_to_file,
    write_sbgn_to_string,
    read_render_from_string,
    write_render_to_string,
)

from .image import (
    render_sbgn,
)
from .validator import validate_xsd

sbgn_examples_dir = Path(__file__).parent / "examples" / "sbgn"

__all__ = [
    "ColorDefinition",
    "G",
    "LinearGradient",
    "ListOfColorDefinitions",
    "ListOfGradientDefinitions",
    "ListOfStyles",
    "RenderInformation",
    "Style",
    "Sbgnbase",
    "Arc",
    "ArcClass",
    "Arcgroup",
    "ArcgroupClass",
    "Bbox",
    "EntityName",
    "Glyph",
    "GlyphClass",
    "GlyphOrientation",
    "Label",
    "Map",
    "MapLanguage",
    "MapVersion",
    "Point",
    "Port",
    "Sbgn",
    "read_sbgn_from_file",
    "write_sbgn_to_string",
    "write_sbgn_to_file",
    "read_render_from_string",
    "write_render_to_string",
    "render_sbgn",
    "validate_xsd",
    "console",
    "sbgn_examples_dir",
]
