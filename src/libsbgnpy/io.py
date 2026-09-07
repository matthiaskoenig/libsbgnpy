"""Reading and writing of SBGN documents.

The functions in this module are the entry points of the package: an SBGN
document is read into the [`Sbgn`][libsbgnpy.sbgn.Sbgn] object tree of
`libsbgnpy.sbgn` and serialized back to SBGN-ML with
[xsdata](https://github.com/tefra/xsdata).

```python
from pathlib import Path

from libsbgnpy import read_sbgn_from_file, write_sbgn_to_file

sbgn = read_sbgn_from_file(Path("map.sbgn"))
write_sbgn_to_file(sbgn, Path("map_copy.sbgn"))
```
"""

import copy
import dataclasses
import logging
from pathlib import Path

from lxml import etree
from xsdata.exceptions import ParserError
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.models.generics import AnyElement
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from libsbgnpy.render import RenderInformation
from libsbgnpy.sbgn import Sbgn, Sbgnbase

logger = logging.getLogger(__name__)

#: namespace of the SBGN-ML version the bindings were generated from
SBGN_NAMESPACE = "http://sbgn.org/libsbgn/0.3"

#: namespace of the render extension, see `libsbgnpy.render`
RENDER_NAMESPACE = "http://www.sbml.org/sbml/level3/version1/render/version1"

#: earlier SBGN-ML namespaces, read by upconverting them to `SBGN_NAMESPACE`
SBGN_NAMESPACES_OLD = (
    "http://sbgn.org/libsbgn/0.1",
    "http://sbgn.org/libsbgn/0.2",
)


def upconvert(xml_str: str) -> str:
    """Replace an SBGN-ML 0.1 or 0.2 namespace with the 0.3 namespace.

    The bindings are generated from the SBGN-ML 0.3 schema, the earlier
    versions are read by upconverting the document.

    Args:
        xml_str: SBGN-ML document

    Returns:
        The document in the `SBGN_NAMESPACE`.
    """
    for namespace in SBGN_NAMESPACES_OLD:
        xml_str = xml_str.replace(namespace, SBGN_NAMESPACE)
    return xml_str


def read_sbgn_from_file(f: Path) -> Sbgn:
    """Read an SBGN document from a file.

    The document is not validated against the schema, see
    [`validate_xsd`][libsbgnpy.validator.validate_xsd]. SBGN-ML 0.1 and 0.2
    documents are upconverted while reading.

    Args:
        f: path of the SBGN file

    Returns:
        The SBGN document.

    Raises:
        OSError: if the file cannot be read
        xsdata.exceptions.ParserError: if the content is no valid SBGN-ML
    """
    with open(f, encoding="utf-8") as f_in:
        xml_str = f_in.read()

    try:
        return read_sbgn_from_string(xml_str)
    except ParserError:
        logger.error("SBGN file could not be parsed: '%s'", f)
        raise


def read_sbgn_from_string(xml_str: str) -> Sbgn:
    """Read an SBGN document from a string.

    Args:
        xml_str: SBGN-ML document

    Returns:
        The SBGN document.

    Raises:
        xsdata.exceptions.ParserError: if the content is no valid SBGN-ML
    """
    parser = XmlParser()
    return parser.from_string(upconvert(xml_str), Sbgn)


def write_sbgn_to_file(sbgn: Sbgn, f: Path) -> None:
    """Write an SBGN document to a file.

    Args:
        sbgn: SBGN document
        f: path of the file to write

    Raises:
        OSError: if the file cannot be written
    """
    with open(f, "w", encoding="utf-8") as f_out:
        f_out.write(write_sbgn_to_string(sbgn))


def write_sbgn_to_string(sbgn: Sbgn) -> str:
    """Serialize an SBGN document to an SBGN-ML string.

    The raw XML of the `notes` and `extension` elements is converted into
    element trees first, see `element_from_string`, so that it is written as
    markup instead of as escaped text.

    Args:
        sbgn: SBGN document

    Returns:
        The SBGN-ML document, indented with two spaces.
    """
    sbgn = _with_parsed_raw_xml(sbgn)
    serializer = XmlSerializer(
        context=XmlContext(), config=SerializerConfig(indent="  ")
    )
    return serializer.render(sbgn, ns_map={None: SBGN_NAMESPACE})


def read_render_from_string(xml_str: str) -> RenderInformation:
    """Read render information from a string.

    Render information is stored in the `extension` of an SBGN element, see
    `libsbgnpy.render`.

    Args:
        xml_str: `renderInformation` document

    Returns:
        The render information.

    Raises:
        xsdata.exceptions.ParserError: if the content is no render information
    """
    parser = XmlParser(
        context=XmlContext(),
        config=ParserConfig(
            fail_on_converter_warnings=False,
            fail_on_unknown_attributes=True,
            fail_on_unknown_properties=True,
        ),
    )
    return parser.from_string(xml_str, RenderInformation)


