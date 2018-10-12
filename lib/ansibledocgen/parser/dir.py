""" DirParser Module """
from ansibledocgen.parser.ansiblecfg import AnsibleCfg
from ansibledocgen.parser.playbook import PlaybookParser
from ansibledocgen.parser.role import RoleParser
from ansibledocgen.parser.hostvars import HostVarsParser
import os

class DirParser(object):
    """ Parses an Ansible Project Directory Structure """

    def __init__(self, project):
        """ Setup Parser Modules
            @param project: is a relative or absolute path to an Ansible Project
        """
        self.ansiblecfg = AnsibleCfg(project)
        self.roleparser = RoleParser(self.ansiblecfg.get_role_paths())
        self.playbookparser = PlaybookParser(
            self.ansiblecfg.get_playbook_paths())
        self.hostVarsParser = HostVarsParser(self.ansiblecfg.get_hosts_paths())

        # Parse all playbooks
        self.hostVarsParser.parse_hosts_vars()
        self.playbookparser.parse_playbooks()
        
    def get_paths(self):
        return {
            'role': self.ansiblecfg.get_role_paths(),
            'playbook': [os.path.dirname(self.ansiblecfg.get_playbook_paths()[0])],
            'host': self.ansiblecfg.get_hosts_paths()
            }
        
    def get_parserdata(self):
        """ This function returns a datastructure
        that can be passed to a formatter """
        return {
            'playbooks': self.playbookparser.parserdata, 
            'roles': self.roleparser.parserdata, 
            'host_vars': self.hostVarsParser.parserdata 
            }
