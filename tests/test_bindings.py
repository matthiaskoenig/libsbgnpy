"""Check that the generated bindings are up to date.

`libsbgnpy.sbgn` and `libsbgnpy.render` are generated from the XML schemas by
`scripts/generate_bindings.py`, see `src/libsbgnpy/schema/README.md`. The test
generates them again and compares them with the committed modules, so a hand
edit or an update of the schemas or of xsdata without a regeneration fails.
"""

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "generate_bindings.py"


def test_bindings_up_to_date() -> None:
    """The committed bindings equal freshly generated ones."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--check"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
