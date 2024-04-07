""" Asible Config Module """
import os
import re
import fnmatch
import codecs


class AnsibleCfg(object):
    """ Parse an Ansible Config File """

    def __init__(self, project):
        """
        Search for configs in all locations, including path
        Load Ansible Configs into a dictionary
        ANSIBLE_CONFIG (an environment variable)
        ansible.cfg (in the current directory)
        .ansible.cfg (in the home directory)
        /etc/ansible/ansible.cfg
        """
        self.project = project
        self.config = None
        self.settings = {}
        self.find_config()

    def find_config(self):
        """ Find The Ansible Config """
        homedir = os.path.expanduser("~")

        # Detect Environment defined ansible config
        ansible_envpath = None
        if "ANSIBLE_CFG" in os.environ:
            ansible_envpath = os.environ["ANSIBLE_CFG"]

        config_files = (ansible_envpath,
                        os.path.join(self.project, "ansible.cfg"),
                        os.path.join(homedir, ".ansible.cfg"),
                        "/etc/ansible/ansible.cfg", )

        # Loop through configs and stop when one is found
        for config in config_files:
            if config is not None:
                if os.path.isfile(config):
                    self.load_config(config)
                    break

    def load_config(self, filename):
        """ Load An Individual AnsibleConfig """
        with codecs.open(filename, "r", encoding="utf-8") as f:
            self.config = f.read()

        for line in self.config.splitlines():
            m = re.match(r'^[ ]*(.*?)[ ]*=[ ]*(.*?)$', line)
            if m:
                self.settings[m.group(1)] = m.group(2)

    def get_role_paths(self):
        """ Get Role Paths Base on Ansible Config """
        if "roles_path" not in self.settings:
            return [os.path.join(self.project, "roles/")]
        else:
            role_paths = self.settings["roles_path"].split(":")
            role_full_paths = []
            found_default_roles = False
            for role_path in role_paths:
                role_full_paths.append(
                    os.path.join(self.project, role_path.strip("./")))
            for role_path in role_full_paths:
                if "/roles/" in role_path:
                    found_default_roles = True
                    break
            if found_default_roles == False:
                role_full_paths.append(os.path.join(self.project, "roles/"))
            return role_full_paths

    def get_playbook_paths(self):
        """ Crawl Directory structure excluding role roles_path
        and find all .yml files """
        playbooks = []

        # Find all .yml files in the project directory
        for root, dirnames, filenames in os.walk(self.project):
            filenames.sort()
            dirnames.sort()
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
    
    def get_hosts_paths(self):
        """ Get host vars Paths Base on Ansible Config 
        @return: host_vars path base
        @rtype: list
        """
        return [os.path.join(self.project, "host_vars")]
