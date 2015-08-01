from ansibledocgen.parser.ansiblecfg import AnsibleCfg
from ansibledocgen.parser.playbook import PlaybookParser
from ansibledocgen.parser.role import RoleParser


class DirParser(object):

    def __init__(self, project):
        self.ansiblecfg = AnsibleCfg(project)
        self.roleparser = RoleParser(self.ansiblecfg.get_role_paths())
        self.playbookparser = PlaybookParser(
            self.ansiblecfg.get_playbook_paths())

        # Parse all playbooks
        self.playbookparser.parse_playbooks()

    def get_parserdata(self):
        return self.playbookparser.parserdata + self.roleparser.parserdata
