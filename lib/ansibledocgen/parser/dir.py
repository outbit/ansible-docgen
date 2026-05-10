"""DirParser Module"""

from ansibledocgen.parser.ansiblecfg import AnsibleCfg
from ansibledocgen.parser.playbook import PlaybookParser
from ansibledocgen.parser.role import RoleParser
from ansibledocgen.parser.hostvars import HostVarsParser


class DirParser:
    """Parses an Ansible Project Directory Structure"""

    def __init__(self, project: str) -> None:
        self.ansiblecfg = AnsibleCfg(project)
        print("Parsing roles")
        self.role_parser = RoleParser(self.ansiblecfg.get_role_paths())
        print("Parsing playbooks")
        self.playbook_parser = PlaybookParser(self.ansiblecfg.get_playbook_paths())
        print("Parsing hosts")
        self.host_vars_parser = HostVarsParser(self.ansiblecfg.get_hosts_paths())

        self.host_vars_parser.parse_hosts_vars()
        self.playbook_parser.parse_playbooks()

    def get_paths(self) -> dict:
        return {
            "role": self.ansiblecfg.get_role_paths(),
            "playbooks": [self.ansiblecfg.get_playbook_paths()],
            "host": self.ansiblecfg.get_hosts_paths(),
        }

    def get_parserdata(self) -> dict:
        return {
            "playbooks": self.playbook_parser.parserdata,
            "roles": self.role_parser.parserdata,
            "host_vars": self.host_vars_parser.parserdata,
        }
