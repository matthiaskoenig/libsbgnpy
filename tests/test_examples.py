"""
Test the example scripts in the examples folder.
"""

import pytest
from pathlib import Path
from libsbgnpy import sbgn_examples_dir
from libsbgnpy.examples.info_example import info_example
from libsbgnpy.examples.read_example import read_sbgn_01
from libsbgnpy.examples.write_example import write_sbgn_01, write_sbgn_02, write_sbgn_03


@pytest.mark.parametrize(
    "filename",
    [
        "adh.sbgn",
        "glycolysis.sbgn",
        "test-output-01.sbgn",
        "test-output-02.sbgn",
    ],
)
def test_read_examples(filename: str) -> None:
    """Parse SBGN file test."""
    sbgn = read_sbgn_01(sbgn_examples_dir / filename)
    assert sbgn is not None


def test_write_example_01(tmpdir: Path) -> None:
    """Write SBGN file test 1."""
    write_sbgn_01(tmpdir / "test-output-01.sbgn")


def test_write_example_02(tmpdir: Path) -> None:
    """Write SBGN file test 2."""
    write_sbgn_02(tmpdir / "test-output-02.sbgn")


def test_write_example_03(tmpdir: Path) -> None:
    """Write SBGN file test 3."""
    write_sbgn_03(tmpdir / "test-output-03.sbgn")


def test_write_read_example_01(tmpdir: Path) -> None:
    write_sbgn_01(tmpdir / "test-output-01.sbgn")
    sbgn = read_sbgn_01(tmpdir / "test-output-01.sbgn")
    assert sbgn is not None


def test_write_read_example_02(tmpdir: Path) -> None:
    write_sbgn_02(tmpdir / "test-output-02.sbgn")
    sbgn = read_sbgn_01(tmpdir / "test-output-02.sbgn")
    assert sbgn is not None


def test_write_read_example_03(tmpdir: Path) -> None:
    write_sbgn_02(tmpdir / "test-output-01.sbgn")
    sbgn = read_sbgn_01(tmpdir / "test-output-01.sbgn")
    assert sbgn is not None


def test_info_example() -> None:
    info_example()
