"""
SBOTerm to SBGN mapping.

Cleanup based on initial mapping provided by Augustin.
"""

import os
import re
from collections import defaultdict


def _clean_line(line):
    """
    Parse the sbo and sbgn from a single line
    :param line:
    :return:
    """
    tokens = [item.strip() for item in line.split("!")]
    sbo = tokens[0].split(" ")[1]
    sbgn = tokens[1].replace(".", "")
    return sbo, sbgn


def _is_sbo(sbo_term):
    """Check is sbo_term is really a SBO term."""
    res = re.search("^SBO:\d{7}$", sbo_term)
    return res is not None


def read_sbo2sbgn(infile):
    """
    Read the initial mapping
    :param infile:
    :return:
    """
    sbo2sbgn = defaultdict(set)
    with open(infile) as f_in:
        for line in f_in:
            sbo, sbgn = _clean_line(line)
            sbo2sbgn[sbo].add(sbgn)
    return sbo2sbgn


def write_sbo2sbgn(outfile, sbo2sbgn):
    """
    Write the sorted entries
    """
    with open(outfile, "w") as f_out:
        for sbo in sorted(sbo2sbgn.keys()):
            sbgn_set = sorted(sbo2sbgn[sbo])
            if not _is_sbo(sbo):
                print("Not SBO:", sbo, sbgn_set)
            else:
                # print(sbo, ':', sbgn_set)
                f_out.write("{}\t{}{}".format(sbo, sbgn_set, os.linesep))


if __name__ == "__main__":
    """
    Cleanup of mapping and writing to file.
    """
    dir = os.path.dirname(os.path.abspath(__file__))
    infile = os.path.join(dir, "sbgn_sbo_mapping.txt")
    outfile = os.path.join(dir, "sbo_sbgn_map.txt")

    sbo2sbgn = read_sbo2sbgn(infile)
    print(sbo2sbgn)
    write_sbo2sbgn(outfile, sbo2sbgn)
