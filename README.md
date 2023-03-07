# LXG83

# LXG PRO : Migration & Replication

## Build and installation

Install master repo

`pip install -U git+https://github.com/wslerry/LXG83.git`



Install development repo

`pip install -U git+https://github.com/wslerry/LXG83.git@dev`



To install from repo

`git clone https://github.com/wslerry/LXG83.git`

`cd LXG83`

then follow as below as your choice of installation.

To install as python module

`python setup.py install`

or

`pip install .`

or `pip install -e .` for development

## Usage

1. For migration or replication

   ```python
   from LXG83 import Migration, Replication
   
   Migration()
   ```


2. For detecting changes of two different version of database

   ```python
   as
   ```

   

## Dev

**Versioning**

[ref 1](https://jacobtomlinson.dev/posts/2020/versioning-and-formatting-your-python-code/)

```bash
git add -A
git commit -m "Add versioneer"
git tag 0.0.1
```

