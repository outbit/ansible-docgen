from ansibledocgen.ansiblecfg import AnsibleCfg

class DirParser(object):
	def __init__(self, project):
	    self.ansiblecfg = AnsibleCfg(project)

	def get_roles(self):
	    # TEST
	    return [ "fullpath/role1", "fullpath/role2"]
