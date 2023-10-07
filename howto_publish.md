```bash
python setup.py bdist_wheel --universal
rm -f dist/*
twine upload --repository-url https://upload.pypi.org/legacy/ dist/ansible_docgen-*
```
