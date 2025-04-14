"""Tests the IO functionality."""

from pathlib import Path

import pytest
from libsbgnpy import *


@pytest.fixture
def f_adh() -> Path:
    """ADH example SBGN."""
    return sbgn_examples_dir / "adh.sbgn"


def test_read_sbgn_from_file(f_adh) -> None:
    sbgn = read_sbgn_from_file(f_adh)
    assert sbgn is not None


def test_write_sbgn_to_file(f_adh: Path, tmpdir: Path) -> None:
    sbgn = read_sbgn_from_file(f_adh)
    write_sbgn_to_file(sbgn, tmpdir / "test.sbgn")
    sbgn2 = read_sbgn_from_file(tmpdir / "test.sbgn")
    assert sbgn2 is not None


def test_write_sbgn_to_string(f_adh: Path) -> None:
    sbgn = read_sbgn_from_file(f_adh)
    sbgn_str = write_sbgn_to_string(sbgn)

    assert sbgn_str is not None
    assert "xml" in sbgn_str


def test_read_write_render(f_adh) -> None:
    xml_str = """
    <renderInformation id="example" programName="libsbgnpy" programVersion="1.0.0"
     xmlns="http://www.sbml.org/sbml/level3/version1/render/version1">
        <listOfColorDefinitions>
        <colorDefinition id="color0" value="#969696" />
        <colorDefinition id="color1" value="#ff9900" />
        </listOfColorDefinitions>

        <listOfGradientDefinitions>
            <linearGradient x1="0%" y1="0%" x2="100%" y2="0%" id="gradient0">
                <stop offset="0%" stop-color="#ccffff" />
                <stop offset="100%" stop-color="#ffffff" />
            </linearGradient>
        </listOfGradientDefinitions>

        <listOfStyles>
        <style idList="glyph1 glyph2">
            <g stroke="color0" stroke-width="5" fill="color1" />
        </style>
        <style idList="glyph3">
            <g stroke="color1" stroke-width="2" fill="gradient0" />
        </style>
        </listOfStyles>
    </renderInformation>
    """
    render_info = read_render_from_string(xml_str)
    assert render_info is not None

    xml_str2 = write_render_to_string(render_info)
    assert xml_str2 is not None

    render_info2 = read_render_from_string(xml_str2)
    assert render_info2 is not None
