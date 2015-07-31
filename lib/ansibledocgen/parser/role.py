from ansibledocgen.parser.playbook import PlaybookParser
import os
import fnmatch

class RoleParser(object):
    def __init__(self, role_paths):
        self.role_paths = role_paths 
        self.playbooks = []
        self.find_main_tasks()
        self.parse_main_tasks()

    def find_main_tasks(self):
        self.main_tasks = []
        for role_path in self.role_paths:
            for root, dirnames, filenames in os.walk(role_path):
                # WHAT OTHER DIRECTORIES SHOULD I LOOK IN??? handlers/main.yml??
                for filename in fnmatch.filter(filenames, 'tasks/main.yml'):
                    # Absolute path to file
                    fullpath = os.path.join(root, filename)
                    self.main_tasks.append(fullpath)

    def parse_main_tasks(self):
        self.playbookparser = PlaybookParser(self.main_tasks)

        # Parse all main tasks
        self.playbookparser.parse_playbooks()

