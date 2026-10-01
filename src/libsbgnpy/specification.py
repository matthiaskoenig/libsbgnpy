"""The SBGN specifications: versions, vocabularies and the checks beyond the schema.

The SBGN-ML schema has a single enumeration of glyph classes and of arc classes
for all three languages, it does not know which classes belong to which
language, and it cannot express that a map declares its language. This module
holds what the specifications add on top of the schema:

- the specification every `MapVersion` refers to, see `SPECIFICATIONS`, and the
  latest specification of every language, see `LATEST`,
- the glyph and arc classes of every language, see `GLYPH_CLASSES` and
  `ARC_CLASSES`, and the classes which are deprecated, see
  `DEPRECATED_GLYPH_CLASSES`,
- the language of a map, which is given by its `version` or by its deprecated
  `language`, see `map_language`,
- the check of a document against these rules, see `check_sbgn`.

```python
from pathlib import Path

from libsbgnpy import check_sbgn, read_sbgn_from_file

sbgn = read_sbgn_from_file(Path("map.sbgn"))
for error in check_sbgn(sbgn):
    print(error)
```

The validation rules of the language specifications, e.g., which arcs may
connect which glyphs, are not checked.
"""

import logging
from dataclasses import dataclass

from libsbgnpy.sbgn import (
    Arc,
    ArcClass,
    Glyph,
    GlyphClass,
    Map,
    MapLanguage,
    MapVersion,
    Sbgn,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class Specification:
    """A specification of an SBGN language.

    Attributes:
        language: the language the specification defines.
        level: the level of the specification.
        version: the version of the specification, `"1"` stands for the latest
            version 1.x at the time the identifier was registered.
        year: the year the specification was published, None for `"1"`.
        doi: the DOI of the journal publication, None for the versions which
            were only published as a preprint.
    """

    language: MapLanguage
    level: int
    version: str
    year: int | None = None
    doi: str | None = None

    @property
    def name(self) -> str:
        """Short name of the specification, e.g., `"PD L1V2.1"`."""
        return f"{LANGUAGE_ABBREVIATIONS[self.language]} L{self.level}V{self.version}"


#: short name of every language
LANGUAGE_ABBREVIATIONS: dict[MapLanguage, str] = {
    MapLanguage.PROCESS_DESCRIPTION: "PD",
    MapLanguage.ENTITY_RELATIONSHIP: "ER",
    MapLanguage.ACTIVITY_FLOW: "AF",
}

_PD = MapLanguage.PROCESS_DESCRIPTION
_ER = MapLanguage.ENTITY_RELATIONSHIP
_AF = MapLanguage.ACTIVITY_FLOW
_V = MapVersion

#: the specification every version identifier of a map refers to
SPECIFICATIONS: dict[MapVersion, Specification] = {
    _V.HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_PD_LEVEL_1_VERSION_2_1: (
        Specification(
            language=_PD, level=1, version="2.1", year=2026, doi="10.1515/jib-2025-0018"
        )
    ),
    _V.HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_PD_LEVEL_1_VERSION_2_0: (
        Specification(
            language=_PD, level=1, version="2.0", year=2019, doi="10.1515/jib-2019-0022"
        )
    ),
    _V.HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_PD_LEVEL_1_VERSION_1_3: (
        Specification(
            language=_PD,
            level=1,
            version="1.3",
            year=2015,
            doi="10.2390/biecoll-jib-2015-263",
        )
    ),
    _V.HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_PD_LEVEL_1_VERSION_1_2: (
        Specification(language=_PD, level=1, version="1.2", year=2010)
    ),
    _V.HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_PD_LEVEL_1_VERSION_1_1: (
        Specification(language=_PD, level=1, version="1.1", year=2009)
    ),
    _V.HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_PD_LEVEL_1_VERSION_1_0: (
        Specification(language=_PD, level=1, version="1.0", year=2008)
    ),
    _V.HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_PD_LEVEL_1_VERSION_1: (
        Specification(language=_PD, level=1, version="1")
    ),
    _V.HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_ER_LEVEL_1_VERSION_2: (
        Specification(
            language=_ER,
            level=1,
            version="2.0",
            year=2015,
            doi="10.2390/biecoll-jib-2015-264",
        )
    ),
    _V.HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_ER_LEVEL_1_VERSION_1_2: (
        Specification(language=_ER, level=1, version="1.2", year=2011)
    ),
    _V.HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_ER_LEVEL_1_VERSION_1_1: (
        Specification(language=_ER, level=1, version="1.1", year=2010)
    ),
    _V.HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_ER_LEVEL_1_VERSION_1_0: (
        Specification(language=_ER, level=1, version="1.0", year=2009)
    ),
    _V.HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_ER_LEVEL_1_VERSION_1: (
        Specification(language=_ER, level=1, version="1")
    ),
    _V.HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_AF_LEVEL_1_VERSION_1_2: (
        Specification(
            language=_AF,
            level=1,
            version="1.2",
            year=2015,
            doi="10.2390/biecoll-jib-2015-265",
        )
    ),
    _V.HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_AF_LEVEL_1_VERSION_1_0: (
        Specification(language=_AF, level=1, version="1.0", year=2009)
    ),
    _V.HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_AF_LEVEL_1_VERSION_1: (
        Specification(language=_AF, level=1, version="1")
    ),
}

#: the version identifier of the latest specification of every language
LATEST: dict[MapLanguage, MapVersion] = {
    _PD: _V.HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_PD_LEVEL_1_VERSION_2_1,
    _ER: _V.HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_ER_LEVEL_1_VERSION_2,
    _AF: _V.HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_AF_LEVEL_1_VERSION_1_2,
}

_G = GlyphClass

#: the glyph classes of every language, auxiliary units included; the empty set
#: of PD L1V2.0 is the glyph class `source and sink`
GLYPH_CLASSES: dict[MapLanguage, frozenset[GlyphClass]] = {
    _PD: frozenset(
        {
            # entity pool nodes
            _G.UNSPECIFIED_ENTITY,
            _G.SIMPLE_CHEMICAL,
            _G.MACROMOLECULE,
            _G.NUCLEIC_ACID_FEATURE,
            _G.SIMPLE_CHEMICAL_MULTIMER,
            _G.MACROMOLECULE_MULTIMER,
            _G.NUCLEIC_ACID_FEATURE_MULTIMER,
            _G.COMPLEX,
            _G.COMPLEX_MULTIMER,
            _G.SOURCE_AND_SINK,
            _G.PERTURBING_AGENT,
            # process nodes
            _G.PROCESS,
            _G.OMITTED_PROCESS,
            _G.UNCERTAIN_PROCESS,
            _G.ASSOCIATION,
            _G.DISSOCIATION,
            _G.PHENOTYPE,
            # logical operator nodes
            _G.AND,
            _G.OR,
            _G.NOT,
            _G.EQUIVALENCE,
            # containers, references and encapsulation
            _G.COMPARTMENT,
            _G.TAG,
            _G.SUBMAP,
            _G.TERMINAL,
            # auxiliary units and annotations
            _G.STATE_VARIABLE,
            _G.UNIT_OF_INFORMATION,
            _G.CARDINALITY,
            _G.ANNOTATION,
        }
    ),
    _ER: frozenset(
        {
            # interactors
            _G.ENTITY,
            _G.OUTCOME,
            _G.PERTURBING_AGENT,
            # relationships
            _G.INTERACTION,
            _G.INFLUENCE_TARGET,
            _G.PHENOTYPE,
            # logical operators
            _G.AND,
            _G.OR,
            _G.NOT,
            _G.DELAY,
            _G.IMPLICIT_XOR,
            # auxiliary units and annotations
            _G.STATE_VARIABLE,
            _G.EXISTENCE,
            _G.LOCATION,
            _G.VARIABLE_VALUE,
            _G.UNIT_OF_INFORMATION,
            _G.CARDINALITY,
            _G.ANNOTATION,
        }
    ),
    _AF: frozenset(
        {
            # activity nodes
            _G.BIOLOGICAL_ACTIVITY,
            _G.PHENOTYPE,
            _G.PERTURBATION,
            # logical operators
            _G.AND,
            _G.OR,
            _G.NOT,
            _G.DELAY,
            # containers, references and encapsulation
            _G.COMPARTMENT,
            _G.TAG,
            _G.SUBMAP,
            _G.TERMINAL,
            # auxiliary units and annotations
            _G.UNIT_OF_INFORMATION,
            _G.ANNOTATION,
        }
    ),
}

#: glyph classes which are still allowed, but deprecated: the perturbation of
#: AF is a unit of information since AF L1V1.2 and SBGN-ML 0.3, observable is
#: a class of the earliest drafts of SBGN
DEPRECATED_GLYPH_CLASSES: dict[MapLanguage, frozenset[GlyphClass]] = {
    _PD: frozenset({_G.OBSERVABLE}),
    _ER: frozenset({_G.OBSERVABLE}),
    _AF: frozenset({_G.PERTURBATION, _G.OBSERVABLE}),
}

_A = ArcClass

#: the arc classes of every language
ARC_CLASSES: dict[MapLanguage, frozenset[ArcClass]] = {
    _PD: frozenset(
        {
            _A.CONSUMPTION,
            _A.PRODUCTION,
            _A.MODULATION,
            _A.STIMULATION,
            _A.CATALYSIS,
            _A.INHIBITION,
            _A.NECESSARY_STIMULATION,
            _A.LOGIC_ARC,
            _A.EQUIVALENCE_ARC,
        }
    ),
    _ER: frozenset(
        {
            _A.INTERACTION,
            _A.ASSIGNMENT,
            _A.MODULATION,
            _A.STIMULATION,
            _A.INHIBITION,
            _A.NECESSARY_STIMULATION,
            _A.ABSOLUTE_STIMULATION,
            _A.ABSOLUTE_INHIBITION,
            _A.LOGIC_ARC,
        }
    ),
    _AF: frozenset(
        {
            _A.POSITIVE_INFLUENCE,
            _A.NEGATIVE_INFLUENCE,
            _A.UNKNOWN_INFLUENCE,
            _A.NECESSARY_STIMULATION,
            _A.LOGIC_ARC,
            _A.EQUIVALENCE_ARC,
        }
    ),
}


def map_language(map: Map) -> MapLanguage | None:
    """Get the language of a map.

    SBGN-ML 0.3 deprecated the `language` of a map in favour of its `version`,
    which names the language together with the level and the version of its
    specification. The language is therefore taken from the version, and from
    the deprecated language if the map has no version.

    Args:
        map: the map.

    Returns:
        The language of the map, None if neither its version nor its language
        is a known value.
    """
    return language_of(map.version, map.language)


def language_of(
    version: MapVersion | str | None, language: MapLanguage | str | None
) -> MapLanguage | None:
    """Get the language of a map from its version and its language.

    The rule of [`map_language`][libsbgnpy.specification.map_language] for the
    values of the attributes, e.g., as they are in a document which is not
    bound: the language is taken from the version, else from the language.

    Args:
        version: the version of the map, a member of `MapVersion` or its value.
        language: the language of the map, a member of `MapLanguage` or its
            value.

    Returns:
        The language, None if neither the version nor the language is a known
        value.
    """
    try:
        return SPECIFICATIONS[MapVersion(version)].language
    except ValueError:
        pass
    try:
        return MapLanguage(language)
    except ValueError:
        return None


def map_specification(map: Map) -> Specification | None:
    """Get the specification a map refers to with its version.

    Args:
        map: the map.

    Returns:
        The specification, None if the map has no known version.
    """
    if isinstance(map.version, MapVersion):
        return SPECIFICATIONS[map.version]
    return None


def check_map(map: Map) -> list[str]:
    """Check a map against the rules of the specifications the schema lacks.

    The checks are:

    - the map declares its language with a `version` or a `language`, one of
      them is required by SBGN-ML 0.3,
    - the `version` and the `language` name the same language,
    - every glyph and every arc has a class of the language of the map.

    Classes which are deprecated are allowed, they are logged as a warning.
    Unknown values of an enumeration are errors of the schema and not
    repeated here, see [`validate_xsd`][libsbgnpy.validator.validate_xsd].

    Args:
        map: the map.

    Returns:
        The errors, empty if the map follows the rules.
    """
    errors: list[str] = []
    name = f"map '{map.id}'"
    if map.version is None and map.language is None:
        errors.append(
            f"{name}: neither 'version' nor 'language' is set, "
            "SBGN-ML 0.3 requires one of them"
        )
    if isinstance(map.version, MapVersion) and isinstance(map.language, MapLanguage):
        specification = SPECIFICATIONS[map.version]
        if specification.language != map.language:
            errors.append(
                f"{name}: 'version' is {specification.name}, "
                f"but 'language' is '{map.language.value}'"
            )

    language = map_language(map)
    if language is None:
        return errors

    for glyph in _glyphs(map):
        glyph_class = glyph.class_value
        if not isinstance(glyph_class, GlyphClass):
            continue
        if glyph_class in DEPRECATED_GLYPH_CLASSES[language]:
            logger.warning(
                "%s: glyph '%s' has the deprecated class '%s'",
                name,
                glyph.id,
                glyph_class.value,
            )
        elif glyph_class not in GLYPH_CLASSES[language]:
            errors.append(
                f"{name}: glyph '{glyph.id}' has the class '{glyph_class.value}', "
                f"which is no glyph class of {language.value}"
            )
    for arc in _arcs(map):
        arc_class = arc.class_value
        if not isinstance(arc_class, ArcClass):
            continue
        if arc_class not in ARC_CLASSES[language]:
            errors.append(
                f"{name}: arc '{arc.id}' has the class '{arc_class.value}', "
                f"which is no arc class of {language.value}"
            )
    return errors


def check_sbgn(sbgn: Sbgn) -> list[str]:
    """Check every map of a document, see `check_map`.

    Args:
        sbgn: the SBGN document.

    Returns:
        The errors, empty if all maps follow the rules.
    """
    return [error for map in sbgn.map for error in check_map(map)]


def _glyphs(map: Map) -> list[Glyph]:
    """Collect every glyph of a map.

    Glyphs are nested in glyphs (content and auxiliary units), in arcs
    (cardinality, outcome) and in arc groups (interaction).

    Args:
        map: the map.

    Returns:
        The glyphs in document order.
    """
    glyphs: list[Glyph] = []

    def visit(glyph: Glyph) -> None:
        glyphs.append(glyph)
        for child in glyph.glyph:
            visit(child)

    def visit_arc(arc: Arc) -> None:
        for child in arc.glyph:
            visit(child)

    for glyph in map.glyph:
        visit(glyph)
    for arc in map.arc:
        visit_arc(arc)
    for arcgroup in map.arcgroup:
        for glyph in arcgroup.glyph:
            visit(glyph)
        for arc in arcgroup.arc:
            visit_arc(arc)
    return glyphs


def _arcs(map: Map) -> list[Arc]:
    """Collect every arc of a map, the arcs of the arc groups included.

    Args:
        map: the map.

    Returns:
        The arcs in document order.
    """
    arcs: list[Arc] = list(map.arc)
    for arcgroup in map.arcgroup:
        arcs.extend(arcgroup.arc)
    return arcs
