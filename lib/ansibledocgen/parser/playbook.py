import yaml
import re

class PlaybookParser(object):
    def __init__(self, playbooks, is_role=False):
        self.playbooks = playbooks
        self.parserdata = []
        self.is_role = is_role

    def parse_playbooks(self):
        for playbook in self.playbooks:
            self.parse_playbook(playbook)

    def parse_playbook(self, playbook):
        with open(playbook) as f:
            rolename = None
            if self.is_role:
                m = re.match(r".*roles/(.*?)/.*", playbook)
                if m:
                    rolename = m.group(1)

            playbookentry = {}
            playbookentry["task_names"] = []
            playbookentry["relative_path"] = playbook

            # TEST
            playbookentry["author"] = "Test Author"
            playbookentry["description"] = "Test Description"
            playbookentry["rolename"] = rolename

            data = f.read()
            for task in yaml.load(data):
                for key in task:
                    if key == "name":
                        playbookentry["task_names"].append(task[key])
            self.parserdata.append(playbookentry)
