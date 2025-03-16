# Documentation Builder

## Pandoc
```bash
sudo apt -Y install pandoc
```

## Python requirements (sphinx)
```bash
pip install -r requirements-docs.txt
```

## Build documentation
```bash
uv run make html
```

## Update jupyter notebooks
```bash
pip install jupyterlab
ipython kernel install --user --name libsbgnpy
```
