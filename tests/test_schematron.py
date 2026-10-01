"""Tests of the schematron validation."""

import copy
import logging
import re
from pathlib import Path

import pytest
from lxml import etree, isoschematron

import libsbgnpy
from libsbgnpy import Issue, validate_schematron
from libsbgnpy.io import SBGN_NAMESPACE

#: the packaged schemas and rules
SCHEMA_DIR = Path(libsbgnpy.__file__).parent / "schema"

#: reference maps of the SBGN specifications, one directory per map language
DATA_DIR = Path(__file__).parent / "data"

#: test files of the rules of libsbgn, see `src/libsbgnpy/schema/README.md`
SCHEMATRON_DIR = DATA_DIR / "schematron"

#: `<rule>-pass.sbgn` does not break the rule, `<rule>-fail[-<n>].sbgn` does
RULE_FILE = re.compile(r"(?P<rule>[a-z]{2}\d{5})-(?P<outcome>pass|fail)(-\d+)?")

#: the rules the reference maps break; the same as with Saxon, the XSLT 2.0
#: processor of the Java library
REFERENCE_MAP_ISSUES = [
    ("AF/AF_Reference_Card.sbgn", "af10111"),
    ("AF/AF_Reference_Card.sbgn", "af10112"),
    ("AF/AF_Reference_Card.sbgn", "af10113"),
    ("ER/ER_Reference_Card.sbgn", "er10102"),
    ("ER/ER_Reference_Card.sbgn", "er10104"),
    ("PD/PD_Reference_Card.sbgn", "pd10104"),
    ("PD/PD_Reference_Card.sbgn", "pd10108"),
    ("PD/PD_Reference_Card.sbgn", "pd10111"),
    ("PD/PD_Reference_Card.sbgn", "pd10125"),
    ("PD/PD_Reference_Card.sbgn", "pd10126"),
    ("PD/PD_Reference_Card.sbgn", "pd10127"),
    ("PD/PD_Reference_Card.sbgn", "pd10128"),
    ("PD/PD_Reference_Card.sbgn", "pd10131"),
    ("PD/PD_Reference_Card.sbgn", "pd10132"),
    ("PD/PD_Reference_Card.sbgn", "pd10141"),
    ("PD/PD_Reference_Card.sbgn", "pd10142"),
    ("PD/annotation.sbgn", "pd10131"),
    ("PD/labeledCloneMarker.sbgn", "pd10131"),
    ("PD/multimer2.sbgn", "pd10131"),
    ("PD/statesType2.sbgn", "pd10131"),
    ("PD/utf8_test_case_with_byte_order_mark.sbgn", "pd10131"),
    ("PD/utf8_test_case_without_byte_order_mark.sbgn", "pd10131"),
]

PD_FAIL = SCHEMATRON_DIR / "PD" / "pd10101-fail.sbgn"
ER_FAIL = SCHEMATRON_DIR / "ER" / "er10103-fail.sbgn"


RULE_FILES = sorted(SCHEMATRON_DIR.glob("*/*.sbgn"))


@pytest.mark.parametrize("language", ["af", "er", "pd"])
def test_rules_compile_with_xslt1(language: str) -> None:
    """The basic phase of the packaged rules compiles with XSLT 1.0.

    The upstream rules deviate from the ISO Schematron grammar, e.g., pattern
    ids which are no XML names, so the grammar check is disabled.
    """
    rules = etree.parse(SCHEMA_DIR / f"sbgn_{language}.sch")
    isoschematron.Schematron(rules, phase="basic", validate_schema=False)


@pytest.mark.parametrize("f", RULE_FILES, ids=lambda f: f.name)
def test_rule_files(f: Path) -> None:
    """A fail file breaks the rule it is named after, a pass file does not."""
    match = RULE_FILE.fullmatch(f.stem)
    assert match, f"unexpected name of a test file: {f.name}"

    rule_ids = {issue.rule_id for issue in validate_schematron(f)}

    if match["outcome"] == "fail":
        assert match["rule"] in rule_ids
    else:
        assert match["rule"] not in rule_ids


