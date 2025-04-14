"""Test validator."""

import pytest
from pathlib import Path
from libsbgnpy import validator


def find_sbgn_files(directory: Path) -> list[Path]:
    """Find SBGN files in directory."""

    return sorted([f for f in directory.glob("**/*.sbgn")])


@pytest.mark.skip(reason="Not implemented")
@pytest.mark.parametrize(
    "filename",
    find_sbgn_files(directory=Path(__file__).parent / "test-files"),
    ids=lambda x: f"{x.parent.name}/{x.name}",
)
def test_validate_file(filename: str, tmpdir: Path) -> None:
    """Validate test files."""
    errors = validator.validate_xsd(f=Path(filename)) is None
    assert not errors
