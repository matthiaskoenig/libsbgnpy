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
import os
import tempfile
from pathlib import Path

import requests

from libsbgnpy.io import write_sbgn_to_string
from libsbgnpy.sbgn import Sbgn

logger = logging.getLogger(__name__)

#: web service rendering an SBGN document
RENDER_URL = "https://sbml.bioquant.uni-heidelberg.de/layout"

#: image formats supported by the web service
RENDER_FORMATS = ("png",)

#: seconds to wait for the web service
RENDER_TIMEOUT = 60

#: largest image accepted from the web service, in bytes
RENDER_MAX_BYTES = 50 * 1024 * 1024

#: first bytes of every PNG file
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

#: first bytes of every JPEG file; the web service currently answers with a
#: JPEG although it declares `image/png`
JPEG_SIGNATURE = b"\xff\xd8\xff"


class RenderError(requests.RequestException):
    """The rendering web service answered, but not with an image."""


def render_sbgn(sbgn: Sbgn, image_file: Path, file_format: str = "png") -> None:
    """Render an SBGN document to an image.

    The document is sent to the rendering web service, which lays the map out
    and returns the image. The request is equivalent to

    ```bash
    curl -X POST -F file=@"map.sbgn" \
        https://sbml.bioquant.uni-heidelberg.de/layout -o map.png
    ```

    The image is only written if the service returns an image, and it is
    written atomically: an existing file is replaced as a whole or left as it
    is. The service currently returns a JPEG although it declares a PNG; the
    JPEG is written as it is and a warning is logged.

    Args:
        sbgn: SBGN document
        image_file: path of the image to create, ending in `.<file_format>`
            (in any case)
        file_format: image format, only `png` is supported

    Raises:
        ValueError: if the format is not supported or the file has another suffix
        RenderError: if the web service answers with something else than an
            image, or with an image larger than `RENDER_MAX_BYTES`
        requests.RequestException: if the web service cannot be reached or fails;
            `RenderError` is a subclass
    """
    image_file = Path(image_file)
    if file_format not in RENDER_FORMATS:
        raise ValueError(
            f"Unsupported image format: '{file_format}', "
            f"supported formats are {RENDER_FORMATS}."
        )
    if image_file.suffix.lower() != f".{file_format}":
        raise ValueError(
            f"The image file must end in '.{file_format}', but is '{image_file}'."
        )

    xml_bytes = write_sbgn_to_string(sbgn).encode("utf-8")
    with requests.post(
        RENDER_URL,
        files={"file": ("render.sbgn", xml_bytes, "application/xml")},
        timeout=RENDER_TIMEOUT,
        stream=True,
    ) as response:
        response.raise_for_status()
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith(f"image/{file_format}"):
            raise RenderError(
                f"The web service returned '{content_type}' instead of an image.",
                response=response,
            )
        image = _read_limited(response)

    if image.startswith(JPEG_SIGNATURE):
        logger.warning(
            "The web service returned a JPEG instead of a PNG, it is written to "
            "'%s' as it is.",
            image_file,
        )
    elif not image.startswith(PNG_SIGNATURE):
        raise RenderError("The web service returned no image.", response=response)
    _write_atomic(image_file, image)
    logger.info("SBGN rendered: %s", image_file)


def _read_limited(response: requests.Response) -> bytes:
    """Read the body of a streamed response up to `RENDER_MAX_BYTES`.

    Args:
        response: streamed response of the web service

    Returns:
        The body.

    Raises:
        RenderError: if the body is larger than `RENDER_MAX_BYTES`
    """
    chunks: list[bytes] = []
    size = 0
    for chunk in response.iter_content(chunk_size=64 * 1024):
        size += len(chunk)
        if size > RENDER_MAX_BYTES:
            raise RenderError(
                f"The image is larger than {RENDER_MAX_BYTES} bytes.",
                response=response,
            )
        chunks.append(chunk)
    return b"".join(chunks)


def _write_atomic(path: Path, content: bytes) -> None:
    """Write a file atomically, via a temporary file in the same directory.

    Args:
        path: file to write
        content: content of the file

    Raises:
        OSError: if the file cannot be written
    """
    fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    try:
        with os.fdopen(fd, "wb") as f_out:
            f_out.write(content)
        os.replace(tmp_name, path)
    except BaseException:
        Path(tmp_name).unlink(missing_ok=True)
        raise
