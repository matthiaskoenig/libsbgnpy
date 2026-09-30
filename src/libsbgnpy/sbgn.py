"""Python bindings of the SBGN-ML schema.

Generated from `libsbgnpy/schema/SBGN.xsd` with
[xsdata](https://github.com/tefra/xsdata) by `scripts/generate_bindings.py`, see
`libsbgnpy/schema/README.md`; do not edit by hand. The classes mirror the
schema, so the
[SBGN specifications](https://sbgn.github.io/specifications)
are the reference for what an element means, and the docstrings are the
documentation of the schema.

An SBGN document is an `Sbgn` holding `Map` objects, a map holds `Glyph` and
`Arc` objects, and every element inherits from `Sbgnbase`, which carries the
`notes` and the `extension`. See the user guide for how they are used.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

__NAMESPACE__ = "http://sbgn.org/libsbgn/0.3"


@dataclass(kw_only=True)
class Sbgnbase:
    """
    The SBGNBase type is the base type of all main components in SBGN.

    It supports attaching notes and extensions to components, with metadata and
    annotations encoded in the extension element.
    """

    class Meta:
        name = "SBGNBase"

    notes: Sbgnbase.Notes | None = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://sbgn.org/libsbgn/0.3",
        },
    )
    extension: Sbgnbase.Extension | None = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://sbgn.org/libsbgn/0.3",
        },
    )

    @dataclass(kw_only=True)
    class Notes:
        """
        The notes element stores notes.
        """

        w3_org_1999_xhtml_element: list[object] = field(
            default_factory=list,
            metadata={
                "type": "Wildcard",
                "namespace": "http://www.w3.org/1999/xhtml",
                "process_contents": "skip",
            },
        )

    @dataclass(kw_only=True)
    class Extension:
        """
        The extension element stores extension information like render information,
        metadata or annotations.
        """

        any_element: list[object] = field(
            default_factory=list,
            metadata={
                "type": "Wildcard",
                "namespace": "##any",
                "process_contents": "skip",
            },
        )


class ArcClass(Enum):
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


class ArcgroupClass(Enum):
    INTERACTION = "interaction"


class EntityName(Enum):
    UNSPECIFIED_ENTITY = "unspecified entity"
    SIMPLE_CHEMICAL = "simple chemical"
    MACROMOLECULE = "macromolecule"
    NUCLEIC_ACID_FEATURE = "nucleic acid feature"
    COMPLEX = "complex"
    PERTURBATION = "perturbation"


class GlyphClass(Enum):
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
    EQUIVALENCE = "equivalence"
    STATE_VARIABLE = "state variable"
    UNIT_OF_INFORMATION = "unit of information"
    ENTITY = "entity"
    OUTCOME = "outcome"
    INTERACTION = "interaction"
    INFLUENCE_TARGET = "influence target"
    ANNOTATION = "annotation"
    VARIABLE_VALUE = "variable value"
    IMPLICIT_XOR = "implicit xor"
    DELAY = "delay"
    EXISTENCE = "existence"
    LOCATION = "location"
    CARDINALITY = "cardinality"
    OBSERVABLE = "observable"


class GlyphOrientation(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


class MapLanguage(Enum):
    ENTITY_RELATIONSHIP = "entity relationship"
    PROCESS_DESCRIPTION = "process description"
    ACTIVITY_FLOW = "activity flow"


class MapVersion(Enum):
    HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_PD_LEVEL_1_VERSION_2_1 = (
        "http://identifiers.org/combine.specifications/sbgn.pd.level-1.version-2.1"
    )
    HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_PD_LEVEL_1_VERSION_2_0 = (
        "http://identifiers.org/combine.specifications/sbgn.pd.level-1.version-2.0"
    )
    HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_PD_LEVEL_1_VERSION_1_3 = (
        "http://identifiers.org/combine.specifications/sbgn.pd.level-1.version-1.3"
    )
    HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_PD_LEVEL_1_VERSION_1_2 = (
        "http://identifiers.org/combine.specifications/sbgn.pd.level-1.version-1.2"
    )
    HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_PD_LEVEL_1_VERSION_1_1 = (
        "http://identifiers.org/combine.specifications/sbgn.pd.level-1.version-1.1"
    )
    HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_PD_LEVEL_1_VERSION_1_0 = (
        "http://identifiers.org/combine.specifications/sbgn.pd.level-1.version-1.0"
    )
    HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_PD_LEVEL_1_VERSION_1 = (
        "http://identifiers.org/combine.specifications/sbgn.pd.level-1.version-1"
    )
    HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_ER_LEVEL_1_VERSION_2 = (
        "http://identifiers.org/combine.specifications/sbgn.er.level-1.version-2"
    )
    HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_ER_LEVEL_1_VERSION_1_2 = (
        "http://identifiers.org/combine.specifications/sbgn.er.level-1.version-1.2"
    )
    HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_ER_LEVEL_1_VERSION_1_1 = (
        "http://identifiers.org/combine.specifications/sbgn.er.level-1.version-1.1"
    )
    HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_ER_LEVEL_1_VERSION_1_0 = (
        "http://identifiers.org/combine.specifications/sbgn.er.level-1.version-1.0"
    )
    HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_ER_LEVEL_1_VERSION_1 = (
        "http://identifiers.org/combine.specifications/sbgn.er.level-1.version-1"
    )
    HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_AF_LEVEL_1_VERSION_1_2 = (
        "http://identifiers.org/combine.specifications/sbgn.af.level-1.version-1.2"
    )
    HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_AF_LEVEL_1_VERSION_1_0 = (
        "http://identifiers.org/combine.specifications/sbgn.af.level-1.version-1.0"
    )
    HTTP_IDENTIFIERS_ORG_COMBINE_SPECIFICATIONS_SBGN_AF_LEVEL_1_VERSION_1 = (
        "http://identifiers.org/combine.specifications/sbgn.af.level-1.version-1"
    )


@dataclass(kw_only=True)
class Bbox(Sbgnbase):
    """
    The bbox element describes a rectangle.

    This rectangle is defined by: PointAttributes corresponding to the 2D
    coordinates of the top left corner, width and height attributes. The rectangle
    corresponds to the outer bounding box of a shape. The shape itself can be
    irregular (for instance in the case of some compartments). In the case of
    process nodes, the bounding box only concerns the central glyph (square, or
    circle), the input/output ports are not included, and neither are the lines
    connecting them to the central glyph. A bbox is required for all glyphs, and is
    optional for labels.
    """

    class Meta:
        name = "bbox"
        namespace = "http://sbgn.org/libsbgn/0.3"

    x: float = field(
        metadata={
            "type": "Attribute",
        }
    )
    y: float = field(
        metadata={
            "type": "Attribute",
        }
    )
    w: float = field(
        metadata={
            "type": "Attribute",
        }
    )
    h: float = field(
        metadata={
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class Point(Sbgnbase):
    """
    The point element is characterized by PointAttributes, which describe absolute
    2D cartesian coordinates.

    Namely: x (horizontal, from left to right), y (vertical, from top to bottom).
    The origin is located in the top-left corner of the map. There is no unit:
    proportions must be preserved, but the maps can be drawn at any scale. In the
    test files examples, to obtain a drawing similar to the reference *.png file,
    values in the corresponding *.sbgn file should be read as pixels.
    """

    class Meta:
        name = "point"
        namespace = "http://sbgn.org/libsbgn/0.3"

    x: float = field(
        metadata={
            "type": "Attribute",
        }
    )
    y: float = field(
        metadata={
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class Port(Sbgnbase):
    """
    The port element describes an anchor point to which arcs can refer as a source
    or target.

    It consists of: absolute 2D cartesian coordinates (PointAttribute), a unique id
    attribute. Two port elements are required for process nodes. They represent the
    extremity of the two "arms" which protrude on both sides of the core of the
    glyph (= square or circle shape). Other glyphs don't need ports (but can use
    them if desired).

    Attributes:
        x:
        y:
        id: The xsd:ID type is an alphanumeric identifier, starting with a
            letter. Port IDs often contain the ID of their glyph, followed by a
            local port number (e.g. glyph4.1, glyph4.2, etc.) However, this style
            convention is not mandatory, and IDs should never be interpreted as
            carrying any meaning.
    """

    class Meta:
        name = "port"
        namespace = "http://sbgn.org/libsbgn/0.3"

    x: float = field(
        metadata={
            "type": "Attribute",
        }
    )
    y: float = field(
        metadata={
            "type": "Attribute",
        }
    )
    id: str = field(
        metadata={
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class Label(Sbgnbase):
    """
    The label element describes the text accompanying a glyph.

    The text attribute is mandatory. Its position can be specified by a bbox
    (optional). Tools are free to display the text in any style (font, font-size,
    etc.).

    Attributes:
        bbox:
        text: Multi-line labels are allowed. Line breaks are encoded as &amp;#xA;
            as specified by the XML standard.
    """

    class Meta:
        name = "label"
        namespace = "http://sbgn.org/libsbgn/0.3"

    bbox: Bbox | None = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    text: str = field(
        metadata={
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class Glyph(Sbgnbase):
    """
    The glyph element is: either a stand-alone, high-level SBGN glyph (EPN, PN,
    compartment, etc), or a sub-glyph (state variable, unit of information, inside
    of a complex, ...) In the first case, it appears directly in the glyph list of
    the map.

    In the second case, it is a child of another glyph element.

    Attributes:
        label:
        state: The state element should only be used for state variables. It
            replaces the label element used for other glyphs. It describes the
            text to be drawn inside the state variable. A state must have a
            value, a variable, or both. If it has both, they are rendered as a
            concatenated string with @ in between.
        clone: The clone element (which is optional) means the glyph carries a
            clone marker. It can contain an optional label.
        callout: The callout element is only used for glyphs with class
            annotation. It contains the coordinate of the point where the
            annotation points to, as well as a reference to the element that is
            pointed to.
        entity: The entity is only used in activity flow diagrams. It can only be
            used on a unit of information glyph on a biological activity glyph,
            where it is compulsory. It is used to indicate the shape of this unit
            of information.
        bbox: The bbox element is mandatory and unique: exactly one per glyph. It
            defines the outer bounding box of the glyph. The actual shape of the
            glyph can be irregular (for instance in the case of some
            compartments) In the case of process nodes, the bounding box only
            concerns the central glyph (square, or circle): the input/output
            ports are not included, and neither are the lines connecting them to
            the central glyph.
        glyph: A glyph element can contain any number of children glyph elements.
            In practice, this should only happen in the following cases: a
            compartment with unit of information children, an EPN with states
            variables and/or unit of information children, a complex, with state
            variables, unit of info, and/or EPN children.
        port:
        class_value: The class attribute defines the semantic of the glyph, and
            influences: the way that glyph should be rendered, the overall
            syntactic validity of the map. The various classes encompass the
            following PD SBGN elements: Entity Pool Nodes (EPN), Process Nodes
            (PN), Logic Operator Nodes, Sub-glyphs on Nodes (State Variable, Unit
            of Information), Sub-glyphs on Arcs (Stoichiometry Label), Other
            glyphs (Compartment, Submap, Tag, Terminal). And the following ER
            SBGN elements Entities (Entity, Outcome) Other (Annotation,
            Phenotype) Auxiliary on glyps (Existence, Location) Auxiliary on arcs
            (Cardinality) Delay operator implicit xor
        orientation: The orientation attribute is used to express how to draw
            asymmetric glyphs. In PD, the orientation of Process Nodes is either
            horizontal or vertical. It refers to an (imaginary) line connecting
            the two in/out sides of the PN. In PD, the orientation of Tags and
            Terminals can be left, right, up or down. It refers to the direction
            the arrow side of the glyph is pointing at.
        id: The xsd:ID type is an alphanumeric identifier, starting with a
            letter. It is recommended to generate meaningless IDs (e.g.
            "glyph1234") and avoid IDs with a meaning (e.g. "epn_ethanol")
        compartment_ref: Reference to the ID of the compartment that this glyph
            is part of. Only use this if there is at least one explicit
            compartment present in the diagram. Compartments are only used in PD
            and AF, and thus this attribute as well. For PD, this should be used
            only for EPN's. For AF, this should be used only for Activity Nodes.
            In case there are no compartments, entities that can have a location,
            such as EPN's, are implicit member of an invisible compartment that
            encompasses the whole map. In that case, this attribute must be
            omitted.
        compartment_order: The compartment order attribute can be used to define
            a drawing order for compartments. It enables tools to draw
            compartments in the correct order especially in the case of
            overlapping compartments. Compartments are only used in PD and AF,
            and thus this attribute as well. The attribute is of type float, the
            attribute value has not to be unique. Compartments with higher
            compartment order are drawn on top. The attribute is optional and
            should only be used for compartments.
        map_ref: This attribute is only used on a submap glyph. It is required.
            Reference to the ID of the map which provides the content of the
            submap. If no map is available providing the content of the submap an
            omitted process should be used instead of the submap. Submaps are
            only used in PD and AF, and thus this attribute as well.
        tag_ref: This attribute is only used on a terminal glyph. It is required.
            Reference to the ID of a tag on a map providing the content of a
            submap. The terminal glyph is defined as sub-glyph of this submap.
            Submaps and therefore terminals are only used in PD and AF, and thus
            this attribute as well.
    """

    class Meta:
        name = "glyph"
        namespace = "http://sbgn.org/libsbgn/0.3"

    label: Label | None = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    state: Glyph.State | None = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    clone: Glyph.Clone | None = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    callout: Glyph.Callout | None = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    entity: Glyph.Entity | None = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    bbox: Bbox = field(
        metadata={
            "type": "Element",
        }
    )
    glyph: list[Glyph] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    port: list[Port] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    class_value: GlyphClass = field(
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    orientation: GlyphOrientation = field(
        default=GlyphOrientation.HORIZONTAL,
        metadata={
            "type": "Attribute",
        },
    )
    id: str = field(
        metadata={
            "type": "Attribute",
        }
    )
    compartment_ref: str | None = field(
        default=None,
        metadata={
            "name": "compartmentRef",
            "type": "Attribute",
        },
    )
    compartment_order: float | None = field(
        default=None,
        metadata={
            "name": "compartmentOrder",
            "type": "Attribute",
        },
    )
    map_ref: str | None = field(
        default=None,
        metadata={
            "name": "mapRef",
            "type": "Attribute",
        },
    )
    tag_ref: str | None = field(
        default=None,
        metadata={
            "name": "tagRef",
            "type": "Attribute",
        },
    )

    @dataclass(kw_only=True)
    class Clone:
        label: Label | None = field(
            default=None,
            metadata={
                "type": "Element",
            },
        )

    @dataclass(kw_only=True)
    class Callout:
        point: Point = field(
            metadata={
                "type": "Element",
            }
        )
        target: str | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class Entity:
        name: EntityName = field(
            metadata={
                "type": "Attribute",
            }
        )

    @dataclass(kw_only=True)
    class State:
        """
        Attributes:
            value: The value attribute represents the state of the variable. It
                can be: either from a predefined set of string (P, S, etc.) which
                correspond to specific SBO terms (cf. SBGN specs), or any
                arbitrary string.
            variable: The variable attribute describes the site where the
                modification described by the value attribute occurs. It is:
                optional when there is only one state variable on the parent EPN,
                required when there is more than one state variable the parent
                EPN.
        """

        value: str | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )
        variable: str | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )


@dataclass(kw_only=True)
class Arc(Sbgnbase):
    """
    The arc element describes an SBGN arc between two SBGN nodes.

    It contains: For PD: an optional stoichiometry marker, For ER: an optional
    cardinality marker, zero or more ports (influence targets), and zero or more
    outcomes, a mandatory source and target (glyph or port), a geometric description
    of its whole path, from start to end. This path can involve any number of
    straight lines or quadratic/cubic Bezier curves.

    Attributes:
        glyph: In PD, an arc can contain a single optional sub-glyph. This glyph
            must be a stoichiometry marker (square with a numeric label) In ER,
            an arc can contain several sub-glyphs. This can be zero or one
            cardinality glyphs (e.g. cis or trans), plus zero to many outcome
            glyphs (black dot)
        port: Ports are only allowed in ER.
        start: The start element represents the starting point of the arc's path.
            It is unique and mandatory.
        next: The next element represents the next point in the arc's path.
            Between the start and the end of the path, there can be any number
            (even zero) of next elements (intermediate points). They are read
            consecutively: start, next, next, ..., next, end. When the path from
            the previous point to this point is not straight, this element also
            contains a list of control points (between 1 and 2) describing a
            Bezier curve (quadratic if 1 control point, cubic if 2) between the
            previous point and this point.
        end: The end element represents the ending point of the arc's path. It is
            unique and mandatory. When the path from the previous point to this
            point is not straight, this element also contains a list of control
            points (between 1 and 2) describing a Bezier curve (quadratic if 1
            control point, cubic if 2) between the previous point and this point.
        class_value: The class attribute defines the semantic of the arc, and
            influences: the way that arc should be rendered, the overall
            syntactic validity of the map. The various classes encompass all
            possible types of SBGN arcs: production and consumption arcs, all
            types of modification arcs, logic arcs, equivalence arcs. To express
            a reversible reaction, use production arcs on both sides of the
            Process Node.
        id: The xsd:ID type is an alphanumeric identifier, starting with a
            letter.
        source: The source attribute can refer: either to the id of a glyph, or
            to the id of a port on a glyph.
        target: The target attribute can refer: either to the id of a glyph, or
            to the id of a port on a glyph.
    """

    class Meta:
        name = "arc"
        namespace = "http://sbgn.org/libsbgn/0.3"

    glyph: list[Glyph] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    port: list[Port] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    start: Arc.Start = field(
        metadata={
            "type": "Element",
        }
    )
    next: list[Arc.Next] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    end: Arc.End = field(
        metadata={
            "type": "Element",
        }
    )
    class_value: ArcClass = field(
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    id: str = field(
        metadata={
            "type": "Attribute",
        }
    )
    source: str = field(
        metadata={
            "type": "Attribute",
        }
    )
    target: str = field(
        metadata={
            "type": "Attribute",
        }
    )

    @dataclass(kw_only=True)
    class Start:
        x: float = field(
            metadata={
                "type": "Attribute",
            }
        )
        y: float = field(
            metadata={
                "type": "Attribute",
            }
        )

    @dataclass(kw_only=True)
    class Next:
        point: list[Point] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "max_occurs": 2,
            },
        )
        x: float = field(
            metadata={
                "type": "Attribute",
            }
        )
        y: float = field(
            metadata={
                "type": "Attribute",
            }
        )

    @dataclass(kw_only=True)
    class End:
        point: list[Point] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "max_occurs": 2,
            },
        )
        x: float = field(
            metadata={
                "type": "Attribute",
            }
        )
        y: float = field(
            metadata={
                "type": "Attribute",
            }
        )


@dataclass(kw_only=True)
class Arcgroup(Sbgnbase):
    """
    The arc group describes a set of arcs and glyphs that together have a relation.

    For example For ER: interaction arcs around an interaction glyph, ... Note that,
    in spite of the name, an arcgroup contains both arcs and glyphs.

    Attributes:
        glyph: An arcgroup can contain glyphs. For example, in an interaction
            arcgroup, there must be one interaction glyph.
        arc: An arcgroup can have multiple arcs. They are all assumed to form a
            single hyperarc-like structure.
        class_value: The class attribute defines the semantic of the arcgroup.
    """

    class Meta:
        name = "arcgroup"
        namespace = "http://sbgn.org/libsbgn/0.3"

    glyph: list[Glyph] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    arc: list[Arc] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    class_value: ArcgroupClass = field(
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class Map(Sbgnbase):
    """
    The map element describes a single SBGN PD map.

    It contains a list of glyph elements and a list of arc elements. These lists can
    be of any size (possibly empty).

    Attributes:
        bbox: The bbox element on a map is not mandatory, it allows the
            application to define a canvas, and at the same time define a
            whitespace margin around the glyphs. If a bbox is defined on a map,
            all glyphs and arcs must be inside this bbox, otherwise they could be
            clipped off by applications.
        glyph:
        arc:
        arcgroup:
        version: Version of the map: URI identifier that gives the language,
            level and version defined by SBGN. Different
            languages/levels/versions have different restrictions on the usage of
            sub-elements (that are not encoded in this schema but must be
            validated with an external validator)
        language: Language of the map: one of three sublanguages defined by SBGN.
            Different languages have different restrictions on the usage of sub-
            elements (that are not encoded in this schema but must be validated
            with an external validator)
        id: The xsd:ID type is an alphanumeric identifier, starting with a
            letter. It is recommended to generate meaningless IDs (e.g.
            "map1234") and avoid IDs with a meaning (e.g. "MAPK cascade")
    """

    class Meta:
        name = "map"
        namespace = "http://sbgn.org/libsbgn/0.3"

    bbox: Bbox | None = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    glyph: list[Glyph] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    arc: list[Arc] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    arcgroup: list[Arcgroup] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    version: MapVersion | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    language: MapLanguage | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: str = field(
        metadata={
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class Sbgn(Sbgnbase):
    """
    The sbgn element is the root of any SBGNML document.

    Currently each document must contain exactly one map element.
    """

    class Meta:
        name = "sbgn"
        namespace = "http://sbgn.org/libsbgn/0.3"

    map: list[Map] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
