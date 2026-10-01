# SBGN specifications

SBGN is defined by two kinds of specifications: the **language specifications** define what a glyph and an arc mean and how they may be combined, one for each of the three languages, and the **SBGN-ML specification** defines how a map is stored as XML. `libsbgnpy` implements SBGN-ML 0.3 and knows the versions and the vocabularies of the language specifications, see `libsbgnpy.specification`. The specifications are published on [sbgn.github.io/specifications](https://sbgn.github.io/specifications) and registered with [COMBINE](https://github.com/combine-org/combine-specifications).

## The languages

| language | specification | publication |
| --- | --- | --- |
| Process Description (PD) | Level 1 Version 2.1 (2026) | Balci, Rougny et al. *Systems biology graphical notation: process description language level 1 version 2.1.* J Integr Bioinform (2026). [10.1515/jib-2025-0018](https://doi.org/10.1515/jib-2025-0018) |
| Entity Relationship (ER) | Level 1 Version 2.0 (2015) | Sorokin et al. *Systems Biology Graphical Notation: Entity Relationship language Level 1 Version 2.0.* J Integr Bioinform 12(2):264 (2015). [10.2390/biecoll-jib-2015-264](https://doi.org/10.2390/biecoll-jib-2015-264) |
| Activity Flow (AF) | Level 1 Version 1.2 (2015) | Mi et al. *Systems Biology Graphical Notation: Activity Flow language Level 1 Version 1.2.* J Integr Bioinform 12(2):265 (2015). [10.2390/biecoll-jib-2015-265](https://doi.org/10.2390/biecoll-jib-2015-265) |
| SBGN-ML | Version 0.3 (2020) | Bergmann et al. *Systems biology graphical notation markup language (SBGNML) version 0.3.* J Integr Bioinform 17(2-3):20200016 (2020). [10.1515/jib-2020-0016](https://doi.org/10.1515/jib-2020-0016) |

## The version of a map

A map states which specification it follows with its `version`, the identifier of the specification. SBGN-ML 0.3 deprecated the `language` of a map in favour of the `version`, and requires one of the two. The version names the language as well, so `map_language` takes the language from the version, and from the deprecated `language` if a map has no version:

```python
from libsbgnpy import LATEST, Map, MapLanguage, map_language

map = Map(
    id="ethanol",
    version=LATEST[MapLanguage.PROCESS_DESCRIPTION],
    language=MapLanguage.PROCESS_DESCRIPTION,
)
print(map.version.value)
# http://identifiers.org/combine.specifications/sbgn.pd.level-1.version-2.1
print(map_language(map))
# MapLanguage.PROCESS_DESCRIPTION
```

`LATEST` holds the version of the latest specification of every language, set in bold below. Set the `language` as well if a map is read by tools which only know SBGN-ML 0.2. `SPECIFICATIONS` maps every `MapVersion` to its `Specification`, i.e., its language, level, version, year and DOI. The `version` of a map is `http://identifiers.org/combine.specifications/` followed by the identifier of the specification:

<!-- specification:versions -->
| specification | year | publication | identifier |
| --- | --- | --- | --- |
| **PD L1V2.1** | 2026 | [10.1515/jib-2025-0018](https://doi.org/10.1515/jib-2025-0018) | `sbgn.pd.level-1.version-2.1` |
| PD L1V2.0 | 2019 | [10.1515/jib-2019-0022](https://doi.org/10.1515/jib-2019-0022) | `sbgn.pd.level-1.version-2.0` |
| PD L1V1.3 | 2015 | [10.2390/biecoll-jib-2015-263](https://doi.org/10.2390/biecoll-jib-2015-263) | `sbgn.pd.level-1.version-1.3` |
| PD L1V1.2 | 2010 |  | `sbgn.pd.level-1.version-1.2` |
| PD L1V1.1 | 2009 |  | `sbgn.pd.level-1.version-1.1` |
| PD L1V1.0 | 2008 |  | `sbgn.pd.level-1.version-1.0` |
| PD L1V1 |  |  | `sbgn.pd.level-1.version-1` |
| **ER L1V2.0** | 2015 | [10.2390/biecoll-jib-2015-264](https://doi.org/10.2390/biecoll-jib-2015-264) | `sbgn.er.level-1.version-2` |
| ER L1V1.2 | 2011 |  | `sbgn.er.level-1.version-1.2` |
| ER L1V1.1 | 2010 |  | `sbgn.er.level-1.version-1.1` |
| ER L1V1.0 | 2009 |  | `sbgn.er.level-1.version-1.0` |
| ER L1V1 |  |  | `sbgn.er.level-1.version-1` |
| **AF L1V1.2** | 2015 | [10.2390/biecoll-jib-2015-265](https://doi.org/10.2390/biecoll-jib-2015-265) | `sbgn.af.level-1.version-1.2` |
| AF L1V1.0 | 2009 |  | `sbgn.af.level-1.version-1.0` |
| AF L1V1 |  |  | `sbgn.af.level-1.version-1` |
<!-- /specification:versions -->

The version `version-1` of a language is the identifier of the latest version 1.x at the time it was registered. The published SBGN-ML schema, which `libsbgnpy` takes from [sbgn/libsbgn](https://github.com/sbgn/libsbgn), lacks PD L1V2.0 and L1V2.1; `libsbgnpy` adds both to its schema. PD L1V2.0 is listed by the SBGN-ML 0.3 specification, the identifier of PD L1V2.1 follows the naming of the registry but is not registered yet.

## What SBGN-ML 0.3 changed

SBGN-ML 0.3 is the format `libsbgnpy` reads and writes, documents in SBGN-ML 0.1 and 0.2 are upconverted while reading, see [Reading and writing](io.md#older-sbgn-ml-versions). Compared with 0.2:

- a document holds several maps, every map has an `id`,
- the `version` of a map replaces the deprecated `language`,
- submaps are supported completely with the `mapRef` and the `tagRef` of a glyph,
- the `perturbation` of AF is no longer an activity node, but a unit of information of a biological activity; the glyph class is deprecated in AF,
- colours and styles are stored as render information in the extension of a map, see [Render information](render.md).

## Glyphs of the latest PD specification in SBGN-ML

PD L1V2.0 and L1V2.1 renamed and added glyphs without changing SBGN-ML. They are encoded with the glyph classes which already exist:

| glyph of PD L1V2.x | SBGN-ML |
| --- | --- |
| empty set (replaces source and sink) | `source and sink` |
| submap terminal | `terminal` inside a `submap` |
| subunit of a complex | a glyph of an entity pool node class inside a `complex` |
| equivalence operator | `equivalence` |
| annotation | `annotation` |
| stoichiometry of a flux arc | `cardinality` inside the `arc` |

The shapes, e.g., the stadium of a simple chemical or of a state variable since PD L1V2.0, are a matter of the drawing and not stored in SBGN-ML.

## Glyphs and arcs of every language

The SBGN-ML schema has a single enumeration of glyph classes and of arc classes for all languages, it does not know which class belongs to which language. `GLYPH_CLASSES` and `ARC_CLASSES` hold the classes of the latest specification of every language, auxiliary units such as state variables included. Deprecated classes are still allowed, but logged as a warning.

<!-- specification:glyphs -->
| class | PD | ER | AF |
| --- | :---: | :---: | :---: |
| `unspecified entity` | ✓ |  |  |
| `simple chemical` | ✓ |  |  |
| `macromolecule` | ✓ |  |  |
| `nucleic acid feature` | ✓ |  |  |
| `simple chemical multimer` | ✓ |  |  |
| `macromolecule multimer` | ✓ |  |  |
| `nucleic acid feature multimer` | ✓ |  |  |
| `complex` | ✓ |  |  |
| `complex multimer` | ✓ |  |  |
| `source and sink` | ✓ |  |  |
| `perturbation` |  |  | deprecated |
| `biological activity` |  |  | ✓ |
| `perturbing agent` | ✓ | ✓ |  |
| `compartment` | ✓ |  | ✓ |
| `submap` | ✓ |  | ✓ |
| `tag` | ✓ |  | ✓ |
| `terminal` | ✓ |  | ✓ |
| `process` | ✓ |  |  |
| `omitted process` | ✓ |  |  |
| `uncertain process` | ✓ |  |  |
| `association` | ✓ |  |  |
| `dissociation` | ✓ |  |  |
| `phenotype` | ✓ | ✓ | ✓ |
| `and` | ✓ | ✓ | ✓ |
| `or` | ✓ | ✓ | ✓ |
| `not` | ✓ | ✓ | ✓ |
| `equivalence` | ✓ |  |  |
| `state variable` | ✓ | ✓ |  |
| `unit of information` | ✓ | ✓ | ✓ |
| `entity` |  | ✓ |  |
| `outcome` |  | ✓ |  |
| `interaction` |  | ✓ |  |
| `influence target` |  | ✓ |  |
| `annotation` | ✓ | ✓ | ✓ |
| `variable value` |  | ✓ |  |
| `implicit xor` |  | ✓ |  |
| `delay` |  | ✓ | ✓ |
| `existence` |  | ✓ |  |
| `location` |  | ✓ |  |
| `cardinality` | ✓ | ✓ |  |
| `observable` | deprecated | deprecated | deprecated |
<!-- /specification:glyphs -->

<!-- specification:arcs -->
| class | PD | ER | AF |
| --- | :---: | :---: | :---: |
| `production` | ✓ |  |  |
| `consumption` | ✓ |  |  |
| `catalysis` | ✓ |  |  |
| `modulation` | ✓ | ✓ |  |
| `stimulation` | ✓ | ✓ |  |
| `inhibition` | ✓ | ✓ |  |
| `assignment` |  | ✓ |  |
| `interaction` |  | ✓ |  |
| `absolute inhibition` |  | ✓ |  |
| `absolute stimulation` |  | ✓ |  |
| `positive influence` |  |  | ✓ |
| `negative influence` |  |  | ✓ |
| `unknown influence` |  |  | ✓ |
| `equivalence arc` | ✓ |  | ✓ |
| `necessary stimulation` | ✓ | ✓ | ✓ |
| `logic arc` | ✓ | ✓ | ✓ |
<!-- /specification:arcs -->

## Checking a map

`check_map` and `check_sbgn` check what the specifications require on top of the schema: a map declares its language with a `version` or a `language`, the two agree, and every glyph and every arc has a class of the language of the map. `validate` combines these checks with the validation against the schema, see [Validation](validation.md):

```python
from libsbgnpy import Bbox, Glyph, GlyphClass, Map, MapLanguage, check_map

map = Map(id="m", language=MapLanguage.PROCESS_DESCRIPTION)
map.glyph.append(
    Glyph(
        id="g1",
        class_value=GlyphClass.BIOLOGICAL_ACTIVITY,
        bbox=Bbox(x=0, y=0, w=120, h=60),
    )
)
print(check_map(map))
# ["map 'm': glyph 'g1' has the class 'biological activity', which is no glyph class of process description"]
```

The validation rules of the language specifications, e.g., that a consumption arc connects an entity pool node with a process, are checked by `validate_schematron`, see [Schematron rules](validation.md#schematron-rules).
