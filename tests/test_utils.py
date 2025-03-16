"""
Tests the SBGN utility functions.
"""

from pathlib import Path

import pytest
from libsbgnpy import sbgn_examples_dir
from libsbgnpy import utils as utils
from libsbgnpy.libsbgnTypes import Language


@pytest.fixture
def f_adh() -> Path:
    """ADH example SBGN."""
    return sbgn_examples_dir / "adh.sbgn"


def test_read_from_file(f_adh) -> None:
    sbgn = utils.read_from_file(f_adh)
    assert sbgn is not None


def test_write_to_file(f_adh: Path, tmpdir: Path) -> None:
    sbgn = utils.read_from_file(f_adh)
    utils.write_to_file(sbgn, tmpdir / "test.sbgn")
    sbgn2 = utils.read_from_file(tmpdir / "test.sbgn")
    assert sbgn2 is not None


def test_write_to_string(f_adh: Path) -> None:
    sbgn = utils.read_from_file(f_adh)
    sbgn_str = utils.write_to_string(sbgn)

    assert sbgn_str is not None
    assert "xml" in sbgn_str


def test_get_version(f_adh):
    version = utils.get_version(f_adh)
    assert version == 2


def test_get_language(f_adh):
    language = utils.get_language(f_adh)
    assert language == Language.PD
