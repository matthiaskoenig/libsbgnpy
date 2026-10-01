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
import warnings
from pathlib import Path

from lxml import etree
from xsdata.exceptions import ConverterWarning, ParserError
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.models.generics import AnyElement
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata.formats.dataclass.parsers.handlers import LxmlEventHandler
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

#: namespace of the earlier EML render extension, read by upconverting it to
#: `RENDER_NAMESPACE`
RENDER_NAMESPACES_OLD = ("http://projects.eml.org/bcb/sbml/render/level2",)

#: attributes of the EML render extension without counterpart in
#: `RENDER_NAMESPACE`, dropped while upconverting
RENDER_ATTRIBUTES_OLD = {"linearGradient": ("z1", "z2", "spreadMethod")}


def _xml_parser(encoding: str | None = None) -> etree.XMLParser:
    """Create the lxml parser for untrusted documents.

    Entities are not resolved, nothing is loaded from the network and the
    limits of libxml2 against huge documents stay in place, so neither external
    entities (XXE) nor entity expansion are an issue. Comments and processing
    instructions are dropped, they have no representation in the bindings.

    Args:
        encoding: encoding which overrides the one declared by the document,
            used for documents which are already decoded into a string

    Returns:
        The parser.
    """
    return etree.XMLParser(
        encoding=encoding,
        resolve_entities=False,
        no_network=True,
        huge_tree=False,
        remove_comments=True,
        remove_pis=True,
    )


def parse_xml(source: str | bytes) -> etree._Element:
    """Parse an untrusted XML document.

    Entities are not resolved, nothing is loaded from the network, comments,
    processing instructions and unresolved entity references are dropped. A
    string is already decoded, so an encoding declared in it is ignored; bytes
    are decoded with the declared encoding, UTF-8 by default.

    Args:
        source: XML document

    Returns:
        The root element.

    Raises:
        lxml.etree.XMLSyntaxError: if the document is no well-formed XML
    """
    if isinstance(source, str):
        root = etree.fromstring(source.encode("utf-8"), _xml_parser("utf-8"))
    else:
        root = etree.fromstring(source, _xml_parser())
    etree.strip_elements(root, etree.Entity, with_tail=False)
    return root


def _move_namespaces(
    node: etree._Element, old: tuple[str, ...], new: str
) -> etree._Element:
    """Copy a tree with its elements and attributes moved into a new namespace.

    Only the names and the namespace declarations change, the prefixes, the
    text, the attribute values, the source lines, comments and processing
    instructions are copied as they are.

    Args:
        node: root of the tree
        old: namespaces to move
        new: namespace they are moved to

    Returns:
        The copy of the tree.
    """

    def moved(name: str) -> str:
        namespace, _, local = name[1:].partition("}")
        if name.startswith("{") and namespace in old:
            return f"{{{new}}}{local}"
        return name

    copy_node = etree.Element(
        moved(etree.QName(node).text),
        nsmap={
            prefix: new if uri in old else uri for prefix, uri in node.nsmap.items()
        },
    )
    # the lines of the source are kept, the validation errors refer to them;
    # lxml allows to set them, types-lxml declares them read-only
    copy_node.sourceline = node.sourceline  # ty: ignore[invalid-assignment]
    for name, value in node.attrib.items():
        copy_node.set(moved(name), value)
    copy_node.text = node.text
    for child in node:
        if isinstance(child.tag, str):
            copy_child = _move_namespaces(child, old, new)
        else:
            copy_child = copy.copy(child)
        copy_child.tail = child.tail
        copy_node.append(copy_child)
    return copy_node


def upconvert_tree(root: etree._Element) -> etree._Element:
    """Move an SBGN-ML 0.1 or 0.2 tree into the 0.3 namespace.

    Args:
        root: root element of an SBGN-ML document, see `parse_xml`

    Returns:
        The tree in the `SBGN_NAMESPACE`, see `upconvert`: a copy for a 0.1 or
        0.2 document, the tree itself otherwise.
    """
    if not any(
        etree.QName(node).namespace in SBGN_NAMESPACES_OLD
        for node in root.iter(etree.Element)
    ):
        return root
    return _move_namespaces(root, SBGN_NAMESPACES_OLD, SBGN_NAMESPACE)


def upconvert(xml_str: str) -> str:
    """Move a document from the SBGN-ML 0.1 or 0.2 into the 0.3 namespace.

    The bindings are generated from the SBGN-ML 0.3 schema, the earlier
    versions are read by upconverting the document. Only the names of the
    elements and attributes are changed, text and attribute values which
    mention a namespace are left as they are.

    Args:
        xml_str: SBGN-ML document

    Returns:
        The document in the `SBGN_NAMESPACE`, without XML declaration.

    Raises:
        lxml.etree.XMLSyntaxError: if the document is no well-formed XML
    """
    return etree.tostring(upconvert_tree(parse_xml(xml_str)), encoding="unicode")


def _read_sbgn(source: str | bytes) -> Sbgn:
    """Parse, upconvert, check and bind an SBGN-ML document.

    Args:
        source: SBGN-ML document, a decoded string or bytes

    Returns:
        The SBGN document.

    Raises:
        xsdata.exceptions.ParserError: if the content is no SBGN-ML
    """
    try:
        root = upconvert_tree(parse_xml(source))
    except etree.XMLSyntaxError as err:
        raise ParserError(str(err)) from err

    expected = f"{{{SBGN_NAMESPACE}}}sbgn"
    if root.tag != expected:
        raise ParserError(
            f"The root element of an SBGN-ML document is '{expected}', "
            f"but is '{root.tag}'."
        )
    with warnings.catch_warnings(record=True) as caught:
        # a value outside of an enumeration is kept as a string, xsdata warns
        warnings.simplefilter("always", ConverterWarning)
        try:
            sbgn = XmlParser(handler=LxmlEventHandler).parse(root, Sbgn)
        except TypeError as err:
            # a required element or attribute is missing, the dataclass rejects it
            raise ParserError(f"The document is no valid SBGN-ML: {err}") from err
    for warning in caught:
        if issubclass(warning.category, ConverterWarning):
            logger.warning("%s", warning.message)
        else:
            warnings.warn(warning.message, warning.category, stacklevel=2)
    return sbgn


