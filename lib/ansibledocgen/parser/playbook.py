import yaml

class PlaybookParser(object):
    def __init__(self, playbooks, rolename=None):
        self.playbooks = playbooks
        self.parserdata = []
        self.rolename = rolename

    def parse_playbooks(self):
        for playbook in self.playbooks:
            self.parse_playbook(playbook)

    def parse_playbook(self, playbook):
        with open(playbook) as f:
            playbookentry = {}
            playbookentry["task_names"] = []
            playbookentry["relative_path"] = playbook

            # TEST
            playbookentry["author"] = "Test Author"
            playbookentry["description"] = "Test Description"
            playbookentry["rolename"] = self.rolename

            data = f.read()
            for task in yaml.load(data):
                for key in task:
                    if key == "name":
                        playbookentry["task_names"].append(key)
            self.parserdata.append(playbookentry)