def test_reference_maps() -> None:
    """The reference maps break the rules they break with the Java library."""
    files = sorted(
        f
        for language in ("AF", "ER", "PD")
        for f in (DATA_DIR / language).glob("*.sbgn")
    )
    issues = sorted(
        {
            (f"{f.parent.name}/{f.name}", issue.rule_id)
            for f in files
            for issue in validate_schematron(f)
        }
    )
    assert issues == REFERENCE_MAP_ISSUES


def test_issue() -> None:
    """An issue names the rule, its message and the element which breaks it."""
    issues = validate_schematron(PD_FAIL)

    assert issues[0] == Issue(
        severity="error",
        rule_id="pd10101",
        message=(
            "Arc with class consumption must have source reference to glyph of "
            "EPN classes"
        ),
        element_id="a01",
    )


def test_valid_document() -> None:
    """A document which breaks no rule has no issues."""
    assert validate_schematron(SCHEMATRON_DIR / "PD" / "pd10101-pass.sbgn") == []


def _write(root: etree._Element, f: Path) -> Path:
    """Write a tree into a file."""
    f.write_bytes(etree.tostring(root, xml_declaration=True, encoding="UTF-8"))
    return f


def test_maps_of_two_languages(tmp_path: Path) -> None:
    """Every map is checked on its own with the rules of its language."""
    root = etree.parse(PD_FAIL).getroot()
    er_map = etree.parse(ER_FAIL).getroot().find(f"{{{SBGN_NAMESPACE}}}map")
    assert er_map is not None
    root.append(er_map)
    f = _write(root, tmp_path / "two_maps.sbgn")

    issues = validate_schematron(f)

    assert issues == validate_schematron(PD_FAIL) + validate_schematron(ER_FAIL)
    assert {issue.rule_id[:2] for issue in issues} == {"pd", "er"}


def test_maps_do_not_see_each_other(tmp_path: Path) -> None:
    """A map is not checked against the glyphs and arcs of another map.

    Two copies of a valid map hold the same ids; rules which look up an id in
    the whole document would find a second, unrelated element.
    """
    root = etree.parse(SCHEMATRON_DIR / "PD" / "pd10101-pass.sbgn").getroot()
    sbgn_map = root.find(f"{{{SBGN_NAMESPACE}}}map")
    assert sbgn_map is not None
    root.append(copy.deepcopy(sbgn_map))
    f = _write(root, tmp_path / "copies.sbgn")

    assert validate_schematron(f) == []


def test_upconverted_document(tmp_path: Path) -> None:
    """An SBGN-ML 0.2 document is checked as the 0.3 document it is read as."""
    xml = PD_FAIL.read_text().replace(SBGN_NAMESPACE, "http://sbgn.org/libsbgn/0.2")
    f = tmp_path / "pd_0.2.sbgn"
    f.write_text(xml)

    assert validate_schematron(f) == validate_schematron(PD_FAIL)


def test_byte_order_mark(tmp_path: Path) -> None:
    """A document with a byte order mark is read."""
    f = tmp_path / "bom.sbgn"
    f.write_bytes(b"\xef\xbb\xbf" + PD_FAIL.read_bytes())

    assert validate_schematron(f) == validate_schematron(PD_FAIL)


def test_map_without_language(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """A map of an unknown language is not checked, which is logged."""
    root = etree.parse(PD_FAIL).getroot()
    sbgn_map = root.find(f"{{{SBGN_NAMESPACE}}}map")
    assert sbgn_map is not None
    del sbgn_map.attrib["language"]
    f = _write(root, tmp_path / "no_language.sbgn")

    with caplog.at_level(logging.INFO, logger="libsbgnpy"):
        assert validate_schematron(f) == []
    assert "map1" in caplog.text


def test_no_sbgn_document(tmp_path: Path) -> None:
    """A document without SBGN maps has no issues, see `validate_xsd`."""
    f = tmp_path / "other.xml"
    f.write_text("<other/>")

    assert validate_schematron(f) == []


def test_malformed_xml(tmp_path: Path) -> None:
    """A document which is no well-formed XML raises."""
    f = tmp_path / "malformed.sbgn"
    f.write_text("<sbgn>")

    with pytest.raises(etree.XMLSyntaxError):
        validate_schematron(f)
