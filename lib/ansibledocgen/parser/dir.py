""" DirParser Module """
from ansibledocgen.parser.ansiblecfg import AnsibleCfg
from ansibledocgen.parser.playbook import PlaybookParser
from ansibledocgen.parser.role import RoleParser


class DirParser(object):
    """ Parses an Ansible Project Directory Structure """

    def __init__(self, project):
        """ Setup Parser Modules
            @project is a relative or absolute path to an Ansible Project
        """
        self.ansiblecfg = AnsibleCfg(project)
        self.roleparser = RoleParser(self.ansiblecfg.get_role_paths())
        self.playbookparser = PlaybookParser(
            self.ansiblecfg.get_playbook_paths())

        # Parse all playbooks
        self.playbookparser.parse_playbooks()

    def get_parserdata(self):
        """ This function returns a datastructure
        that can be passed to a formatter """
        return self.playbookparser.parserdata + self.roleparser.parserdata
