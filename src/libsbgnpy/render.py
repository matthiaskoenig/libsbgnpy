from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "http://www.sbml.org/sbml/level3/version1/render/version1"


@dataclass
class ColorDefinition:
    class Meta:
        name = "colorDefinition"
        namespace = "http://www.sbml.org/sbml/level3/version1/render/version1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
            "required": True,
        },
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
            "required": True,
        },
    )


@dataclass
class G:
    class Meta:
        name = "g"
        namespace = "http://www.sbml.org/sbml/level3/version1/render/version1"

    stroke: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    stroke_width: Optional[float] = field(
        default=None,
        metadata={
            "name": "stroke-width",
            "type": "Attribute",
            "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    fill: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    fill_rule: Optional[str] = field(
        default=None,
        metadata={
            "name": "fill-rule",
            "type": "Attribute",
            "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    font_family: Optional[str] = field(
        default=None,
        metadata={
            "name": "font-family",
            "type": "Attribute",
            "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    font_weight: Optional[str] = field(
        default=None,
        metadata={
            "name": "font-weight",
            "type": "Attribute",
            "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    font_style: Optional[str] = field(
        default=None,
        metadata={
            "name": "font-style",
            "type": "Attribute",
            "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    text_anchor: Optional[str] = field(
        default=None,
        metadata={
            "name": "text-anchor",
            "type": "Attribute",
            "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    vtext_anchor: Optional[str] = field(
        default=None,
        metadata={
            "name": "vtext-anchor",
            "type": "Attribute",
            "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    font_size: Optional[int] = field(
        default=None,
        metadata={
            "name": "font-size",
            "type": "Attribute",
            "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )


@dataclass
class LinearGradient:
    class Meta:
        name = "linearGradient"
        namespace = "http://www.sbml.org/sbml/level3/version1/render/version1"

    stop: list["LinearGradient.Stop"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
            "required": True,
        },
    )
    x1: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    x2: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    y1: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    y2: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )

    @dataclass
    class Stop:
        offset: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
                "required": True,
            },
        )
        stop_color: Optional[str] = field(
            default=None,
            metadata={
                "name": "stop-color",
                "type": "Attribute",
                "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
                "required": True,
            },
        )


@dataclass
class ListOfColorDefinitions:
    class Meta:
        name = "listOfColorDefinitions"
        namespace = "http://www.sbml.org/sbml/level3/version1/render/version1"

    color_definition: list[ColorDefinition] = field(
        default_factory=list,
        metadata={
            "name": "colorDefinition",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class ListOfGradientDefinitions:
    class Meta:
        name = "listOfGradientDefinitions"
        namespace = "http://www.sbml.org/sbml/level3/version1/render/version1"

    linear_gradient: list[LinearGradient] = field(
        default_factory=list,
        metadata={
            "name": "linearGradient",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Style:
    class Meta:
        name = "style"
        namespace = "http://www.sbml.org/sbml/level3/version1/render/version1"

    g: Optional[G] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    id_list: Optional[str] = field(
        default=None,
        metadata={
            "name": "idList",
            "type": "Attribute",
            "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    role_list: Optional[str] = field(
        default=None,
        metadata={
            "name": "roleList",
            "type": "Attribute",
            "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    type_list: Optional[str] = field(
        default=None,
        metadata={
            "name": "typeList",
            "type": "Attribute",
            "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )


@dataclass
class ListOfStyles:
    class Meta:
        name = "listOfStyles"
        namespace = "http://www.sbml.org/sbml/level3/version1/render/version1"

    style: list[Style] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class RenderInformation:
    class Meta:
        name = "renderInformation"
        namespace = "http://www.sbml.org/sbml/level3/version1/render/version1"

    list_of_color_definitions: Optional[ListOfColorDefinitions] = field(
        default=None,
        metadata={
            "name": "listOfColorDefinitions",
            "type": "Element",
            "required": True,
        },
    )
    list_of_gradient_definitions: Optional[ListOfGradientDefinitions] = field(
        default=None,
        metadata={
            "name": "listOfGradientDefinitions",
            "type": "Element",
            "required": True,
        },
    )
    list_of_styles: Optional[ListOfStyles] = field(
        default=None,
        metadata={
            "name": "listOfStyles",
            "type": "Element",
            "required": True,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    program_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "programName",
            "type": "Attribute",
            "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    program_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "programVersion",
            "type": "Attribute",
            "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    background_color: Optional[str] = field(
        default=None,
        metadata={
            "name": "backgroundColor",
            "type": "Attribute",
            "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
