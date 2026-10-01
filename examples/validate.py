"""Validate SBGN documents against the schema, the specifications and the rules.

The documents in `examples/sbgn/` are valid, `invalid.sbgn` breaks the schema
on purpose, so a run shows both outcomes. The schematron rules of the SBGN
languages are checked separately, a document can be valid and still break a
rule.

```bash
python examples/validate.py
```
"""

from pathlib import Path

from libsbgnpy import validate, validate_schematron
from libsbgnpy.console import console

SBGN_DIR = Path(__file__).parent / "sbgn"


def report(f: Path) -> list[str]:
    """Validate an SBGN file and report the errors and the broken rules.

    Args:
        f: path of the SBGN file

    Returns:
        The validation errors, empty if the document is valid.
    """
    errors = validate(f)
    if errors:
        console.print(f"[error]invalid[/error]: {f.name}")
        for error in errors:
            console.print(f"  {error}")
    else:
        console.print(f"[success]valid[/success]: {f.name}")

    for issue in validate_schematron(f):
        console.print(f"  {issue.rule_id} '{issue.element_id}'")
        console.print(f"    {issue.message}")
    return errors


if __name__ == "__main__":
    files = sorted(SBGN_DIR.glob("*.sbgn"))
    invalid = [f_sbgn for f_sbgn in files if report(f_sbgn)]
    console.print(f"\n{len(files) - len(invalid)}/{len(files)} documents are valid")
    if invalid:
        console.print(f"invalid: {', '.join(f_sbgn.name for f_sbgn in invalid)}")
