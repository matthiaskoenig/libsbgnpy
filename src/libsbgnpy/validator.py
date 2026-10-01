"""Validation of SBGN documents.

`validate_xsd` validates against the SBGN XSD schema, the packaged SBGN-ML 0.3
schema in `libsbgnpy/schema/SBGN.xsd`. Documents in the earlier namespaces are
upconverted before they are validated, i.e., the same documents are read and
validated. `validate` adds the rules of the SBGN specifications which the
schema cannot express, see `libsbgnpy.specification`. The schematron rules of
the SBGN languages are checked separately, see `libsbgnpy.schematron`.

```python
from pathlib import Path

from libsbgnpy import validate

errors = validate(Path("map.sbgn"))
if errors:
    for error in errors:
        print(error)
```
"""

import logging
from pathlib import Path

from lxml import etree
from xsdata.exceptions import ParserError

from libsbgnpy.io import _read_sbgn, parse_xml, upconvert_tree
from libsbgnpy.specification import check_sbgn

logger = logging.getLogger(__name__)

#: SBGN-ML schema the documents are validated against
XSD_SCHEMA = Path(__file__).parent / "schema" / "SBGN.xsd"


def validate_xsd(f: Path) -> list[str]:
    """Validate an SBGN file against the SBGN XSD schema.

    The file is decoded with the encoding its XML declaration names, UTF-8 by
    default; a file which is no well-formed XML is reported as a single error.

    Args:
        f: path of the SBGN file

    Returns:
        The validation errors, empty if the document is valid.

    Raises:
        OSError: if the file cannot be read
    """
    try:
        doc = upconvert_tree(parse_xml(Path(f).read_bytes()))
    except etree.XMLSyntaxError as err:
        logger.info("SBGN file is no well-formed XML: '%s'", f)
        return [str(err)]

    schema = etree.XMLSchema(etree.parse(XSD_SCHEMA))
    if schema.validate(doc):
        return []

    errors = [str(error) for error in schema.error_log]
    logger.info("SBGN file is invalid: '%s' (%s errors)", f, len(errors))
    return errors


def validate(f: Path) -> list[str]:
    """Validate an SBGN file against the schema and the SBGN specifications.

    The errors of [`validate_xsd`][libsbgnpy.validator.validate_xsd] are
    followed by the errors of
    [`check_sbgn`][libsbgnpy.specification.check_sbgn], i.e., of the rules of
    the specifications which the schema cannot express. A document which cannot
    be read is only checked against the schema.

    Args:
        f: path of the SBGN file

    Returns:
        The validation errors, empty if the document is valid.

    Raises:
        OSError: if the file cannot be read
    """
    errors = validate_xsd(f)
    try:
        sbgn = _read_sbgn(Path(f).read_bytes())
    except ParserError:
        return errors
    return errors + check_sbgn(sbgn)
