"""Run the examples.

The examples are runnable scripts in `examples/`, not part of the package, see
`examples/README.md`. Every example is executed in a temporary working
directory, so the files it writes do not end up in the repository.
"""

import subprocess
import sys
from pathlib import Path

import pytest

#: the runnable examples, see `examples/README.md`
EXAMPLES_DIR = Path(__file__).parent.parent / "examples"

#: examples which query the rendering web service, see `tests/test_image.py`
NETWORK_EXAMPLES = {"ethanol.py"}

EXAMPLES = sorted(
    f for f in EXAMPLES_DIR.glob("*.py") if f.name not in NETWORK_EXAMPLES
)


@pytest.mark.parametrize("f", EXAMPLES, ids=lambda f: f.name)
def test_example(f: Path, tmp_path: Path) -> None:
    """Every example runs without an error."""
    result = subprocess.run(
        [sys.executable, str(f)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
