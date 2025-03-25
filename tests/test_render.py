"""Tests the SBGN render functions."""

from pathlib import Path
from libsbgnpy.examples import render_example


def test_render_example(tmpdir: Path) -> None:
    f_sbgn = tmpdir / "test.sbgn"
    render_example.write_map_render(f_sbgn)
    render_example.read_map_render(f_sbgn)
