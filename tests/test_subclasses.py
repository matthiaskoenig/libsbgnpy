"""
Test Notes and Extensions.
"""

from pathlib import Path

from libsbgnpy import Extension, Language, Notes, libsbgn, utils
from libsbgnpy.examples import extension_example, notes_example


def test_create_notes():
    sbgn = libsbgn.sbgn()
    map = libsbgn.map()
    map.set_language(Language.PD)
    sbgn.set_map(map)

    # create a glyph with an id and class "macromolecule"
    g = libsbgn.glyph()
    g.set_id("g1")

    # define a label for this glyph
    label = libsbgn.label()
    label.set_text("INSR")

    bbox = libsbgn.bbox(x=100, y=100, w=80, h=40)
    g.set_bbox(bbox)
    map.add_glyph(g)

    notes = Notes(
        """
       <body xmlns="http://www.w3.org/1999/xhtml">
           This is an example note describing the INSR glyph.
       </body>"""
    )
    g.set_notes(notes)
    assert g.get_notes() is not None

    notes_str = str(g.get_notes())
    assert "<body" in notes_str


def test_read_notes(tmpdir: Path) -> None:
    sbgn = libsbgn.sbgn()
    map = libsbgn.map()
    map.set_language(Language.PD)
    sbgn.set_map(map)

    text = """
           <body xmlns="http://www.w3.org/1999/xhtml">
               This is an example note describing the map.
           </body>
           """
    notes = Notes(text)
    map.set_notes(notes)
    assert map.get_notes() is not None

    f_sbgn = tmpdir / "test.sbgn"
    utils.write_to_file(sbgn, f_sbgn)
    del map, sbgn, notes

    sbgn2 = utils.read_from_file(f_sbgn)
    _ = utils.write_to_string(sbgn2)

    map2 = sbgn2.get_map()
    notes2 = map2.get_notes()
    assert notes2 is not None
    assert "<body" in str(notes2)

    # assert str(notes2) == text


def test_notes_example(tmpdir: Path) -> None:
    f_sbgn = tmpdir / "test.sbgn"
    notes_example.write_glyph_notes(f_sbgn)
    notes_example.read_glyph_notes(f_sbgn)


def test_create_extension():
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
               <g stroke="Color_2" stroke-width="5" fill="yelloComp"  />
           </style>
           <style idList="glyph1">
               <g stroke="Color_2" stroke-width="5" fill="grayComp"  />
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

    assert map.get_extension() is not None

    extension_str = str(map.get_extension())
    assert "<linearGradient" in extension_str


def test_read_extension(tmpdir: Path) -> None:
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
       </renderInformation>"""
    )

    map.set_extension(extension)
    assert map.get_extension() is not None

    f_sbgn = tmpdir / "test.sbgn"
    utils.write_to_file(sbgn, f_sbgn)
    del map, sbgn, extension

    sbgn = utils.read_from_file(f_sbgn)
    map = sbgn.get_map()
    extension = map.get_extension()
    assert extension is not None
    assert "<colorDefinition" in str(extension)


def test_extension_example(tmpdir: Path) -> None:
    """Test writing and reading of extension example."""
    f_sbgn = tmpdir / "test.sbgn"
    extension_example.write_map_extension(f_sbgn)
    extension_example.read_map_extension(f_sbgn)
