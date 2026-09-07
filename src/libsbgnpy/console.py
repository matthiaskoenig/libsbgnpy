"""Shared rich console.

The console is used for the output of scripts and examples; library code logs
instead of printing, see `libsbgnpy.log`.

```python
from libsbgnpy.console import console

console.print(sbgn)
console.rule("Glyphs", style="white")
```

Importing this module has no side effects on the interpreter. To get rich
representations in an interactive session, install them explicitly with
`rich.pretty.install()`.
"""

from rich.console import Console
from rich.theme import Theme

custom_theme = Theme(
    {
        "success": "green",
        "info": "blue",
        "warning": "orange3",
        "error": "red",
    }
)

console = Console(theme=custom_theme)