def read_sbgn_from_file(f: Path) -> Sbgn:
    """Read an SBGN document from a file.

    The document is not validated against the schema, see
    [`validate_xsd`][libsbgnpy.validator.validate_xsd]. SBGN-ML 0.1 and 0.2
    documents are upconverted while reading.

    Args:
        f: path of the SBGN file

    Returns:
        The SBGN document.

    The file is decoded with the encoding its XML declaration names, UTF-8 by
    default.

    Raises:
        OSError: if the file cannot be read
        xsdata.exceptions.ParserError: if the content is no SBGN-ML
    """
    try:
        return _read_sbgn(Path(f).read_bytes())
    except ParserError:
        logger.error("SBGN file could not be parsed: '%s'", f)
        raise


def read_sbgn_from_string(xml_str: str) -> Sbgn:
    """Read an SBGN document from a string.

    The string is already decoded, an encoding named by its XML declaration is
    ignored. SBGN-ML 0.1 and 0.2 documents are upconverted while reading.

    Args:
        xml_str: SBGN-ML document

    Returns:
        The SBGN document.

    Raises:
        xsdata.exceptions.ParserError: if the content is no SBGN-ML
    """
    return _read_sbgn(xml_str)


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

    Element-only content is indented with two spaces, mixed content (text
    next to elements, as in XHTML notes) is written as it is.

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
    if not _has_mixed_content(node):
        etree.indent(node, space="  ")
    return etree.tostring(node, encoding="unicode")


def _has_mixed_content(node: etree._Element) -> bool:
    """Check whether text stands next to child elements in a tree.

    Args:
        node: root of the tree

    Returns:
        True if an element has children and non-whitespace text or tails.
    """
    for element in node.iter(etree.Element):
        if len(element) == 0:
            continue
        if (element.text or "").strip():
            return True
        if any((child.tail or "").strip() for child in element):
            return True
    return False


def element_from_string(xml_str: str) -> AnyElement:
    """Parse raw XML into an entry of a `notes` or `extension` element.

    Args:
        xml_str: XML of a single element

    Returns:
        The element tree.

    Raises:
        lxml.etree.XMLSyntaxError: if the string is no well-formed XML
    """
    return _node_to_element(parse_xml(xml_str))


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
            child_node = _element_to_node(child)
            child_node.tail = child.tail
            node.append(child_node)
        elif isinstance(child, str):
            # text between the child elements, it follows the previous element
            if len(node):
                node[-1].tail = (node[-1].tail or "") + child
            else:
                node.text = (node.text or "") + child
    return node


def _node_to_element(node: etree._Element) -> AnyElement:
    """Convert an lxml element tree into an `AnyElement` tree.

    Comments and processing instructions are dropped, they have no
    representation in the bindings; the text after them is kept.

    Args:
        node: lxml element to convert

    Returns:
        The element tree.
    """
    text = node.text
    children: list[AnyElement] = []
    for child in node:
        if isinstance(child.tag, str):
            element = _node_to_element(child)
            element.tail = child.tail
            children.append(element)
        elif child.tail:
            if children:
                children[-1].tail = (children[-1].tail or "") + child.tail
            else:
                text = (text or "") + child.tail

    return AnyElement(
        qname=etree.QName(node).text,
        text=text,
        children=list(children),
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
    extension is returned. Render information in the namespace of the earlier
    EML render extension is upconverted to `RENDER_NAMESPACE`.

    Args:
        extension: extension of an SBGN element, e.g., of a map

    Returns:
        The render information, or `None` if the extension contains none.

    Raises:
        xsdata.exceptions.ParserError: if the `renderInformation` entry is no
            valid render information
        lxml.etree.XMLSyntaxError: if an entry set as a string is no
            well-formed XML
    """
    if extension is None:
        return None

    qname = f"{{{RENDER_NAMESPACE}}}renderInformation"
    for element in extension.any_element:
        root = parse_xml(element_to_string(element))
        if etree.QName(root).namespace in RENDER_NAMESPACES_OLD:
            root = _upconvert_render(root)
        if root.tag == qname:
            return read_render_from_string(etree.tostring(root, encoding="unicode"))
    return None


def _upconvert_render(root: etree._Element) -> etree._Element:
    """Upconvert render information of the EML render extension.

    Args:
        root: `renderInformation` element in a namespace of
            `RENDER_NAMESPACES_OLD`

    Returns:
        A copy in the `RENDER_NAMESPACE`, without the attributes of
        `RENDER_ATTRIBUTES_OLD`.
    """
    root = _move_namespaces(root, RENDER_NAMESPACES_OLD, RENDER_NAMESPACE)
    for tag, attributes in RENDER_ATTRIBUTES_OLD.items():
        for node in root.iter(f"{{{RENDER_NAMESPACE}}}{tag}"):
            for name in attributes:
                if node.attrib.pop(name, None) is not None:
                    logger.debug("Render attribute '%s' of '%s' dropped", name, tag)
    return root
