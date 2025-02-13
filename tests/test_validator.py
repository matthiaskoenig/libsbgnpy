"""Test validator."""

from pathlib import Path
from libsbgnpy.validation import validator


def test_validate_xsd_01():
    """Test XSD validation."""
    f = Path(__file__).parent / "../src/libsbgnpy/examples/sbgn/adh.sbgn"
    is_valid = validator.validate_xsd(f) is None
    assert is_valid


def test_validate_xsd_02():
    """Test XSD validation."""
    f = Path(__file__).parent / "../src/libsbgnpy/examples/sbgn/glycolysis.sbgn"
    is_valid = validator.validate_xsd(f) is None
    assert is_valid
