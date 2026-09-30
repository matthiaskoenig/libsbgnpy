"""Test the rendering of SBGN documents as images.

The rendering uses a web service. The tests of the behavior run against a
local HTTP server; `test_render_sbgn` queries the real service, it is marked as
`network` and deselected by default, run it with `pytest -m network`.
"""

import threading
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import pytest
import requests

from libsbgnpy import Sbgn, read_sbgn_from_file, render_sbgn
from libsbgnpy import image as image_module
from libsbgnpy.image import JPEG_SIGNATURE, PNG_SIGNATURE, RenderError

#: the SBGN documents the examples read
EXAMPLES_SBGN_DIR = Path(__file__).parent.parent / "examples" / "sbgn"

PNG = PNG_SIGNATURE + b"png content"


class Service:
    """A local stand-in for the rendering web service."""

    def __init__(self) -> None:
        """Answer with a PNG until told otherwise."""
        self.status = 200
        self.content_type = "image/png"
        self.body = PNG
        self.requests: list[bytes] = []


@pytest.fixture
def service(monkeypatch: pytest.MonkeyPatch) -> Iterator[Service]:
    """Serve the rendering requests locally."""
    state = Service()

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self) -> None:
            state.requests.append(self.rfile.read(int(self.headers["Content-Length"])))
            self.send_response(state.status)
            self.send_header("Content-Type", state.content_type)
            self.send_header("Content-Length", str(len(state.body)))
            self.end_headers()
            self.wfile.write(state.body)

        def log_message(self, format: str, *args: object) -> None:
            pass

    server = HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(
        target=server.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True
    )
    thread.start()
    monkeypatch.setattr(
        image_module, "RENDER_URL", f"http://127.0.0.1:{server.server_port}/layout"
    )
    yield state
    server.shutdown()
    server.server_close()


@pytest.fixture
def sbgn() -> Sbgn:
    """ADH example document."""
    return read_sbgn_from_file(EXAMPLES_SBGN_DIR / "adh.sbgn")


@pytest.mark.network
def test_render_sbgn(tmp_path: Path, sbgn: Sbgn) -> None:
    """An SBGN document is rendered to a PNG by the web service."""
    f_png = tmp_path / "test.png"
    render_sbgn(sbgn, f_png)

    assert f_png.read_bytes().startswith((PNG_SIGNATURE, JPEG_SIGNATURE))


def test_render_sbgn_local(tmp_path: Path, sbgn: Sbgn, service: Service) -> None:
    """The document is posted and the returned PNG is written."""
    f_png = tmp_path / "test.png"
    render_sbgn(sbgn, f_png)

    assert f_png.read_bytes() == PNG
    assert b"http://sbgn.org/libsbgn/0.3" in service.requests[0]


def test_render_sbgn_uppercase_suffix(
    tmp_path: Path, sbgn: Sbgn, service: Service
) -> None:
    """The suffix of the image file is checked case insensitively."""
    f_png = tmp_path / "test.PNG"
    render_sbgn(sbgn, f_png)

    assert f_png.read_bytes() == PNG


@pytest.mark.parametrize(
    ("content_type", "body", "match"),
    [
        ("text/html", b"<html>maintenance</html>", "instead of an image"),
        ("image/png", b"<html>no png</html>", "returned no image"),
    ],
)
def test_render_sbgn_no_image(
    tmp_path: Path,
    sbgn: Sbgn,
    service: Service,
    content_type: str,
    body: bytes,
    match: str,
) -> None:
    """An answer which is no PNG raises and leaves an existing file as it is."""
    service.content_type = content_type
    service.body = body
    f_png = tmp_path / "test.png"
    f_png.write_bytes(b"previous")

    with pytest.raises(RenderError, match=match):
        render_sbgn(sbgn, f_png)
    assert f_png.read_bytes() == b"previous"
    assert [f.name for f in tmp_path.iterdir()] == ["test.png"]


def test_render_sbgn_too_large(
    tmp_path: Path, sbgn: Sbgn, service: Service, monkeypatch: pytest.MonkeyPatch
) -> None:
    """An image larger than `RENDER_MAX_BYTES` is rejected."""
    monkeypatch.setattr(image_module, "RENDER_MAX_BYTES", len(PNG) - 1)

    with pytest.raises(RenderError, match="larger than"):
        render_sbgn(sbgn, tmp_path / "test.png")
    assert not (tmp_path / "test.png").exists()


def test_render_sbgn_server_error(tmp_path: Path, sbgn: Sbgn, service: Service) -> None:
    """An error of the web service raises an HTTP error."""
    service.status = 500
    service.content_type = "text/html"
    service.body = b"<html>error</html>"

    with pytest.raises(requests.HTTPError):
        render_sbgn(sbgn, tmp_path / "test.png")
    assert not (tmp_path / "test.png").exists()


def test_render_sbgn_unsupported_format(tmp_path: Path, sbgn: Sbgn) -> None:
    """An unsupported image format is reported."""
    with pytest.raises(ValueError, match="Unsupported image format"):
        render_sbgn(sbgn, tmp_path / "test.svg", file_format="svg")


def test_render_sbgn_wrong_suffix(tmp_path: Path, sbgn: Sbgn) -> None:
    """An image file with another suffix is reported."""
    with pytest.raises(ValueError, match="must end in"):
        render_sbgn(sbgn, tmp_path / "test.jpg")


def test_render_sbgn_jpeg(
    tmp_path: Path,
    sbgn: Sbgn,
    service: Service,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """A JPEG declared as PNG, as the web service returns it, is written."""
    service.body = JPEG_SIGNATURE + b"jpeg content"
    f_png = tmp_path / "test.png"
    render_sbgn(sbgn, f_png)

    assert f_png.read_bytes() == service.body
    assert "JPEG instead of a PNG" in caplog.text
