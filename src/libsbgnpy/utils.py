"""
Helper functions to work with SBGN.
"""

import os
import libsbgnpy.libsbgn as libsbgn


def read_from_file(f, silence=True):
    """Read an sbgn file (without validating against the schema).

    :param silence: display no information
    :param f: file to read
    :return: parsed SBGN
    :rtype:
    """
    sbgn = libsbgn.parse(f, silence=silence)
    return sbgn


def write_to_file(sbgn, f):
    """Write sbgn object to file.

    :param sbgn:
    :param f:
    :return:
    """
    sbgn.write_file(f)


def write_to_string(sbgn):
    """Write SBGN to string.
    Returns None if problems.

    :param sbgn: sbgn object
    :return: SBGN xml string
    """
    import tempfile

    f = tempfile.NamedTemporaryFile(suffix=".sbgn", delete=False)
    write_to_file(sbgn, f.name)
    with open(f.name, "rt", encoding="utf-8") as fin:
        sbgn_str = fin.read()
        return sbgn_str

    f.close()
    os.unlink(f.name)
    return None


def get_version(f):
    """SBGN version.

    1: xmlns="http://sbgn.org/libsbgn/0.1
    2: xmlns="http://sbgn.org/libsbgn/0.2
    3: xmlns="http://sbgn.org/libsbgn/0.3

    :param f: file for which version should be found.
    :return: version as an integer, i.e. 1, 2, 3
    """
    import re
    from xml.etree import ElementTree

    tree = ElementTree.parse(f)
    root = tree.getroot()
    tag = root.tag
    m = re.search(r"\d\.\d", tag)
    version = m.group(0)  # full version, i.e. 0.2 or similar
    tokens = version.split(".")
    return int(tokens[-1])


def get_language(f):
    """SBGN language of the map.
    Returns a Language value.

    :param f:
    :return:
    """
    sbgn = read_from_file(f)
    map = sbgn.get_map()
    return map.get_language()


def print_bbox(b):
    """Print bounding box representation.

    :param b:
    :type b:
    :return:
    :rtype:
    """
    print("x, y, w, h : ", b.get_x(), b.get_y(), b.get_w(), b.get_h())
