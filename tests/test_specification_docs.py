"""Check that the tables of `docs/specifications.md` are up to date.

The tables are generated from `libsbgnpy.specification` by
`scripts/specification_docs.py`; a change of the versions or of the classes of
a language without a regeneration of the page fails.
"""

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "specification_docs.py"


def test_specification_docs_up_to_date() -> None:
    """The tables of the page equal freshly generated ones."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--check"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
