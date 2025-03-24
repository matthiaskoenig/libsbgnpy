# Generate python bindings with xdata

The python language bindings were created from the XML schema using
[xsdata](https://github.com/tefra/xsdata).
The latest schema files are available from https://github.com/sbgn/libsbgn
in the folder resources.

## Install all dependencies
pip install xsdata[cli,lxml,soap]


## Generate models
```bash
xsdata generate SBGN.xsd --package sbgn
```
