"""
SBOTerm to SBGN mapping.

Cleanup based on initial mapping provided by Augustin.
"""

import re
from collections import defaultdict
from pathlib import Path
from typing import Tuple


def _clean_line(line: str) -> Tuple[str, str]:
    """Parse sbo and sbgn from single line."""
    tokens = [item.strip() for item in line.split("!")]
    sbo = tokens[0].split(" ")[1]
    sbgn = tokens[1].replace(".", "")
    return sbo, sbgn


def _is_sbo(sbo_term: str) -> bool:
    """Check is sbo_term is really a SBO term."""
    res = re.search(r"^SBO:\d{7}$", sbo_term)
    return res is not None


def read_sbo2sbgn(filename: Path) -> dict[str, set[str]]:
    """Read the initial mapping."""
    sbo2sbgn: dict[str, set(str)] = defaultdict(set)
    with open(filename, "r") as f_in:
        for line in f_in:
            sbo, sbgn = _clean_line(line)
            sbo2sbgn[sbo].add(sbgn)
    return sbo2sbgn


def write_sbo2sbgn(outfile: Path, sbo2sbgn: dict[str, set[str]]) -> None:
    """Write the sorted entries."""

    with open(outfile, "w") as f_out:
        for sbo in sorted(sbo2sbgn.keys()):
            sbgn_set = sorted(sbo2sbgn[sbo])
            if not _is_sbo(sbo):
                print("Not SBO:", sbo, sbgn_set)
            else:
                f_out.write(f"{sbo}\t{sbgn_set}\n")


if __name__ == "__main__":
    """
    Cleanup of mapping and writing to file.
    """
    infile = Path(__file__).parent / "sbgn_sbo_mapping.txt"
    outfile = Path(__file__).parent / "sbo_sbgn_map.txt"

    sbo2sbgn = read_sbo2sbgn(infile)
    print(sbo2sbgn)
    write_sbo2sbgn(outfile, sbo2sbgn)
