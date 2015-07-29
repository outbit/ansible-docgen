class AnsibleCfg(object):
	def __init__(self, project):
		# Search for configs in all locations, including path
		# Load Ansible Configs into a dictionary
	    self.project = project

	def get_role_paths(self):
		# TESTING FOR NOW
		return ["test/integration/roles/basic/"]

	def get_playbook_paths(self):
		# TESTING FOR NOW
		return ["test/integration/basic_playbook.yml"]