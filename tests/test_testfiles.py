"""Read all test files."""

import pytest
from pathlib import Path
from libsbgnpy.io import read_sbgn_from_file, write_sbgn_to_file


def find_sbgn_files(directory: Path) -> list[Path]:
    """Find SBGN files in directory."""

    return sorted([f for f in directory.glob("**/*.sbgn")])


@pytest.mark.parametrize(
    "filename",
    find_sbgn_files(directory=Path(__file__).parent / "test-files"),
    ids=lambda x: f"{x.parent.name}/{x.name}",
)
def test_read_examples(filename: str, tmpdir: Path) -> None:
    """Parse SBGN file test."""

    sbgn = read_sbgn_from_file(filename)
    assert sbgn is not None

    # write everything to tempfile
    write_sbgn_to_file(sbgn=sbgn, f=tmpdir / "test.sbgn")
