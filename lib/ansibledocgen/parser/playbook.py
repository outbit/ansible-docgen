""" Playbook Module """
import yaml
import re
import os
import codecs


class PlaybookParser(object):
    """ Parse An Individual Playbook """

    def __init__(self, playbooks, is_role=False):
        """ @playbooks is a list of paths to playbooks
            @is_role is used to determine if the playbook is part of a role
        """
        self.playbooks = playbooks
        self.parserdata = []
        self.is_role = is_role
        # basename of playbooks already parsed, to prevent infinate recrusion
        self.already_parsed_playbooks = []

    def parse_playbooks(self):
        """ Parse Each Playbook """
        for playbook in self.playbooks:
            self.parse_playbook(playbook)

    def parse_playbook(self, playbook):
        """ Parse an Individual Playbook """
        with codecs.open(playbook, "r", encoding="utf-8") as f:
            # Get Rolename from filepath
            rolename = None
            if self.is_role:
                m = re.match(r".*/(.*?)/tasks/main.yml", playbook)
                if m:
                    rolename = m.group(1)

            # Do Not Parse If Its Already been Parsed
            playbook_base = os.path.basename(playbook)
            if self.is_role:
                # If Role, prepend rolename to make file unique to role
                playbook_base = "%s/%s" % (rolename, playbook_base)
            # Check if this file has alread been parsed
            if playbook_base in self.already_parsed_playbooks:
                return
            self.already_parsed_playbooks.append(playbook_base)

            # Setup Playbook Metadata
            playbookentry = {}
            playbookentry["relative_path"] = playbook
            playbookentry["rolename"] = rolename

            # Read file content into data
            data = f.read()

            # Parse Comment Data
            for line in data.splitlines():
                m = re.match(r"^[ ]*#[ ]*(.*?)[ ]*:[ ]*(.*?)$", line)
                if m:
                    attribute = m.group(1)
                    value = m.group(2)

                    # Set An Attribute
                    if attribute.lower() == "author" or attribute.lower() == "description":
                        playbookentry[attribute.lower()] = value

            # Parse Task Names from playbook
            yamldata = yaml.load(data)
            # Skip Empty YAML Files
            if yamldata is None:
                return

            # Parase the Yaml
            for task in yamldata:
                # Playbooks have a tasks dict key
                if "tasks" in task:
                    task = task["tasks"]
                # Loop through Role tasks
                if isinstance(task, dict) and self.is_role:
                    for key in task:
                        if key.lower() == "name":
                            # Initialize List for tasks
                            if "task_names" not in playbookentry:
                                playbookentry["task_names"] = []
                            # Append a Task
                            playbookentry["task_names"].append(task[key])
                # Loop through Playbook tasks
                elif isinstance(task, list) and not self.is_role:
                    tasks = task
                    for task in tasks:
                        for key in task:
                            if key.lower() == "name":
                                # Initialize List for tasks
                                if "task_names" not in playbookentry:
                                    playbookentry["task_names"] = []
                                # Append a Task
                                playbookentry["task_names"].append(task[key])
            self.parserdata.append(playbookentry)
