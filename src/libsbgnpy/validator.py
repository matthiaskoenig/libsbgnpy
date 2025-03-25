"""Validation of SBGN files against the schema is implemented."""

from pathlib import Path
import sys
from enum import Enum
from typing import Any

from lxml import etree


XSD_SCHEMA = Path(__file__).parent / "schema" / "SBGN.xsd"


def validate_xsd(f: Path) -> Any:
    """Validate SBGN file against XSD schema.

    :param f: file to validate
    :return: Returns None if valid, the error log otherwise.
    """
    xmlschema_doc = etree.parse(XSD_SCHEMA)
    xmlschema = etree.XMLSchema(xmlschema_doc)

    # with open(f, "r") as f_in:
    #     xml_str = f_in.read()
    #     # upconverting for fixing reading
    #     xml_str = xml_str.replace(
    #         "http://sbgn.org/libsbgn/0.1", "http://sbgn.org/libsbgn/0.3"
    #     )
    #     xml_str = xml_str.replace(
    #         "http://sbgn.org/libsbgn/0.2", "http://sbgn.org/libsbgn/0.3"
    #     )
    #
    # with tempfile.TemporaryFile(mode='w') as f_tmp:
    #   f_tmp.write(xml_str)

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


if __name__ == "__main__":
    from libsbgnpy import sbgn_examples_dir

    f = sbgn_examples_dir / "adh_0.3.sbgn"
    xsd_valid = validate_xsd(f)