def write_render_to_string(render_info: RenderInformation) -> str:
    """Serialize render information to a string.

    The result is written without an XML declaration and without a namespace
    prefix, so that it can be stored in the `extension` of an SBGN element.

    Args:
        render_info: render information

    Returns:
        The `renderInformation` document.
    """
    serializer = XmlSerializer(
        context=XmlContext(),
        config=SerializerConfig(indent="  ", xml_declaration=False),
    )
    return serializer.render(render_info, ns_map={None: RENDER_NAMESPACE})


def element_to_string(element: object) -> str:
    """Serialize the raw XML of a `notes` or `extension` entry.

    The content of `notes` and `extension` is arbitrary XML. It is set as a
    string, but read back as an
    [`AnyElement`](https://xsdata.readthedocs.io/en/latest/api/models/) tree,
    so this function turns such an entry back into XML.

    Args:
        element: entry of `Sbgnbase.Notes` or `Sbgnbase.Extension`

    Returns:
        The XML of the entry.

    Raises:
        TypeError: if the entry is neither a string nor an element tree
        ValueError: if the element tree carries no element name

    Examples:
        >>> from libsbgnpy import element_to_string, read_sbgn_from_file
        >>> sbgn = read_sbgn_from_file(f)  # doctest: +SKIP
        >>> notes = sbgn.map[0].glyph[0].notes  # doctest: +SKIP
        >>> element_to_string(notes.w3_org_1999_xhtml_element[0])  # doctest: +SKIP
        '<html:body xmlns:html="http://www.w3.org/1999/xhtml">note</html:body>'
    """
    if isinstance(element, str):
        return element
    if not isinstance(element, AnyElement):
        raise TypeError(
            f"A `notes` or `extension` entry is a string or an `AnyElement`, "
            f"but is '{type(element)}'."
        )

    node = _element_to_node(element)
    etree.indent(node, space="  ")
    return etree.tostring(node, encoding="unicode")


def element_from_string(xml_str: str) -> AnyElement:
    """Parse raw XML into an entry of a `notes` or `extension` element.

    Args:
        xml_str: XML of a single element

    Returns:
        The element tree.

    Raises:
        lxml.etree.XMLSyntaxError: if the string is no well-formed XML
    """
    return _node_to_element(etree.fromstring(xml_str.encode("utf-8")))


def _element_to_node(element: AnyElement) -> etree._Element:
    """Convert an `AnyElement` tree into an lxml element tree.

    Args:
        element: element to convert

    Returns:
        The lxml element.

    Raises:
        ValueError: if the element carries no name, i.e., it is text only
    """
    if element.qname is None:
        raise ValueError(f"The element carries no name (qname): {element}")

    node = etree.Element(element.qname, attrib=dict(element.attributes))
    node.text = element.text
    for child in element.children:
        if isinstance(child, AnyElement):
            node.append(_element_to_node(child))
    return node


def _node_to_element(node: etree._Element) -> AnyElement:
    """Convert an lxml element tree into an `AnyElement` tree.

    Comments and processing instructions are dropped, they have no
    representation in the bindings.

    Args:
        node: lxml element to convert

    Returns:
        The element tree.
    """
    return AnyElement(
        qname=node.tag,
        text=node.text,
        children=[
            _node_to_element(child) for child in node if isinstance(child.tag, str)
        ],
        attributes=dict(node.attrib),
    )


def _with_parsed_raw_xml(sbgn: Sbgn) -> Sbgn:
    """Copy an SBGN document with the raw XML of its elements parsed.

    The `notes` and `extension` elements hold arbitrary XML, which is set as a
    string but has to be serialized as markup. The document is copied, so that
    the document of the caller is left as it is.

    Args:
        sbgn: SBGN document

    Returns:
        A copy of the document, with every raw XML string parsed.
    """
    sbgn = copy.deepcopy(sbgn)
    _parse_raw_xml(sbgn)
    return sbgn


def _parse_raw_xml(obj: object) -> None:
    """Parse the raw XML of the `notes` and `extension` elements of a subtree.

    Args:
        obj: object of the SBGN document to walk
    """
    if isinstance(obj, Sbgnbase.Notes):
        obj.w3_org_1999_xhtml_element = [
            element_from_string(element) if isinstance(element, str) else element
            for element in obj.w3_org_1999_xhtml_element
        ]
    elif isinstance(obj, Sbgnbase.Extension):
        obj.any_element = [
            element_from_string(element) if isinstance(element, str) else element
            for element in obj.any_element
        ]
    elif isinstance(obj, list):
        for item in obj:
            _parse_raw_xml(item)
    elif dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        for field in dataclasses.fields(obj):
            _parse_raw_xml(getattr(obj, field.name))


def read_render_from_extension(
    extension: Sbgnbase.Extension | None,
) -> RenderInformation | None:
    """Read the render information stored in an extension.

    Render information is stored as raw XML in the `extension` of an SBGN
    element, see `libsbgnpy.render`; the first `renderInformation` entry of the
    extension is returned.

    Args:
        extension: extension of an SBGN element, e.g., of a map

    Returns:
        The render information, or `None` if the extension contains none.

    Raises:
        xsdata.exceptions.ParserError: if the entry is no render information
    """
    if extension is None:
        return None

    for element in extension.any_element:
        xml_str = element_to_string(element)
        if "renderInformation" in xml_str:
            return read_render_from_string(xml_str)
    return None
