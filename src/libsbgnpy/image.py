"""Rendering of SBGN documents as images.

The rendering is performed by the web service of Frank Bergmann at
<https://sbml.bioquant.uni-heidelberg.de/layout>, i.e., it requires an internet
connection. For the documentation of the service see
<http://sysbioapps.spdns.org/Layout>.

```python
from pathlib import Path

from libsbgnpy import read_sbgn_from_file, render_sbgn

sbgn = read_sbgn_from_file(Path("map.sbgn"))
render_sbgn(sbgn, Path("map.png"))
```
"""

import logging
import tempfile
from pathlib import Path

import requests

from libsbgnpy.io import write_sbgn_to_file
from libsbgnpy.sbgn import Sbgn

logger = logging.getLogger(__name__)

#: web service rendering an SBGN document
RENDER_URL = "https://sbml.bioquant.uni-heidelberg.de/layout"

#: image formats supported by the web service
RENDER_FORMATS = ("png",)

#: seconds to wait for the web service
RENDER_TIMEOUT = 60


def render_sbgn(sbgn: Sbgn, image_file: Path, file_format: str = "png") -> None:
    """Render an SBGN document to an image.

    The document is sent to the rendering web service, which lays the map out
    and returns the image. The request is equivalent to

    ```bash
    curl -X POST -F file=@"map.sbgn" \
        https://sbml.bioquant.uni-heidelberg.de/layout -o map.png
    ```

    Args:
        sbgn: SBGN document
        image_file: path of the image to create, ending in `.<file_format>`
        file_format: image format, only `png` is supported

    Raises:
        ValueError: if the format is not supported or the file has another suffix
        requests.RequestException: if the web service cannot be reached or fails
    """
    if file_format not in RENDER_FORMATS:
        raise ValueError(
            f"Unsupported image format: '{file_format}', "
            f"supported formats are {RENDER_FORMATS}."
        )
    if image_file.suffix != f".{file_format}":
        raise ValueError(
            f"The image file must end in '.{file_format}', but is '{image_file}'."
        )

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
        f_sbgn = Path(tmp_dir) / "render.sbgn"
        write_sbgn_to_file(sbgn, f_sbgn)

        with open(f_sbgn, "rb") as f_in:
            response = requests.post(
                RENDER_URL, files={"file": f_in}, timeout=RENDER_TIMEOUT
            )
        response.raise_for_status()

    with open(image_file, "wb") as f_out:
        for chunk in response.iter_content(chunk_size=128):
            f_out.write(chunk)

    logger.info("SBGN rendered: %s", image_file)
