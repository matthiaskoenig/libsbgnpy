"""
Helper functions for rendering SBGN.

Currently uses the webservice provided at "http://sysbioapps.dyndns.org/Layout/GenerateImage".
For documentation see
http://sysbioapps.dyndns.org/Home/Services
"""

import tempfile
from pathlib import Path
import requests

from libsbgnpy import utils


RENDER_URL = "http://sysbioapps.spdns.org/Layout"


def render_sbgn(sbgn, image_file: Path, file_format: str = "png") -> None:
    """Render given sbgn object to image.

    Currently supports the following file_formats:
    - "png"
    The image file must end in .file_format, e.g. in '.png'

    Performs a request analogue to:
    curl -X POST -F file=@".\BorisEJB.xml" http://sysbioapps.spdns.org/Layout/GenerateImage -o out.png

    :param sbgn: sbgn object
    :param image_file: image to create
    :return: None
    """
    if file_format != "png":
        raise ValueError("Only png rendering supported.")

    if not str(image_file).endswith(f".{file_format}"):
        raise ValueError(
            "The filename must end in <.file_format>, e.g. for png it must end in <.png>."
        )

    # Create temporary file for request
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
        f_in: Path = Path(tmp_dir) / "render.sbgn"
        utils.write_to_file(sbgn, f_in)

        # Call webservice for rendering
        files = [
            ("file", open(f_in, "rb")),
        ]
        r = requests.post(f"{RENDER_URL}/GenerateImage", files=files)

        r.raise_for_status()

        with open(image_file, "wb") as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
            fd.close()

        print("SBGN rendered:", image_file)
