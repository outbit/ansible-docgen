ansible-docgen
=====================

Description
===========

ansible-docgen generates documentation from annotated Ansible Playbooks and Roles.

[![Build Status](https://app.travis-ci.com/outbit/ansible-docgen.svg?branch=develop "ansible-docs latest build")](http://travis-ci.org/outbit/ansible-docgen)
[![PIP Version](https://img.shields.io/pypi/v/ansible-docgen.svg "ansible-docs PyPI version")](https://pypi.python.org/pypi/ansible-docgen)
[![Coverage Status](https://coveralls.io/repos/outbit/ansible-docgen/badge.svg?branch=develop&service=github)](https://coveralls.io/github/outbit/ansible-docgen?branch=develop)
[![Gitter IM](https://badges.gitter.im/Join%20Chat.svg)](https://matrix.to/#/#ansible-docgen:gitter.im)


Installation
===========

```shell
pip install ansible-docgen
```

or

```shell
easy_install ansible-docgen
```

Usage
===========

### Annotate Your Playbooks and Roles
```yaml
---
# test_playbook.yml
# Author: John Doe
# Description: Install a Webserver
- name: Install Apache
  yum: name=httpd state=installed
```
```yaml
---
# roles/appserver/tasks/main.yml
# Author: John Doe
# Description: Appserver role
- name: Copy Installer
  copy: src=installer dest=/tmp/
  tags:
    - copy-installer
- name:  Run Installer
  shell: /tmp/installer.sh
  tags:
    - run-installer
```
### Generate Documentation from Annotation
##### Use -p to specify your project directory. Click the links to preview the Markup generated by ansible-docgen. Warning: This will overwrite existing README files.

`ansible-docgen -p your_ansible_project`

`Generated Markup File` [your_ansible_project/rolestest/README.md](test/integration/project1/rolestest/README.md)

`Generated Markup File` [your_ansible_project/roles/README.md](test/integration/project1/roles/README.md)

`Generated Markup File` [your_ansible_project/README.md](test/integration/project1/README.md)


##### If your current directory is your project directory just run ansible-docgen without any arguments. Warning: This will overwrite existing README files.

`cd your_ansible_project && ansible-docgen`

`Generated Markup File` [otherroles/README.md](test/integration/project1/otherroles/README.md)

`Generated Markup File` [roles/README.md](test/integration/project1/roles/README.md)

`Generated Markup File` [README.md](test/integration/project1/README.md)

##### Help output
```bash
usage: ansible-docgen [-h] [-p PROJECT] [-f FILENAME] [-s STYLE] [-n] [-v]

options:
  -h, --help            show this help message and exit
  -p PROJECT, --project PROJECT
                        Path to Ansible project. Default is the current directory.
  -f FILENAME, --filename FILENAME
                        filename used for the output documentation file. Default is README
  -s STYLE, --style STYLE
                        Choose the format for the documentation. Default is markdown. Example: --style=[markdown]
  -n, --no-tags         This option disables show tags in the documentation
  -v, --version         Print version
  ```

License
=======

ansible-docgen is released under the [MIT License](LICENSE.md).

Author
======

David Whiteside (<david@davidwhiteside.com>)

