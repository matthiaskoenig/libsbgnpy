# Examples

Runnable examples of `libsbgnpy`. They are not part of the package, they are
run from a checkout of the repository:

```bash
python examples/read.py
```

| example | what it shows |
| --- | --- |
| [`read.py`](read.py) | read an SBGN document and display its content |
| [`write.py`](write.py) | create SBGN documents from scratch |
| [`clone_marker.py`](clone_marker.py) | mark glyphs which occur more than once |
| [`labels.py`](labels.py) | special characters in labels |
| [`notes.py`](notes.py) | write and read notes |
| [`extension.py`](extension.py) | write and read extensions |
| [`render.py`](render.py) | write and read render information |
| [`validate.py`](validate.py) | validate against the SBGN schema |
| [`ethanol.py`](ethanol.py) | build a map step by step and render it as an image |

`ethanol.py` renders images with a web service and therefore needs an internet
connection, all other examples run offline.

The SBGN documents the examples read are in [`sbgn/`](sbgn).
