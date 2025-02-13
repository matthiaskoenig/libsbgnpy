"""
Tests the SBGN utility functions.
"""

from pathlib import Path
import tempfile

import pytest

from libsbgnpy import utils as utils
from libsbgnpy.libsbgnTypes import Language


@pytest.fixture
def f_adh():
    return Path(__file__).parent / "../src/libsbgnpy/examples/sbgn/adh.sbgn"


def test_read_from_file(f_adh):
    sbgn = utils.read_from_file(f_adh)
    assert sbgn is not None


def test_write_to_file(f_adh):
    sbgn = utils.read_from_file(f_adh)
    f_out = tempfile.NamedTemporaryFile(suffix=".sbgn")
    utils.write_to_file(sbgn, f_out.name)
    sbgn2 = utils.read_from_file(f_out)
    assert sbgn2 is not None


def test_write_to_string(f_adh):
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
