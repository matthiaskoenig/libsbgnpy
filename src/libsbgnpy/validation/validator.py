# -*- coding: utf-8 -*-
"""
This is an example that shows both low-level validation against the XSD Schema,
and high-level validation using schematron.

At this point only the XSD validation is implemented.
see [#7](https://github.com/matthiaskoenig/libsbgnpy/issues/7)
"""

import os
import sys
from enum import Enum

from lxml import etree

import libsbgnpy.utils as utils
from libsbgnpy.libsbgnTypes import Language


dir = os.path.dirname(os.path.realpath(__file__))
XSD_SCHEMA = os.path.join(dir, "../schema/SBGN.xsd")


def validate_xsd(f):
    """Validate SBGN file against XSD schema.

    :param f: file to validate
    :return: Returns None if valid, the error log otherwise.
    """
    xmlschema_doc = etree.parse(XSD_SCHEMA)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    doc = etree.parse(f)
    is_valid = xmlschema.validate(doc)
    if not is_valid:
        log = xmlschema.error_log
        sys.stderr.write(str(log) + "\n")
        return log

    return None


class Severity(Enum):
    WARNING = 1
    ERROR = 2


class Issue(object):
    """
    Describes one issue found during schematron validation.
    One validation run may produce multiple issues.
    """

    def __init__(self, role, rule_id, diagnostic_id, message):
        self.message = message.strip()
        self.diagnostic_id = diagnostic_id
        self.rule_id = rule_id
        if role.lower() == "error":
            self.severity = Severity.ERROR
        else:
            self.severity = Severity.WARNING

    def get_severity(self):
        """Severity of the issue, i.e.: is it an error, or a warning?"""
        return self.severity

    def get_message(self):
        """Human readable description of the issue."""
        return self.message

    def get_diagnostic_id(self):
        """Identifier of the element that this issue is about."""
        return self.diagnostic_id

    def get_rule_id(self):
        """Identifier of the issue"""
        return self.rule_id

    def __str__(self):
        return "{} at diagnosticId={}; ruleId={} Message: {}".format(
            self.severity, self.diagnostic_id, self.rule_id, self.message
        )


def validate_schematron(f_sbgn):
    """Validate SBGN file with schematron.

    In Java this does the XSL Transformations on the ruleset and the exported Pathway Object
    and then invokes the SAX parser through "parseSVRL" method on the transformation's result.

    :param f: SBGN file
    :return:
    """
    # !!! NOT IMPLEMENTED !!!

    # schema for language
    language = utils.get_language(f_sbgn)
    if language == Language.AF:
        lang = "af"
    elif language == Language.PD:
        lang = "pd"
    elif language == language.ER:
        lang = "er"
    f_schema = os.path.join(dir, "rules/sbgn_{}.sch".format(lang))
    print(f_schema)

    # Create an svrl file via subsequent xslt transformations
    f_xsl = os.path.join(dir, "schematron/iso_svrl_for_xslt1.xsl")

    # prepare schematron rules via transformation
    doc_schema = etree.parse(f_schema)

    doc_xslt = etree.parse(f_xsl)
    transform_1 = etree.XSLT(doc_xslt)
    doc_sct = transform_1(doc_schema)
    print("*" * 80)
    print(etree.tostring(doc_sct, pretty_print=True))
    print("*" * 80)

    # validation via transformation
    doc_sbgn = etree.parse(f_sbgn)
    transform_2 = etree.XSLT(doc_sct)
    doc_svrlt = transform_2(doc_sbgn)
    print("*" * 80)
    print(etree.tostring(doc_svrlt, pretty_print=True))
    print("*" * 80)

    # from lxml.isoschematron import Schematron
    # schematron = Schematron(doc_schema)
    # schematron.validate(doc_sbgn)


if __name__ == "__main__":
    f = "../examples/sbgn/adh.sbgn"
    # f = "error-test-files/PD/pd10101-pass.sbgn"
    # f = "../examples/sbgn/glycolysis.sbgn"

    xsd_valid = validate_xsd(f) is None
    print("XSD valid ({}): {}".format(f, xsd_valid))

    sct_valid = validate_schematron(f)
    print("Schematron valid ({}): {}".format(f, xsd_valid))
