"""Validate SBGN documents against the SBGN XSD schema.

The documents in `examples/sbgn/` are valid, `invalid.sbgn` breaks the schema
on purpose, so a run shows both outcomes.

```bash
python examples/validate.py
```
"""

from pathlib import Path

from libsbgnpy import validate_xsd
from libsbgnpy.console import console

SBGN_DIR = Path(__file__).parent / "sbgn"


def validate(f: Path) -> list[str]:
    """Validate an SBGN file and report the errors.

    Args:
        f: path of the SBGN file

    Returns:
        The validation errors, empty if the document is valid.
    """
    errors = validate_xsd(f)
    if errors:
        console.print(f"[error]invalid[/error]: {f.name}")
        for error in errors:
            console.print(f"  {error}")
    else:
        console.print(f"[success]valid[/success]: {f.name}")
    return errors


if __name__ == "__main__":
    files = sorted(SBGN_DIR.glob("*.sbgn"))
    invalid = [f_sbgn for f_sbgn in files if validate(f_sbgn)]
    console.print(f"\n{len(files) - len(invalid)}/{len(files)} documents are valid")
    if invalid:
        console.print(f"invalid: {', '.join(f_sbgn.name for f_sbgn in invalid)}")
