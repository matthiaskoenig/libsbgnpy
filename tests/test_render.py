"""
Tests the SBGN render functions.
"""

from pathlib import Path
from libsbgnpy import utils, sbgn_examples_dir


def test_render_sbgn(tmpdir: Path):
    """Test rendering SBGN to PNG."""
    sbgn = utils.read_sbgn_from_file(sbgn_examples_dir / "adh.sbgn")
    render.render_sbgn(sbgn, image_file=tmpdir / "test.png", file_format="png")
