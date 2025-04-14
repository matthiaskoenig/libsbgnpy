"""
Helper functions to work with SBGN.
"""

import logging
from pathlib import Path

import xsdata.exceptions
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from libsbgnpy import Sbgn, RenderInformation

logger = logging.getLogger(__name__)


def read_sbgn_from_file(f: Path) -> Sbgn:
    """Read an sbgn file (without validating against the schema).

    :param silence: display no information
    :param f: file to read
    :return: parsed SBGN
    :rtype:
    """
    with open(f, "r", encoding="utf-8") as f_in:
        xml_str = f_in.read()
        # upconverting for fixing reading
        xml_str = xml_str.replace(
            "http://sbgn.org/libsbgn/0.1", "http://sbgn.org/libsbgn/0.3"
        )
        xml_str = xml_str.replace(
            "http://sbgn.org/libsbgn/0.2", "http://sbgn.org/libsbgn/0.3"
        )

    parser = XmlParser()
    try:
        sbgn = parser.from_string(xml_str, Sbgn)
    except xsdata.exceptions.ParserError as err:
        logger.error(f"Could not parse SBGN file: '{f}'")
        logger.error(err)
        logger.error(f"\n{xml_str}")

    # sbgn = parser.parse(f, Sbgn)
    return sbgn


def write_sbgn_to_file(sbgn: Sbgn, f: Path) -> None:
    """Write sbgn object to file.

    :param sbgn: SBGN object
    :param f: file to write
    :return: None
    """
    config = SerializerConfig(indent="  ")
    context = XmlContext()
    serializer = XmlSerializer(context=context, config=config)
    with open(f, "w", encoding="utf-8") as f:
        serializer.write(f, sbgn, ns_map={None: "http://sbgn.org/libsbgn/0.3"})


def write_sbgn_to_string(sbgn: Sbgn) -> str:
    """Write SBGN to string.

    :param sbgn: sbgn object
    :return: SBGN xml string
    """
    config = SerializerConfig(indent="  ")
    context = XmlContext()
    serializer = XmlSerializer(context=context, config=config)
    return serializer.render(sbgn, ns_map={None: "http://sbgn.org/libsbgn/0.3"})


def write_render_to_string(render_info: RenderInformation) -> str:
    """Write RenderInformation to string."""
    config = SerializerConfig(indent="  ")
    context = XmlContext()
    serializer = XmlSerializer(context=context, config=config)
    return serializer.render(
        render_info,
        ns_map={
            # None: "http://www.sbml.org/sbml/level3/version1/render/version1"
        },
    )


def read_render_from_string(xml_str: str) -> RenderInformation:
    """Read RenderInformation from string."""
    parser = XmlParser()
    return parser.from_string(xml_str, RenderInformation)
