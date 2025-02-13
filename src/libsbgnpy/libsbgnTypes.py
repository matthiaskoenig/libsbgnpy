# -*- coding: utf-8 -*-
"""
Definition of Language, GlyphClass and ArcClass types.
Created manually from schema file.
"""

from enum import Enum, unique


@unique
class Language(Enum):
    """
    Enum representing the three languages of SBGN.
    """

    AF = "activity flow"
    ER = "entity relationship"
    PD = "process description"


@unique
class Orientation(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    UP = "up"
    DOWN = "down"
    RIGHT = "right"
    LEFT = "left"


@unique
class GlyphClass(Enum):
    """
    Enumeration with all possible values for the class attribute of Glyphs in SBGN-ML.
    This includes both top-level glyphs and sub-glyphs.
    """

    # glyphs
    UNSPECIFIED_ENTITY = "unspecified entity"
    SIMPLE_CHEMICAL = "simple chemical"
    MACROMOLECULE = "macromolecule"
    NUCLEIC_ACID_FEATURE = "nucleic acid feature"
    SIMPLE_CHEMICAL_MULTIMER = "simple chemical multimer"
    MACROMOLECULE_MULTIMER = "macromolecule multimer"
    NUCLEIC_ACID_FEATURE_MULTIMER = "nucleic acid feature multimer"
    COMPLEX = "complex"
    COMPLEX_MULTIMER = "complex multimer"
    SOURCE_AND_SINK = "source and sink"
    PERTURBATION = "perturbation"
    BIOLOGICAL_ACTIVITY = "biological activity"
    PERTURBING_AGENT = "perturbing agent"
    COMPARTMENT = "compartment"
    SUBMAP = "submap"
    TAG = "tag"
    TERMINAL = "terminal"
    PROCESS = "process"
    OMITTED_PROCESS = "omitted process"
    UNCERTAIN_PROCESS = "uncertain process"
    ASSOCIATION = "association"
    DISSOCIATION = "dissociation"
    PHENOTYPE = "phenotype"
    AND = "and"
    OR = "or"
    NOT = "not"
    STATE_VARIABLE = "state variable"
    UNIT_OF_INFORMATION = "unit of information"

    # @deprecated
    # By mistake, we used STOICHIOMETRY in instead of {@link CARDINALITY} in LibSBGN M1.
    # We keep this constant here to support reading old documents.
    # This constant will be removed in LibSBGN M3.
    STOICHIOMETRY = "stoichiometry"
    ENTITY = "entity"
    OUTCOME = "outcome"

    # @deprecated
    # Observable was used in old versions of SBGN, but has been replaced with {@link PHENOTYPE}.
    # However, because older versions of SBGN are supported by LibSBGN, this constant will never be removed.
    OBSERVABLE = "observable"
    INTERACTION = "interaction"
    ANNOTATION = "annotation"
    VARIABLE_VALUE = "variable value"
    IMPLICIT_XOR = "implicit xor"
    DELAY = "delay"
    EXISTENCE = "existence"
    LOCATION = "location"
    CARDINALITY = "cardinality"


@unique
class ArcClass(Enum):
    """
    Enumeration with all possible values for the class attribute of Arcs in SBGN-ML.
    """

    # arcs
    PRODUCTION = "production"
    CONSUMPTION = "consumption"
    CATALYSIS = "catalysis"
    MODULATION = "modulation"
    STIMULATION = "stimulation"
    INHIBITION = "inhibition"
    ASSIGNMENT = "assignment"
    INTERACTION = "interaction"
    ABSOLUTE_INHIBITION = "absolute inhibition"
    ABSOLUTE_STIMULATION = "absolute stimulation"
    POSITIVE_INFLUENCE = "positive influence"
    NEGATIVE_INFLUENCE = "negative influence"
    UNKNOWN_INFLUENCE = "unknown influence"
    EQUIVALENCE_ARC = "equivalence arc"
    NECESSARY_STIMULATION = "necessary stimulation"
    LOGIC_ARC = "logic arc"
