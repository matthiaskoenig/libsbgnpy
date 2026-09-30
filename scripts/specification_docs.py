"""Write the tables of `docs/specifications.md` from `libsbgnpy.specification`.

The versions of the specifications and the glyph and arc classes of every
language are data of `libsbgnpy.specification`; the tables of the page are
generated from them, so the documentation and the checks cannot drift apart.
Every table is written between the markers
`<!-- specification:<name> -->` and `<!-- /specification:<name> -->`.

```bash
uv run python scripts/specification_docs.py
```

`--check` fails if the page differs from freshly generated tables,
`tests/test_specification_docs.py` runs it.
"""

import argparse
import re
import sys
from collections.abc import Callable
from pathlib import Path

from libsbgnpy import ArcClass, GlyphClass, MapLanguage
from libsbgnpy.specification import (
    ARC_CLASSES,
    DEPRECATED_GLYPH_CLASSES,
    GLYPH_CLASSES,
    LANGUAGE_ABBREVIATIONS,
    LATEST,
    SPECIFICATIONS,
)

REPO_DIR: Path = Path(__file__).parent.parent
PAGE: Path = REPO_DIR / "docs" / "specifications.md"

#: the common prefix of the version identifiers, stated once on the page
IDENTIFIER_PREFIX = "http://identifiers.org/combine.specifications/"

LANGUAGES: tuple[MapLanguage, ...] = (
    MapLanguage.PROCESS_DESCRIPTION,
    MapLanguage.ENTITY_RELATIONSHIP,
    MapLanguage.ACTIVITY_FLOW,
)


def versions_table() -> str:
    """Create the table of the version identifiers of the maps.

    Returns:
        The markdown table.
    """
    rows = [
        "| specification | year | publication | identifier |",
        "| --- | --- | --- | --- |",
    ]
    for version, spec in SPECIFICATIONS.items():
        name = f"**{spec.name}**" if LATEST[spec.language] == version else spec.name
        year = str(spec.year) if spec.year else ""
        doi = f"[{spec.doi}](https://doi.org/{spec.doi})" if spec.doi else ""
        identifier = version.value.removeprefix(IDENTIFIER_PREFIX)
        rows.append(f"| {name} | {year} | {doi} | `{identifier}` |")
    return "\n".join(rows)


def _class_table(
    classes: dict[MapLanguage, frozenset], values: list[GlyphClass] | list[ArcClass]
) -> str:
    """Create a table of classes against the languages.

    Args:
        classes: the classes of every language.
        values: the classes in the order of the schema.

    Returns:
        The markdown table.
    """
    header = " | ".join(LANGUAGE_ABBREVIATIONS[language] for language in LANGUAGES)
    rows = [f"| class | {header} |", "| --- |" + " :---: |" * len(LANGUAGES)]
    for value in values:
        cells = []
        for language in LANGUAGES:
            if value in DEPRECATED_GLYPH_CLASSES.get(language, frozenset()):
                cells.append("deprecated")
            elif value in classes[language]:
                cells.append("✓")
            else:
                cells.append("")
        rows.append(f"| `{value.value}` | " + " | ".join(cells) + " |")
    return "\n".join(rows)


def glyphs_table() -> str:
    """Create the table of the glyph classes of every language.

    Returns:
        The markdown table.
    """
    return _class_table(dict(GLYPH_CLASSES), list(GlyphClass))


def arcs_table() -> str:
    """Create the table of the arc classes of every language.

    Returns:
        The markdown table.
    """
    return _class_table(dict(ARC_CLASSES), list(ArcClass))


TABLES: dict[str, Callable[[], str]] = {
    "versions": versions_table,
    "glyphs": glyphs_table,
    "arcs": arcs_table,
}


def render(page: str) -> str:
    """Replace the tables of the page with freshly generated ones.

    Args:
        page: the markdown of the page.

    Returns:
        The markdown with the generated tables.

    Raises:
        ValueError: if the markers of a table are missing.
    """
    for name, table in TABLES.items():
        start = f"<!-- specification:{name} -->"
        end = f"<!-- /specification:{name} -->"
        pattern = re.compile(re.escape(start) + r"\n.*?" + re.escape(end), re.DOTALL)
        if not pattern.search(page):
            raise ValueError(f"the markers of the table '{name}' are missing")
        replacement = f"{start}\n{table()}\n{end}"
        page = pattern.sub(lambda _, text=replacement: text, page)
    return page


def main() -> int:
    """Write the tables, or check them with `--check`.

    Returns:
        The exit code.
    """
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if the page differs from freshly generated tables",
    )
    args = parser.parse_args()
    page = PAGE.read_text(encoding="utf-8")
    rendered = render(page)
    if args.check:
        if rendered == page:
            return 0
        print("tables are outdated, run `python scripts/specification_docs.py`")
        return 1
    PAGE.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
