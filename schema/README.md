# Generate python bindings with xdata

The python language bindings were created from the XML schema using
[xsdata](https://github.com/tefra/xsdata).
The latest schema files are available from https://github.com/sbgn/libsbgn
in the folder resources.

## Install all dependencies
pip install xsdata[cli,lxml,soap]


## Generate models
```bash
cd schema
xsdata generate SBGN.xsd --package libsbgn
```

## Updates
## Copy files
- copy files to libsbgnpy folder
- copy the init content to the __init__
- rename classes: "sbgn" -> SBGN; "Sbgnbase" -> SBGNBase
