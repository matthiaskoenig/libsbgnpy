"""Test image rendering"""

import pytest
from pathlib import Path

from libsbgnpy import *
from libsbgnpy.image import render_sbgn


@pytest.mark.skip
def test_image_render_sbgn(tmpdir: Path) -> None:
    """Test rendering SBGN to PNG."""
    sbgn = read_sbgn_from_file(sbgn_examples_dir / "adh.sbgn")
    render_sbgn(sbgn, image_file=tmpdir / "test.png", file_format="png")
