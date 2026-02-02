"""Test image rendering"""

from pathlib import Path

from libsbgnpy import *
from libsbgnpy.image import render_sbgn


def test_image_render_sbgn(tmpdir: Path) -> None:
    """Test rendering SBGN to PNG."""
    sbgn = read_sbgn_from_file(sbgn_examples_dir / "adh.sbgn")
    render_sbgn(sbgn, image_file=tmpdir / "test.png", file_format="png")
