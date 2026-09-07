# Render information

SBGN says what a map means, not what it looks like. Colors, line widths and fonts are therefore not part of the SBGN-ML schema: they are stored as an extension of the map, using the vocabulary of the [SBML render extension](https://sbml.org/documents/specifications/level-3/version-1/render/), see the [SBGN-ML rendering](https://github.com/sbgn/sbgn/wiki/SBGN-ML_Rendering).

`libsbgnpy.render` holds the python bindings of that vocabulary.

## The structure

A `RenderInformation` object has three parts:

- **`ListOfColorDefinitions`** — named colors, i.e., a `ColorDefinition` maps an id to a hex value such as `#ff9900` or `#1f77b4bb` with an alpha channel,
- **`ListOfGradientDefinitions`** — named gradients, i.e., a `LinearGradient` with its stops,
- **`ListOfStyles`** — a `Style` applies a `G` to the glyphs and arcs it lists in `id_list`; the `G` carries `stroke`, `stroke_width`, `fill` and the font attributes, and refers to the colors and gradients by their id.

```python
from libsbgnpy import (
    ColorDefinition,
    G,
    ListOfColorDefinitions,
    ListOfGradientDefinitions,
    ListOfStyles,
    RenderInformation,
    Style,
)

render_info = RenderInformation(
    id="example",
    program_name="libsbgnpy",
    program_version="1.0.0",
    list_of_color_definitions=ListOfColorDefinitions(
        color_definition=[
            ColorDefinition(id="grey", value="#969696"),
            ColorDefinition(id="orange", value="#ff9900"),
        ]
    ),
    list_of_gradient_definitions=ListOfGradientDefinitions(),
    list_of_styles=ListOfStyles(
        style=[
            Style(
                id_list="glyph1 glyph2",
                g=G(stroke="grey", stroke_width=5, fill="orange"),
            ),
        ]
    ),
)
```

`id_list` is a space separated list of the ids of the glyphs and arcs the style applies to.

## Storing it in a map

The render information is serialized and stored as an extension of the map:

```python
from libsbgnpy import Sbgnbase, write_render_to_string

map.extension = Sbgnbase.Extension(any_element=[write_render_to_string(render_info)])
```

`write_render_to_string` writes the document without an XML declaration and without a namespace prefix, which is what belongs into an extension.

## Reading it back

`read_render_from_extension` finds the `renderInformation` in an extension and parses it:

```python
from pathlib import Path

from libsbgnpy import read_render_from_extension, read_sbgn_from_file

sbgn = read_sbgn_from_file(Path("map.sbgn"))
render_info = read_render_from_extension(sbgn.map[0].extension)

if render_info is not None:
    for color in render_info.list_of_color_definitions.color_definition:
        print(color.id, color.value)
        # grey #969696
```

It returns `None` if the map carries no render information. To parse a `renderInformation` document which is not stored in an extension use `read_render_from_string`.

## Examples

| example | what it shows |
| --- | --- |
| [`render.py`](https://github.com/matthiaskoenig/libsbgnpy/blob/develop/examples/render.py) | write and read render information |
| [`ethanol.py`](https://github.com/matthiaskoenig/libsbgnpy/blob/develop/examples/ethanol.py) | color a map and render it as an image |
