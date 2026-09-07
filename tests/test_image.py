"""Test the rendering of SBGN documents as images.

The rendering uses a web service, these tests therefore require network access.
"""

from pathlib import Path

import pytest

from libsbgnpy import read_sbgn_from_file, render_sbgn

#: the SBGN documents the examples read
EXAMPLES_SBGN_DIR = Path(__file__).parent.parent / "examples" / "sbgn"


def test_render_sbgn(tmp_path: Path) -> None:
    """An SBGN document is rendered to a PNG."""
    sbgn = read_sbgn_from_file(EXAMPLES_SBGN_DIR / "adh.sbgn")
    f_png = tmp_path / "test.png"
    render_sbgn(sbgn, f_png)

    assert f_png.exists()
    assert f_png.stat().st_size > 0


def test_render_sbgn_unsupported_format(tmp_path: Path) -> None:
    """An unsupported image format is reported."""
    sbgn = read_sbgn_from_file(EXAMPLES_SBGN_DIR / "adh.sbgn")

    with pytest.raises(ValueError, match="Unsupported image format"):
        render_sbgn(sbgn, tmp_path / "test.svg", file_format="svg")


def test_render_sbgn_wrong_suffix(tmp_path: Path) -> None:
    """An image file with another suffix is reported."""
    sbgn = read_sbgn_from_file(EXAMPLES_SBGN_DIR / "adh.sbgn")

    with pytest.raises(ValueError, match="must end in"):
        render_sbgn(sbgn, tmp_path / "test.jpg")
