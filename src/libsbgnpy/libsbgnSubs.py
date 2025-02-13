"""
Overwritten classes (Notes & Extension)
"""

try:
    from lxml import etree as etree_
except ImportError:
    from xml.etree import ElementTree as etree_


import libsbgnpy.libsbgn as supermod
from libsbgnpy.libsbgn import showIndent


def _process_xml_input(input):
    """Helper function for input to Notes and Extension.

    :param input: xml_string
    :return: anytypeobjs_
    """
    anytypeobjs_ = None
    if input is not None:
        anytypeobjs_ = input.strip()
    return anytypeobjs_


class _Information(object):
    def __str__(self):
        if type(self.anytypeobjs_) in (list, tuple):
            return str(self.anytypeobjs_[0])
        else:
            return str(self.anytypeobjs_)

    def hasContent_(self):
        return self.anytypeobjs_ is not None

    def export(
        self,
        outfile,
        level,
        namespace_="sbgn:",
        name_=None,
        namespacedef_='xmlns:sbgn="http://sbgn.org/libsbgn/0.2"',
        pretty_print=True,
    ):
        """Custom export function.

        Necessary to provide handling for the xsd:any.
        """
        name_ = self.__class__.__name__.lower()
        if pretty_print:
            eol_ = "\n"
        else:
            eol_ = ""

        if self.hasContent_():
            # notes defined as sequence, so handle the normal case of just having string
            notes_items = self.anytypeobjs_
            if type(self.anytypeobjs_) not in [list, tuple]:
                notes_items = [notes_items]
            showIndent(outfile, level, pretty_print)
            outfile.write(
                "<%s%s%s>%s"
                % (namespace_, name_, namespacedef_ and " " + namespacedef_ or "", eol_)
            )
            for obj_ in notes_items:
                showIndent(outfile, level, pretty_print)
                outfile.write("%s%s" % (obj_, eol_))
            showIndent(outfile, level, pretty_print)
            outfile.write(
                "</%s%s%s>%s"
                % (namespace_, name_, namespacedef_ and " " + namespacedef_ or "", eol_)
            )

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False):
        """Custom build function.

        Necessary to provide handling for the xsd:any.
        """
        # This is the lxml.etree._Element, in first version going via strings
        obj_ = etree_.tostring(child_, pretty_print=False, encoding="unicode")
        # print('obj_', obj_)
        if obj_ is not None:
            self.add_anytypeobjs_(obj_)


class Notes(_Information, supermod.notesType):
    """SBGN Notes class.

    The optional SBGN element named 'notes', present on every major SBGN
    component type, is intended as a place for storing optional
    information intended to be seen by humans.  An example use of the
    'notes' element would be to contain formatted user comments about the
    model element in which the 'notes' element is enclosed.  Every object
    derived directly or indirectly from type SBase can have a separate
    value for 'notes', allowing users considerable freedom when adding
    comments to their models.

    The format of 'notes' elements must be XHTML 1.0 (http://www.w3.org/1999/xhtml).
    """

    def __init__(self, xml_string=None):
        super(Notes, self).__init__(
            _process_xml_input(xml_string),
        )


supermod.notesType.subclass = Notes


class Extension(_Information, supermod.extensionType):
    """SBGN Extension class.

    Any well-formed XML content, and with each top-level element placed in a unique XML namespace; see text.
    Whereas Notes is a container for content to be shown directly to humans, Extension is a container for
    optional software-generated content not meant to be shown to humans. Every SBGN object can
    have its own Extension object instance. In XML, the Extension content type is any, allowing essentially
    arbitrary well-formed XML data content.
    """

    def __init__(self, xml_string=None):
        super(Extension, self).__init__(
            _process_xml_input(xml_string),
        )


supermod.extensionType.subclass = Extension
