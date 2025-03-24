"""
Helper functions to work with SBGN.
"""

from pathlib import Path
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from libsbgnpy import Sbgn, MapLanguage
import libsbgnpy.sbgn as libsbgn


def read_sbgn_from_file(f: Path) -> Sbgn:
    """Read an sbgn file (without validating against the schema).

    :param silence: display no information
    :param f: file to read
    :return: parsed SBGN
    :rtype:
    """
    with open(f, "r") as f_in:
        xml_str = f_in.read()
        # upconverting for fixing reading
        xml_str = xml_str.replace(
            "http://sbgn.org/libsbgn/0.1", "http://sbgn.org/libsbgn/0.3"
        )
        xml_str = xml_str.replace(
            "http://sbgn.org/libsbgn/0.2", "http://sbgn.org/libsbgn/0.3"
        )

    parser = XmlParser()
    sbgn = parser.from_string(xml_str, Sbgn)
    # sbgn = parser.parse(f, Sbgn)
    return sbgn


def write_sbgn_to_file(sbgn: Sbgn, f: Path) -> None:
    """Write sbgn object to file.

    :param sbgn: SBGN object
    :param f: file to write
    :return: None
    """
    config = SerializerConfig(indent="  ", pretty_print=True)
    context = XmlContext()
    serializer = XmlSerializer(context=context, config=config)
    with open(f, "w") as f:
        serializer.write(f, sbgn, ns_map={None: "http://sbgn.org/libsbgn/0.3"})


def write_sbgn_to_string(sbgn: Sbgn) -> str:
    """Write SBGN to string.

    :param sbgn: sbgn object
    :return: SBGN xml string
    """
    config = SerializerConfig(indent="  ", pretty_print=True)
    context = XmlContext()
    serializer = XmlSerializer(context=context, config=config)
    return serializer.render(sbgn, ns_map={None: "http://sbgn.org/libsbgn/0.3"})


def get_version(f: Path) -> int:
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


def get_language(f: Path) -> str:
    """SBGN language of the map.
    Returns a Language value.

    :param f:
    :return:
    """
    sbgn: Sbgn = read_sbgn_from_file(f)
    map: list[libsbgn.Map] = sbgn.map
    language: MapLanguage = map[0].language
    return language.value


def print_bbox(b: libsbgn.Bbox) -> None:
    """Print bounding box representation.

    :param b:
    :type b:
    :return:
    :rtype:
    """
    print("x, y, w, h : ", b.x, b.y, b.w, b.h)
