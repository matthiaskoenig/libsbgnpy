"""
Tests the SBGN render functions.
"""

from pathlib import Path
import tempfile

import pytest

from libsbgnpy import render, utils


@pytest.fixture
def f_adh() -> Path:
    return Path(__file__).parent / "../src/libsbgnpy/examples/sbgn/adh.sbgn"


def test_render_sbgn(f_adh):
    sbgn = utils.read_from_file(f_adh)
    tmp_file = tempfile.NamedTemporaryFile(suffix=".png")
    render.render_sbgn(sbgn, image_file=tmp_file.name, file_format="png")
