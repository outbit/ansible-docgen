# ansible-docgen

Generate documentation from annotated Ansible playbooks and roles.

[![Tests](https://github.com/outbit/ansible-docgen/actions/workflows/tests.yml/badge.svg?branch=develop)](https://github.com/outbit/ansible-docgen/actions/workflows/tests.yml)
[![PyPI version](https://img.shields.io/pypi/v/ansible-docgen.svg)](https://pypi.python.org/pypi/ansible-docgen)

## Requirements

- Python 3.10+

## Installation

```shell
pip install ansible-docgen
```

## Usage

### 1. Annotate your playbooks and roles

Add `# Author:` and `# Description:` comments at the top of your playbook or role task file:

```yaml
---
# Author: John Doe
# Description: Install and configure a web server

- hosts: webservers
  tasks:
    - name: Install Apache
      yum:
        name: httpd
        state: installed
```

```yaml
---
# roles/appserver/tasks/main.yml
# Author: John Doe
# Description: Appserver role

- name: Copy installer
  copy:
    src: installer
    dest: /tmp/
  tags:
    - copy-installer

- name: Run installer
  shell: /tmp/installer.sh
  tags:
    - run-installer
```

### 2. Generate documentation

Run from your project directory:

```shell
ansible-docgen
```

Or specify the project path explicitly:

```shell
ansible-docgen -p /path/to/your/ansible/project
```

This writes `README.md` files into your project, roles, and custom roles directories.

> **Warning:** This will overwrite any existing README files in those directories.

### CLI reference

```
usage: ansible-docgen [-h] [-p PROJECT] [-f FILENAME] [-s STYLE] [-i IGNORE] [-n] [-v]

options:
  -h, --help            show this help message and exit
  -p PROJECT, --project PROJECT
                        Path to Ansible project. Default is the current directory.
  -f FILENAME, --filename FILENAME
                        Output documentation filename (without extension). Default: README
  -s STYLE, --style STYLE
                        Output format. Default: markdown
  -i IGNORE, --ignore IGNORE
                        Comma-separated list of attributes to omit from output.
                        Example: -i author,task
  -n, --no-tags         Hide task tags in the output
  -v, --version         Print version and exit
```

## Development

```shell
git clone https://github.com/outbit/ansible-docgen
cd ansible-docgen
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Run the tests:

```shell
pytest
```

Lint:

```shell
ruff check lib test
```

## License

Released under the [MIT License](LICENSE.md).
