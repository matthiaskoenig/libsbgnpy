"""Test the rules of the SBGN specifications which the schema lacks."""

import logging
from pathlib import Path

import pytest

from libsbgnpy import (
    Arc,
    ArcClass,
    Bbox,
    Glyph,
    GlyphClass,
    Map,
    MapLanguage,
    MapVersion,
    Sbgn,
    check_map,
    check_sbgn,
    map_language,
    read_sbgn_from_string,
    validate,
    write_sbgn_to_file,
)
from libsbgnpy.specification import (
    ARC_CLASSES,
    GLYPH_CLASSES,
    LATEST,
    SPECIFICATIONS,
    map_specification,
)

PD_2_0 = (
    MapVersion.HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_PD_LEVEL_1_VERSION_2_0
)
PD_2_1 = (
    MapVersion.HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_PD_LEVEL_1_VERSION_2_1
)
AF_1_2 = (
    MapVersion.HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_AF_LEVEL_1_VERSION_1_2
)


def _glyph(glyph_id: str, glyph_class: GlyphClass) -> Glyph:
    """Create a glyph with a bounding box."""
    return Glyph(id=glyph_id, class_value=glyph_class, bbox=Bbox(x=0, y=0, w=10, h=10))


def _arc(arc_id: str, arc_class: ArcClass) -> Arc:
    """Create an arc between the glyphs `g1` and `g2`."""
    return Arc(
        id=arc_id,
        class_value=arc_class,
        source="g1",
        target="g2",
        start=Arc.Start(x=0, y=0),
        end=Arc.End(x=10, y=10),
    )


def test_every_version_has_a_specification() -> None:
    """Every version identifier of the schema refers to a specification."""
    assert set(SPECIFICATIONS) == set(MapVersion)


def test_latest() -> None:
    """The latest specifications are PD L1V2.1, ER L1V2.0 and AF L1V1.2."""
    names = {language: SPECIFICATIONS[v].name for language, v in LATEST.items()}
    assert names == {
        MapLanguage.PROCESS_DESCRIPTION: "PD L1V2.1",
        MapLanguage.ENTITY_RELATIONSHIP: "ER L1V2.0",
        MapLanguage.ACTIVITY_FLOW: "AF L1V1.2",
    }


def test_every_class_belongs_to_a_language() -> None:
    """Every glyph and arc class of the schema is used by a language."""
    glyph_classes = set().union(*GLYPH_CLASSES.values())
    assert set(GlyphClass) - glyph_classes == {GlyphClass.OBSERVABLE}
    assert set().union(*ARC_CLASSES.values()) == set(ArcClass)


@pytest.mark.parametrize("version", [PD_2_0, PD_2_1])
def test_read_pd_2(version: MapVersion) -> None:
    """A map of PD L1V2.0 or L1V2.1 is read with its version."""
    sbgn = read_sbgn_from_string(
        '<sbgn xmlns="http://sbgn.org/libsbgn/0.3">'
        f'<map id="m" version="{version.value}"/>'
        "</sbgn>"
    )
    assert sbgn.map[0].version == version
    assert map_language(sbgn.map[0]) == MapLanguage.PROCESS_DESCRIPTION


def test_read_unknown_version_logs(caplog: pytest.LogCaptureFixture) -> None:
    """An unknown version is logged, not raised as a python warning."""
    with caplog.at_level(logging.WARNING, logger="libsbgnpy"):
        sbgn = read_sbgn_from_string(
            '<sbgn xmlns="http://sbgn.org/libsbgn/0.3">'
            '<map id="m" version="http://example.org/sbgn.pd.level-9"/>'
            "</sbgn>"
        )
    assert sbgn.map[0].version == "http://example.org/sbgn.pd.level-9"
    assert "sbgn.pd.level-9" in caplog.text
    assert map_language(sbgn.map[0]) is None
    assert map_specification(sbgn.map[0]) is None


def test_map_language() -> None:
    """The language is taken from the version, else from the language."""
    assert map_language(Map(id="m", version=AF_1_2)) == MapLanguage.ACTIVITY_FLOW
    assert (
        map_language(Map(id="m", language=MapLanguage.ENTITY_RELATIONSHIP))
        == MapLanguage.ENTITY_RELATIONSHIP
    )
    assert map_language(Map(id="m")) is None


def test_check_valid_map() -> None:
    """A map with glyphs and arcs of its language has no errors."""
    map = Map(
        id="m",
        version=PD_2_1,
        language=MapLanguage.PROCESS_DESCRIPTION,
        glyph=[
            _glyph("g1", GlyphClass.SIMPLE_CHEMICAL),
            _glyph("g2", GlyphClass.PROCESS),
        ],
        arc=[_arc("a1", ArcClass.CONSUMPTION)],
    )
    assert check_map(map) == []


def test_check_no_language() -> None:
    """A map needs a version or a language."""
    errors = check_map(Map(id="m"))
    assert len(errors) == 1
    assert "neither 'version' nor 'language'" in errors[0]


def test_check_language_mismatch() -> None:
    """The version and the language name the same language."""
    errors = check_map(Map(id="m", version=PD_2_1, language=MapLanguage.ACTIVITY_FLOW))
    assert len(errors) == 1
    assert "PD L1V2.1" in errors[0]
    assert "activity flow" in errors[0]


def test_check_classes_of_other_language() -> None:
    """Glyphs, nested glyphs and arcs of another language are errors."""
    entity = _glyph("g1", GlyphClass.MACROMOLECULE)
    entity.glyph.append(_glyph("g1.1", GlyphClass.EXISTENCE))
    map = Map(
        id="m",
        version=PD_2_1,
        glyph=[entity, _glyph("g2", GlyphClass.BIOLOGICAL_ACTIVITY)],
        arc=[_arc("a1", ArcClass.POSITIVE_INFLUENCE)],
    )

    errors = check_map(map)
    assert len(errors) == 3
    assert "glyph 'g1.1' has the class 'existence'" in errors[0]
    assert "glyph 'g2' has the class 'biological activity'" in errors[1]
    assert "arc 'a1' has the class 'positive influence'" in errors[2]


def test_check_deprecated_class(caplog: pytest.LogCaptureFixture) -> None:
    """A deprecated class is no error, it is logged."""
    map = Map(id="m", version=AF_1_2, glyph=[_glyph("g1", GlyphClass.PERTURBATION)])
    with caplog.at_level(logging.WARNING, logger="libsbgnpy"):
        assert check_map(map) == []
    assert "deprecated class 'perturbation'" in caplog.text


def test_check_sbgn() -> None:
    """The errors of every map are reported."""
    sbgn = Sbgn(map=[Map(id="m1"), Map(id="m2", version=PD_2_1)])
    errors = check_sbgn(sbgn)
    assert len(errors) == 1
    assert "map 'm1'" in errors[0]


def test_validate(tmp_path: Path) -> None:
    """`validate` reports the errors of the schema and of the specifications."""
    f_sbgn = tmp_path / "map.sbgn"
    map = Map(
        id="m",
        version=PD_2_0,
        glyph=[_glyph("g1", GlyphClass.ENTITY)],
    )
    write_sbgn_to_file(Sbgn(map=[map]), f_sbgn)
    errors = validate(f_sbgn)
    assert len(errors) == 1
    assert "glyph 'g1' has the class 'entity'" in errors[0]


def test_validate_unreadable(tmp_path: Path) -> None:
    """A document which cannot be read reports the schema errors only."""
    f_sbgn = tmp_path / "map.sbgn"
    f_sbgn.write_text("this is not xml", encoding="utf-8")
    assert len(validate(f_sbgn)) == 1
