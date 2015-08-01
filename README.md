ansible-docgen
=====================

Description
===========

ansible-docgen generates documentation from annotated Ansible Playbooks and Roles

[![alt text](https://secure.travis-ci.org/starboarder2001/ansible-docgen.png?branch=master "ansible-docs latest build")](http://travis-ci.org/starboarder2001/ansible-docgen)
[![alt text](https://img.shields.io/pypi/v/ansible-docgen.svg "ansible-docs PyPI version")](https://pypi.python.org/pypi/ansible-docgen)
[![alt text](https://img.shields.io/pypi/dm/ansible-docgen.svg "ansible-docs PyPI downloads")](https://pypi.python.org/pypi/ansible-docgen)


Installation
===========

```shell
pip install ansible-docgen
```

or

```shell
easy_install ansible-docgen
```

Examples
===========

```shell
ansible-docgen -p your_ansible_project
Generated Markup File test/integration/otherroles/README.md
Generated Markup File test/integration/roles/README.md
Generated Markup File test/integration/README.md
```

```shell
cd your_ansible_project && ansible-docgen
Generated Markup File test/integration/otherroles/README.md
Generated Markup File test/integration/roles/README.md
Generated Markup File test/integration/README.md
```

License
=======

ansible-docgen is released under the MIT License.
