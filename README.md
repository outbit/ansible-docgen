ansible-docgen
=====================

Description
===========

ansible-docgen generates documentation from annotated Ansible Playbooks and Roles.

[![Build Status](https://secure.travis-ci.org/starboarder2001/ansible-docgen.png?branch=master "ansible-docs latest build")](http://travis-ci.org/starboarder2001/ansible-docgen)
[![PIP Version](https://img.shields.io/pypi/v/ansible-docgen.svg "ansible-docs PyPI version")](https://pypi.python.org/pypi/ansible-docgen)
[![Coverage Status](https://coveralls.io/repos/starboarder2001/ansible-docgen/badge.svg?branch=develop&service=github)](https://coveralls.io/github/starboarder2001/ansible-docgen?branch=develop)
[![Gitter IM](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/starboarder2001/ansible-docgen)


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

License
=======

ansible-docgen is released under the [MIT License](LICENSE.md).

Author
======

David Whiteside (<david@davidwhiteside.com>)
