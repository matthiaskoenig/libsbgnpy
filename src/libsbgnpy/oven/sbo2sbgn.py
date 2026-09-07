"""Mapping of SBO terms to SBGN glyphs.

Work in progress towards the conversion of SBML to SBGN, see
<https://github.com/matthiaskoenig/libsbgnpy/issues/52>. The mapping is
extracted from the LaTeX sources of the SBGN specifications
(`sbgn_sbo_mapping.txt`), which annotate every glyph with its SBO terms, and
written as a sorted table of SBO term to glyph names (`sbo_sbgn_map.txt`).

Cleanup based on the initial mapping provided by Augustin Luna.

Regenerate the table with

```bash
python -m libsbgnpy.oven.sbo2sbgn
```
"""

import re
from collections import defaultdict
from pathlib import Path

#: SBO terms of the glyphs, extracted from the specification sources
MAPPING_FILE = Path(__file__).parent / "sbgn_sbo_mapping.txt"

#: the cleaned up mapping, written by `write_sbo2sbgn`
MAP_FILE = Path(__file__).parent / "sbo_sbgn_map.txt"


def _clean_line(line: str) -> tuple[str, str]:
    r"""Parse the SBO term and the glyph name from a single line.

    Args:
        line: line of the mapping file, e.g.,
            `\glyphSboTerm SBO:0000247 ! simple chemical.`

    Returns:
        The SBO term and the glyph name.
    """
    tokens = [item.strip() for item in line.split("!")]
    sbo = tokens[0].split(" ")[1]
    sbgn = tokens[1].replace(".", "")
    return sbo, sbgn


def _is_sbo(sbo_term: str) -> bool:
    """Check that the term is an SBO term.

    Args:
        sbo_term: term to check

    Returns:
        `True` if the term is of the form `SBO:0000247`.
    """
    return re.search(r"^SBO:\d{7}$", sbo_term) is not None


def read_sbo2sbgn(filename: Path) -> dict[str, set[str]]:
    """Read the mapping of SBO terms to glyph names.

    Args:
        filename: mapping extracted from the specification sources

    Returns:
        The glyph names for every SBO term.
    """
    sbo2sbgn: dict[str, set[str]] = defaultdict(set)
    with open(filename, encoding="utf-8") as f_in:
        for line in f_in:
            sbo, sbgn = _clean_line(line)
            sbo2sbgn[sbo].add(sbgn)
    return sbo2sbgn


def write_sbo2sbgn(outfile: Path, sbo2sbgn: dict[str, set[str]]) -> None:
    """Write the mapping sorted by SBO term.

    Entries which are no SBO term are skipped.

    Args:
        outfile: file to write
        sbo2sbgn: the glyph names for every SBO term
    """
    with open(outfile, "w", encoding="utf-8") as f_out:
        for sbo in sorted(sbo2sbgn):
            if _is_sbo(sbo):
                f_out.write(f"{sbo}\t{sorted(sbo2sbgn[sbo])}\n")


if __name__ == "__main__":
    write_sbo2sbgn(MAP_FILE, read_sbo2sbgn(MAPPING_FILE))
