"""Read, write and validate the SBGN corpus.

The corpus in `tests/data` are the reference maps of the SBGN specifications,
one directory per map language (`AF`, `ER`, `PD`).
"""

from pathlib import Path

import pytest

from libsbgnpy import read_sbgn_from_file, validate_xsd, write_sbgn_to_file

#: reference maps of the SBGN specifications
DATA_DIR = Path(__file__).parent / "data"

#: every SBGN document of the corpus
SBGN_FILES = sorted(DATA_DIR.glob("**/*.sbgn"))


def _file_id(f: Path) -> str:
    """Name a corpus file by its language directory and file name."""
    return f"{f.parent.name}/{f.name}"


@pytest.mark.parametrize("f", SBGN_FILES, ids=_file_id)
def test_read_write(f: Path, tmp_path: Path) -> None:
    """Every document of the corpus is read and written again."""
    sbgn = read_sbgn_from_file(f)
    assert sbgn.map

    f_out = tmp_path / "test.sbgn"
    write_sbgn_to_file(sbgn, f_out)
    assert read_sbgn_from_file(f_out).map


@pytest.mark.parametrize("f", SBGN_FILES, ids=_file_id)
def test_validate(f: Path) -> None:
    """Every document of the corpus is valid SBGN."""
    assert validate_xsd(f) == []
