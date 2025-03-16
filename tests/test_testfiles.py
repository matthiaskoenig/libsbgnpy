"""
Read all test files.
"""

import pytest
from pathlib import Path
from typing import List
import libsbgnpy.libsbgn as libsbgn


def find_sbgn_files(directory: Path) -> List[Path]:
    """Find SBGN files in directory."""

    return sorted([f for f in directory.glob("**/*.sbgn")])


@pytest.mark.parametrize(
    "filename",
    find_sbgn_files(directory=Path(__file__).parent / "test-files"),
    ids=lambda x: f"{x.parent.name}/{x.name}",
)
def test_read_examples(filename: str, tmpdir: Path) -> None:
    """Parse SBGN file test."""

    sbgn = libsbgn.parse(filename)
    assert sbgn is not None

    # write everything to tempfile
    sbgn.write_file(tmpdir / "test.sbgn")
