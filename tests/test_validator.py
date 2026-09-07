"""Test validation against the SBGN XSD schema."""

from pathlib import Path

from libsbgnpy import validate_xsd

#: the SBGN documents the examples read
EXAMPLES_SBGN_DIR = Path(__file__).parent.parent / "examples" / "sbgn"


def test_valid_file() -> None:
    """A valid document has no errors."""
    assert validate_xsd(EXAMPLES_SBGN_DIR / "adh.sbgn") == []


def test_valid_file_upconverted() -> None:
    """An SBGN-ML 0.2 document is validated against the 0.3 schema."""
    assert validate_xsd(EXAMPLES_SBGN_DIR / "adh_0.3.sbgn") == []


def test_invalid_example_file() -> None:
    """The intentionally invalid example reports one error per kind of violation."""
    errors = validate_xsd(EXAMPLES_SBGN_DIR / "invalid.sbgn")

    assert len(errors) == 3
    # a required attribute is missing, a value is not in the enumeration and a
    # required child element is missing, see `docs/validation.md`
    assert "SCHEMAV_CVC_COMPLEX_TYPE_4" in errors[0]
    assert "SCHEMAV_CVC_ENUMERATION_VALID" in errors[1]
    assert "SCHEMAV_ELEMENT_CONTENT" in errors[2]


def test_invalid_file(tmp_path: Path) -> None:
    """A document which does not follow the schema reports the errors."""
    f_sbgn = tmp_path / "invalid.sbgn"
    f_sbgn.write_text(
        '<sbgn xmlns="http://sbgn.org/libsbgn/0.3">'
        '<map language="process description"/>'
        "</sbgn>",
        encoding="utf-8",
    )

    errors = validate_xsd(f_sbgn)
    assert len(errors) == 1
    assert "id" in errors[0]


def test_not_xml(tmp_path: Path) -> None:
    """A file which is no XML reports the syntax error."""
    f_sbgn = tmp_path / "invalid.sbgn"
    f_sbgn.write_text("this is not xml", encoding="utf-8")

    assert len(validate_xsd(f_sbgn)) == 1
