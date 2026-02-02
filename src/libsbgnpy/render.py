from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://www.sbml.org/sbml/level3/version1/render/version1"


@dataclass(kw_only=True)
class ColorDefinition:
    class Meta:
        name = "colorDefinition"
        namespace = "http://www.sbml.org/sbml/level3/version1/render/version1"

    id: str = field(
        metadata={
            "type": "Attribute",
            # "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
            "required": True,
        }
    )
    value: str = field(
        metadata={
            "type": "Attribute",
            # "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class G:
    class Meta:
        name = "g"
        namespace = "http://www.sbml.org/sbml/level3/version1/render/version1"

    stroke: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            # "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    stroke_width: None | float = field(
        default=None,
        metadata={
            "name": "stroke-width",
            "type": "Attribute",
            # "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    fill: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            # "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    fill_rule: None | str = field(
        default=None,
        metadata={
            "name": "fill-rule",
            "type": "Attribute",
            # "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    font_family: None | str = field(
        default=None,
        metadata={
            "name": "font-family",
            "type": "Attribute",
            # "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    font_weight: None | str = field(
        default=None,
        metadata={
            "name": "font-weight",
            "type": "Attribute",
            # "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    font_style: None | str = field(
        default=None,
        metadata={
            "name": "font-style",
            "type": "Attribute",
            # "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    text_anchor: None | str = field(
        default=None,
        metadata={
            "name": "text-anchor",
            "type": "Attribute",
            # "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    vtext_anchor: None | str = field(
        default=None,
        metadata={
            "name": "vtext-anchor",
            "type": "Attribute",
            # "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    font_size: None | int = field(
        default=None,
        metadata={
            "name": "font-size",
            "type": "Attribute",
            # "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )


@dataclass(kw_only=True)
class LinearGradient:
    class Meta:
        name = "linearGradient"
        namespace = "http://www.sbml.org/sbml/level3/version1/render/version1"

    stop: list[LinearGradient.Stop] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    id: str = field(
        metadata={
            "type": "Attribute",
            # "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
            "required": True,
        }
    )
    x1: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            # "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    x2: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            # "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    y1: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            # "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    y2: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            # "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )

    @dataclass(kw_only=True)
    class Stop:
        offset: str = field(
            metadata={
                "type": "Attribute",
                # "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
                "required": True,
            }
        )
        stop_color: str = field(
            metadata={
                "name": "stop-color",
                "type": "Attribute",
                # "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
                "required": True,
            }
        )


@dataclass(kw_only=True)
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


@dataclass(kw_only=True)
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


@dataclass(kw_only=True)
class Style:
    class Meta:
        name = "style"
        namespace = "http://www.sbml.org/sbml/level3/version1/render/version1"

    g: G = field(
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    id_list: None | str = field(
        default=None,
        metadata={
            "name": "idList",
            "type": "Attribute",
            # "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    role_list: None | str = field(
        default=None,
        metadata={
            "name": "roleList",
            "type": "Attribute",
            # "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    type_list: None | str = field(
        default=None,
        metadata={
            "name": "typeList",
            "type": "Attribute",
            # "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )


@dataclass(kw_only=True)
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


@dataclass(kw_only=True)
class RenderInformation:
    class Meta:
        name = "renderInformation"
        namespace = "http://www.sbml.org/sbml/level3/version1/render/version1"

    list_of_color_definitions: ListOfColorDefinitions = field(
        metadata={
            "name": "listOfColorDefinitions",
            "type": "Element",
            "required": True,
        }
    )
    list_of_gradient_definitions: ListOfGradientDefinitions = field(
        metadata={
            "name": "listOfGradientDefinitions",
            "type": "Element",
            "required": True,
        }
    )
    list_of_styles: ListOfStyles = field(
        metadata={
            "name": "listOfStyles",
            "type": "Element",
            "required": True,
        }
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            # "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    name: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            # "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    program_name: None | str = field(
        default=None,
        metadata={
            "name": "programName",
            "type": "Attribute",
            # "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    program_version: None | str = field(
        default=None,
        metadata={
            "name": "programVersion",
            "type": "Attribute",
            # "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
    background_color: None | str = field(
        default=None,
        metadata={
            "name": "backgroundColor",
            "type": "Attribute",
            # "namespace": "http://www.sbml.org/sbml/level3/version1/render/version1",
        },
    )
