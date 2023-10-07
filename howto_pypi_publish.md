```bash
# Setup your ~/.pypirc
[distutils]
index-servers =
  ansible-docgen
  ansible-docgen-test

[ansible-docgen]
repository = https://upload.pypi.org/legacy/
username = xyz
password = xyz

[ansible-docgen-test]
repository = https://test.pypi.org/legacy/
username = xyz
password = xyz

# Build
python setup.py bdist_wheel --universal

# Upload
rm -f dist/*
twine upload --repository-url https://upload.pypi.org/legacy/ dist/ansible_docgen-*
```
