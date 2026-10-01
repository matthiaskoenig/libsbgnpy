"""Validation of SBGN documents against the schematron rules of libsbgn.

The SBGN specifications define rules which the SBGN-ML schema cannot express,
e.g., that a consumption arc starts at an entity pool node and ends at a
process. [libsbgn](https://github.com/sbgn/libsbgn) implements them as
schematron rules, one file per map language. `validate_schematron` checks a
document against them and reports every broken rule as an `Issue`, the results
are the ones of the Java library.

```python
from pathlib import Path

from libsbgnpy import validate_schematron

for issue in validate_schematron(Path("map.sbgn")):
    print(issue.rule_id, issue.element_id)
    print(f"  {issue.message}")
```

The rules are packaged in `libsbgnpy/schema/`, see the `README.md` there for
their origin and the changes which let lxml run them with XSLT 1.0.
"""

import copy
import logging
from dataclasses import dataclass
from functools import cache
from pathlib import Path

from lxml import etree, isoschematron

from libsbgnpy.io import SBGN_NAMESPACE, parse_xml, upconvert_tree
from libsbgnpy.sbgn import MapLanguage
from libsbgnpy.specification import language_of

logger = logging.getLogger(__name__)

#: folder of the packaged schemas and rules
_SCHEMA_DIR = Path(__file__).parent / "schema"

#: schematron rules of every map language
RULES: dict[MapLanguage, Path] = {
    MapLanguage.PROCESS_DESCRIPTION: _SCHEMA_DIR / "sbgn_pd.sch",
    MapLanguage.ENTITY_RELATIONSHIP: _SCHEMA_DIR / "sbgn_er.sch",
    MapLanguage.ACTIVITY_FLOW: _SCHEMA_DIR / "sbgn_af.sch",
}

#: namespace of the report of a schematron validation
SVRL_NAMESPACE = "http://purl.oclc.org/dsdl/svrl"


@dataclass(frozen=True, kw_only=True)
class Issue:
    """A rule of the SBGN specifications which a map breaks.

    Attributes:
        severity: the role of the rule, `error` for all rules which are checked.
        rule_id: id of the rule, e.g., `pd10101`, the language followed by the
            number of the rule.
        message: what the rule requires.
        element_id: id of the glyph or arc which breaks the rule, None if the
            rule does not name it.
    """

    severity: str
    rule_id: str
    message: str
    element_id: str | None


def validate_schematron(f: Path) -> list[Issue]:
    """Validate an SBGN file against the schematron rules of libsbgn.

    The file is read like [`validate_xsd`][libsbgnpy.validator.validate_xsd]
    reads it: decoded with the encoding of its XML declaration and upconverted
    from SBGN-ML 0.1 and 0.2. Every map is checked on its own with the rules of
    its language, which is taken from its `version` or else its `language`, see
    [`language_of`][libsbgnpy.specification.language_of]; a map of an unknown
    language is not checked. As in the Java library, the `basic` phase of the
    rules is checked.

    The rules do not check the structure of the document, a document without
    maps, e.g., another XML document, has no issues; validate it with
    [`validate_xsd`][libsbgnpy.validator.validate_xsd] first.

    Args:
        f: path of the SBGN file

    Returns:
        The broken rules, in the order of the maps and of the rules; empty if
        the document breaks none.

    Raises:
        OSError: if the file cannot be read
        lxml.etree.XMLSyntaxError: if the file is no well-formed XML
    """
    root = upconvert_tree(parse_xml(Path(f).read_bytes()))
    issues: list[Issue] = []
    for sbgn_map in root.iterchildren(f"{{{SBGN_NAMESPACE}}}map"):
        language = language_of(sbgn_map.get("version"), sbgn_map.get("language"))
        if language is None:
            logger.info(
                "Map '%s' has no known language, its rules are not checked: '%s'",
                sbgn_map.get("id"),
                f,
            )
            continue
        report = _validator(language)(_single_map(root, sbgn_map))
        issues.extend(_issues(report.getroot()))

    if issues:
        logger.info("SBGN file breaks schematron rules: '%s' (%s)", f, len(issues))
    return issues


@cache
def _validator(language: MapLanguage) -> etree.XSLT:
    """Compile the rules of a map language.

    The compiled transformation writes the report of a validation; unlike an
    `isoschematron.Schematron`, which stores the report of its last validation,
    it holds no state.

    Args:
        language: the map language

    Returns:
        The transformation of a document into its validation report.
    """
    schematron = isoschematron.Schematron(
        etree.parse(RULES[language]),
        phase="basic",
        # the upstream rules deviate from the ISO Schematron grammar, see
        # `libsbgnpy/schema/README.md`
        validate_schema=False,
        store_xslt=True,
    )
    validator_xslt = schematron.validator_xslt
    # kept with `store_xslt`
    assert validator_xslt is not None
    return etree.XSLT(validator_xslt)


def _single_map(root: etree._Element, sbgn_map: etree._Element) -> etree._Element:
    """Copy a document with a single of its maps.

    The rules look up glyphs and arcs in the whole document, e.g., the source
    of an arc, so a map is checked in a document without the other maps.

    Args:
        root: root of the document
        sbgn_map: the map which is kept, a child of the root

    Returns:
        The root of the copy.
    """
    single = copy.deepcopy(root)
    for original, copied in zip(root, single, strict=True):
        if original.tag == sbgn_map.tag and original is not sbgn_map:
            single.remove(copied)
    return single


def _issues(report: etree._Element) -> list[Issue]:
    """Read the issues from the report of a schematron validation.

    Args:
        report: root of the report, in the SVRL namespace

    Returns:
        An issue for every failed assertion and successful report.
    """
    issues = []
    for result in report.iter(
        f"{{{SVRL_NAMESPACE}}}failed-assert", f"{{{SVRL_NAMESPACE}}}successful-report"
    ):
        # the diagnostic `id` of the rules is the id of the element, it is
        # empty if the element has none
        element_id = (
            result.findtext(
                f"{{{SVRL_NAMESPACE}}}diagnostic-reference[@diagnostic='id']"
            )
            or ""
        ).strip()
        issues.append(
            Issue(
                severity=result.get("role") or "error",
                rule_id=result.get("id") or "",
                message=" ".join(
                    (result.findtext(f"{{{SVRL_NAMESPACE}}}text") or "").split()
                ),
                element_id=element_id or None,
            )
        )
    return issues
