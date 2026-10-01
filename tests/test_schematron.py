"""Tests of the schematron validation."""

from pathlib import Path

import pytest
from lxml import etree, isoschematron

import libsbgnpy

#: the packaged schemas and rules
SCHEMA_DIR = Path(libsbgnpy.__file__).parent / "schema"


@pytest.mark.parametrize("language", ["af", "er", "pd"])
def test_rules_compile_with_xslt1(language: str) -> None:
    """The basic phase of the packaged rules compiles with XSLT 1.0.

    The upstream rules deviate from the ISO Schematron grammar, e.g., pattern
    ids which are no XML names, so the grammar check is disabled.
    """
    rules = etree.parse(SCHEMA_DIR / f"sbgn_{language}.sch")
    isoschematron.Schematron(rules, phase="basic", validate_schema=False)
