__version__ = "0.3.3"

from pathlib import Path

sbgn_examples_dir = Path(__file__).parent / "examples" / "sbgn"

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
    "sbgn_examples_dir",
]


# __all__ = [
#     "Notes",
#     "Extension",
#     "Language",
#     "sbgn_examples_dir",
# ]
