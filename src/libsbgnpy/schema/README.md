# Generate python bindings


The python language bindings were created from the XML schema using
generateDS and than adapted to include GlyphClasses and ArcClasses.

The latest versions support py2 and py3 (>0.24a0)
```
sudo pip install generateDS
```

```
/usr/local/bin/generateDS.py -o "libsbgn.py" -s "libsbgnSubs.py" SBGN.xsd
```

Additional changes to the mapping after creation:

**Adding write function**
```{python}
class SBGNBase ->

    def write_file(self, outfile, namespace='sbgn'):
        """ Write SBGN to file

        Necessary to fix the issue of the sbgn namespace prefix.

        :param outfile:
        :type outfile:
        :return:
        """
        f = open(outfile, 'w')
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        self.export(f, level=0, namespace_='sbgn', name_='')
        f.close()

        # this is a bad hack to remove the namespaces, because
        # most of the SBGN tools do not support them.
        import fileinput
        f = fileinput.input(outfile, inplace=True)

        for line in f:
            # remove prefix from closing tags, and unnecessary namespace
            line = line.replace(' xmlns:sbgn="http://sbgn.org/libsbgn/0.2"', '')
            line = line.replace('sbgn:', '')
            line = line.replace('<sbgn>', '<sbgn xmlns="http://sbgn.org/libsbgn/0.2">')
            print(line, end='')

        f.close()
```

**Adding type checks**
```{python}
class map ->

    def get_language(self):
        """ Get the Language.
        :return: Language instance.
        """
        return Language(self.language)

    def set_language(self, language):
        """ Sets the language and checks that within allowed values.
        :param language:
        :return:
        """
        if language and not isinstance(language, Language):
            raise TypeError('language must be of type Language')
        if language:
            self.language = _cast(None, language.value)
        else:
            self.language = _cast(None, language)

    __init__
        self.language = self.set_language(language)
        self.set_language(language)

class glyph ->

    def get_class(self):
        """ Returns the GlyphClass."""
        return GlyphClass(self.class_)

    def set_class(self, class_):
        """ Sets the class and checks that in allowed GlyphClasses
        :param class_:
        :return:
        """
        if class_ and not isinstance(class_, GlyphClass):
            raise TypeError('class must be of type GlyphClass')
        if class_:
            self.class_ = _cast(None, class_.value)
        else:
            self.class_ = _cast(None, class_)

    def get_orientation(self):
        """ Get orientation.
        :return: Orientation instance.
        """
        return Orientation(self.orientation)

    def set_orientation(self, orientation):
        """ Sets orientation and checks that allowed Orientation.

        :param orientation:
        :return:
        """
        if not isinstance(orientation, Orientation):
            raise TypeError('orientation must be of type Orientation')
        self.orientation = _cast(None, orientation.value)

    __init__
        self.set_class(class_)
        self.set_orientation(orientation)

class arc ->

    def get_class(self):
        """ Get the ArcClass. """
        return ArcClass(self.class_)

    def set_class(self, class_):
        """ Set the ArcClass.
        :param class_:
        :return:
        """
        if class_ and not isinstance(class_, ArcClass):
            raise TypeError('class must be of type ArcClass')
        if class_:
            self.class_ = _cast(None, class_.value)
        else:
            self.class_ = _cast(None, class_)

    __init__
        self.set_class(class_)
```
**Fixing bugs in automatic creation**
```
class bbox ->
    # change order of arguments for backwards compatibility
    def __init__(self, x=None, y=None, w=None,  h=None, notes=None, extension=None):

class calloutType ->
    # ensure that id is written in SBGN
    def set_target(self, target):
        if isinstance(target, glyph):
            self.target = target.get_id()
        else:
            self.target = target

```

**Overwrite namespace prefix**
```
namespace_='sbgn:' -> namespace_='namespace_'
self.exportChildren(outfile, level + 1, namespace_=namespace_, name_='point', pretty_print=pretty_print)
```
