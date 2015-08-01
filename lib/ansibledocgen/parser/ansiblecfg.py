import os
import re
import fnmatch

class AnsibleCfg(object):
    def __init__(self, project):
        # Search for configs in all locations, including path
        # Load Ansible Configs into a dictionary
        # ANSIBLE_CONFIG (an environment variable)
        # ansible.cfg (in the current directory)
        # .ansible.cfg (in the home directory)
        # /etc/ansible/ansible.cfg
        self.project = project
        self.config = None
        self.settings = {}
        #self.find_config()

    def find_config(self):
        homedir = os.path.expanduser("~")

        # Detect Environment defined ansible config
        ansible_envpath = None
        if "ANSIBLE_CFG" in os.environ:
            ansible_envpath = os.environ["ANSIBLE_CFG"]

        config_files = ( ansible_envpath, "%s%s"%(self.project, "ansible.cfg"), "%s%s"%(os.path.expanduser("~"), ".ansible.cfg"), "/etc/ansible/ansible.cfg", )

        # Loop through configs and stop when one is found
        for config in config_files:
            if config is not None:
                if os.path.isfile(config):
                    self.load_config(config)
                    break

    def load_config(self, filename):
        with open (filename, "r") as f:
            self.config = f.read()

        for line in self.config:
            m = re.match(r'^[ ]*(.*?)[ ]*=[ ]*(.*?)$', line)
            if m:
                self.settings[m.group(1)] = m.group(2)

    def get_role_paths(self):
        if "roles_path" not in self.settings:
            return ["%s%s" % (self.project, "roles/")]
        else:
            return ["%s%s" % (self.project, self.settings["roles_path"])]

    def get_playbook_paths(self):
        """ Crawl Directory structure excluding role roles_path
        and find all .yml files """
        playbooks = []

        # Find all .yml files in the project directory
        for root, dirnames, filenames in os.walk(self.project):
            for filename in fnmatch.filter(filenames, '*.yml'):
                # Absolute path to file
                fullpath = os.path.join(root, filename)

                # Detect if this file is in a role
                is_rolepath = False
                for rolepath in self.get_role_paths():
                    if re.match(r'^%s' % rolepath, fullpath):
                        is_rolepath = True

                # Do not search in roles
                if not is_rolepath:
                    playbooks.append(fullpath)

        return playbooks