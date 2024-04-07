Test locally
===

```bash
$ python -m pip install -e .
$ cd test/integrations/project1/ && ansible-docgen
```

Build new release
===

```bash
$ git checkout master
$ git merge develop --no-ff
$ git push
$ git tag vX.Y.Z
$ git push origin vX.Y.Z
```

- Publish a release on github.com

Follow instructions to build and publish to pypi
===

```bash
# Setup your ~/.pypirc
[distutils]
index-servers =
  pypi
  pypi-test

[pypi]
  username = __token__
  password = SECRET

[pypi-test]
  username = __token__
  password = SECRET

# Build
$ python3 -m pip install --upgrade pip
$ python3 -m pip install --upgrade build
$ python3 -m build
$ rm -f dist/*
$ python3 -m build

# Upload
$ python3 -m pip install --upgrade twine
$ python3 -m twine upload --repository pypi dist/* --verbose
```
