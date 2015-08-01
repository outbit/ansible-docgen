from ansibledocgen.parser.playbook import PlaybookParser
import os
import fnmatch
import re

class RoleParser(object):
    def __init__(self, role_paths):
        self.role_paths = role_paths 
        self.playbooks = []
        self.main_tasks = []
        self.parserdata = []

        self.find_main_tasks()
        self.parse_main_tasks()

    def find_main_tasks(self):
        for role_path in self.role_paths:
            for root, dirnames, filenames in os.walk(role_path):
                # WHAT OTHER DIRECTORIES SHOULD I LOOK IN??? handlers/main.yml??
                for filename in fnmatch.filter(filenames, '*.yml'):
                    # Absolute path to file
                    fullpath = os.path.join(root, filename)
                    m = re.match("^.*?/tasks/main.yml$", fullpath)
                    if m:
                        self.main_tasks.append(fullpath)

    def parse_main_tasks(self):
        # Need to determine the rolename per task somehow
        self.playbookparser = PlaybookParser(self.main_tasks, rolename="TEST ROLENAME")

        # Parse all main tasks
        self.playbookparser.parse_playbooks()
        self.parserdata = self.playbookparser.parserdata

