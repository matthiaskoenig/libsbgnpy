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


def test_declared_encoding(tmp_path: Path) -> None:
    """A file is decoded with the encoding of its XML declaration."""
    f_sbgn = tmp_path / "latin1.sbgn"
    f_sbgn.write_bytes(
        (
            '<?xml version="1.0" encoding="ISO-8859-1"?>'
            '<sbgn xmlns="http://sbgn.org/libsbgn/0.3">'
            '<map id="m" language="process description">'
            '<glyph id="g" class="macromolecule"><label text="König"/>'
            '<bbox x="0" y="0" w="10" h="10"/></glyph>'
            "</map></sbgn>"
        ).encode("latin-1")
    )

    assert validate_xsd(f_sbgn) == []


def test_error_lines(tmp_path: Path) -> None:
    """The errors carry the lines of the file, also for an upconverted file."""
    xml_str = (EXAMPLES_SBGN_DIR / "invalid.sbgn").read_text(encoding="utf-8")
    f_old = tmp_path / "invalid_0.2.sbgn"
    f_old.write_text(xml_str.replace("libsbgn/0.3", "libsbgn/0.2"), encoding="utf-8")

    for f in [EXAMPLES_SBGN_DIR / "invalid.sbgn", f_old]:
        errors = validate_xsd(f)
        assert errors[0].startswith("<string>:11:0:")
        assert errors[1].startswith("<string>:13:0:")
