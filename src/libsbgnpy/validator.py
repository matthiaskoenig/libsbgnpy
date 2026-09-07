"""Validation of SBGN documents against the SBGN XSD schema.

The packaged schema is the SBGN-ML 0.3 schema in `libsbgnpy/schema/SBGN.xsd`,
documents in the earlier namespaces are upconverted before they are validated,
i.e., the same documents are read and validated.

```python
from pathlib import Path

from libsbgnpy import validate_xsd

errors = validate_xsd(Path("map.sbgn"))
if errors:
    for error in errors:
        print(error)
```
"""

import logging
from pathlib import Path

from lxml import etree

from libsbgnpy.io import upconvert

logger = logging.getLogger(__name__)

#: SBGN-ML schema the documents are validated against
XSD_SCHEMA = Path(__file__).parent / "schema" / "SBGN.xsd"


def validate_xsd(f: Path) -> list[str]:
    """Validate an SBGN file against the SBGN XSD schema.

    Args:
        f: path of the SBGN file

    Returns:
        The validation errors, empty if the document is valid.

    Raises:
        OSError: if the file cannot be read
    """
    schema = etree.XMLSchema(etree.parse(XSD_SCHEMA))

    with open(f, encoding="utf-8") as f_in:
        xml_str = upconvert(f_in.read())

    try:
        doc = etree.fromstring(xml_str.encode("utf-8"))
    except etree.XMLSyntaxError as err:
        logger.info("SBGN file is no well-formed XML: '%s'", f)
        return [str(err)]

    if schema.validate(doc):
        return []

    errors = [str(error) for error in schema.error_log]
    logger.info("SBGN file is invalid: '%s' (%s errors)", f, len(errors))
    return errors
