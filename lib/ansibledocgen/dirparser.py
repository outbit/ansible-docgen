from ansibledocgen.ansiblecfg import AnsibleCfg
from ansibledocgen.playbookparser import PlaybookParser
from ansibledocgen.roleparser import RoleParser

class DirParser(object):
	def __init__(self, project):
		self.ansiblecfg = AnsibleCfg(project)
		self.roleparser = RoleParser(self.ansiblecfg.get_role_paths())
		self.playbookparser = PlaybookParser(self.ansiblecfg.get_playbook_paths())

		# Parse all playbooks
		self.playbookparser.parse_playbooks()

	def debug(self):
		self.playbookparser.debug()