"""Write and read extensions.

An extension stores arbitrary XML on any SBGN element, e.g., render
information or annotations, see
<https://github.com/sbgn/sbgn/wiki/SBGN-ML_Extensions>.

```bash
python examples/extension.py
```
"""

from pathlib import Path

from libsbgnpy import (
    Map,
    MapLanguage,
    Sbgn,
    Sbgnbase,
    element_to_string,
    read_sbgn_from_file,
    write_sbgn_to_file,
)
from libsbgnpy.console import console

ANNOTATION = """<annotation xmlns="http://www.sbml.org/2001/ns/libsbml/annotation">
  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
           xmlns:bqbiol="http://biomodels.net/biology-qualifiers/">
    <rdf:Description rdf:about="#glyph1">
      <bqbiol:is>
        <rdf:Bag>
          <rdf:li rdf:resource="https://identifiers.org/uniprot:P05023"/>
        </rdf:Bag>
      </bqbiol:is>
    </rdf:Description>
  </rdf:RDF>
</annotation>"""


def write_extension(f: Path) -> Sbgn:
    """Write a map with an annotation in the extension.

    Args:
        f: path of the SBGN file to write

    Returns:
        The SBGN document.
    """
    map = Map(id="extension", language=MapLanguage.PROCESS_DESCRIPTION)
    sbgn = Sbgn(map=[map])
    map.extension = Sbgnbase.Extension(any_element=[ANNOTATION])

    write_sbgn_to_file(sbgn, f)
    return sbgn


def read_extension(f: Path) -> None:
    """Read the extension of a map.

    The extension is read back as XML elements, `element_to_string` serializes
    them again.

    Args:
        f: path of the SBGN file
    """
    sbgn = read_sbgn_from_file(f)
    extension = sbgn.map[0].extension
    if extension is None:
        return

    for element in extension.any_element:
        console.print(element_to_string(element))


if __name__ == "__main__":
    f_sbgn = Path("extension.sbgn")
    write_extension(f_sbgn)
    read_extension(f_sbgn)
