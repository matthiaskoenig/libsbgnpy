# -*- coding: utf-8 -*-
"""
Write and read extension information.
see https://github.com/sbgn/sbgn/wiki/SBGN-ML_Extensions
"""

from pathlib import Path

from libsbgnpy import Extension, Language, libsbgn, utils


def write_map_extension(f):
    """Write extension information on map.

    :param f: file input
    :return: None
    """
    sbgn = libsbgn.sbgn()
    map = libsbgn.map()
    map.set_language(Language.PD)
    sbgn.set_map(map)

    extension = Extension(
        """<renderInformation id="example" programName="SBML Layout" programVersion="3.0"
     xmlns="http://projects.eml.org/bcb/sbml/render/level2">
        <listOfColorDefinitions>
        <colorDefinition id="yelloComp" value="#ffffccff" />
        <colorDefinition id="grayComp" value="#e0e0e0ff" />
        <colorDefinition id="orange" value="#fa9e2fff" />
        <colorDefinition id="blue" value="#2958acff" />
        <colorDefinition id="green" value="#378f5cff" />
        <colorDefinition id="Color_0" value="#969696" />
        <colorDefinition id="Color_1" value="#ff9900" />
        <colorDefinition id="Color_2" value="#000000" />
        </listOfColorDefinitions>
        <listOfGradientDefinitions>
        <linearGradient x1="0%" y1="0%" z1="0%" x2="100%" y2="0%" z2="100%" id="LinearGradient_0" spreadMethod="reflect">
            <stop offset="0%" stop-color="#ccffff" />
            <stop offset="100%" stop-color="#ffffff" />
        </linearGradient>
        <linearGradient x1="0%" y1="0%" z1="0%" x2="100%" y2="0%" z2="100%" id="OrangeGradient_0" spreadMethod="reflect">
            <stop offset="0%" stop-color="#ffffff" />
            <stop offset="100%" stop-color="#fa9e2fff" />
        </linearGradient>
        <linearGradient x1="0%" y1="0%" z1="0%" x2="100%" y2="0%" z2="100%" id="BlueGradient_0" spreadMethod="reflect">
            <stop offset="0%" stop-color="#ffffff" />
            <stop offset="100%" stop-color="#2958acff" />
        </linearGradient>
        <linearGradient x1="0%" y1="0%" z1="0%" x2="100%" y2="0%" z2="100%" id="GreenGradient_0" spreadMethod="reflect">
            <stop offset="0%" stop-color="#ffffff" />
            <stop offset="100%" stop-color="#378f5cff" />
        </linearGradient>
        </listOfGradientDefinitions>
        <listOfStyles>
        <style idList="glyph0 glyph2 glyph14 glyph34 ">
            <g stroke="Color_2" stroke-width="5" fill="yelloComp" />
        </style>
        <style idList="glyph1">
            <g stroke="Color_2" stroke-width="5" fill="grayComp" />
        </style>
        <style idList="glyph8 glyph23 glyph5 glyph12 glyph21 glyph13 glyph4 glyph6 glyph7 glyph20 glyph22">
            <g stroke="orange" stroke-width="2" fill="OrangeGradient_0" />
        </style>
        <style idList="glyph3 glyph47 glyph10 glyph11">
            <g stroke="blue" stroke-width="2" fill="BlueGradient_0" />
        </style>
        <style idList="glyph32 glyph37 glyph37a glyph31 glyph39 glyph40 glyph36 glyph28 glyph35 glyph27 glyph25 glyph26 glyph9 glyph38 glyph38a glyph29 glyph30 glyph46 glyph33">
            <g stroke="green" stroke-width="2" fill="GreenGradient_0" />
        </style>
        <style idList="a38">
            <g stroke="blue" stroke-width="2"  />
        </style>
        </listOfStyles>
    </renderInformation>"""
    )
    map.set_extension(extension)

    # print(utils.write_to_string(sbgn))
    utils.write_to_file(sbgn=sbgn, f=f)


def read_map_extension(f: Path) -> None:
    """Read notes from glyphs.

    :param f: file input
    :return: None
    """
    sbgn = utils.read_from_file(f=f)

    # map is a container for the glyphs and arcs
    map = sbgn.get_map()

    extension = map.get_extension()
    if extension:
        print(extension)
        print(str(extension))


if __name__ == "__main__":
    f = "sbgn/notes.sbgn"
    write_map_extension(f)
    print("_" * 80, "\n")
    read_map_extension(f)
