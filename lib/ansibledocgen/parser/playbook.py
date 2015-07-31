import yaml

class PlaybookParser(object):
    def __init__(self, playbooks):
        self.playbooks = playbooks
        self.comments = {}
        self.tasks = []

    def parse_playbooks(self):
        for playbook in self.playbooks:
            self.parse_playbook(playbook)

    def parse_playbook(self, playbook):
        with open(playbook) as f:
            data = f.read()
            for task in yaml.load(data):
                for key in task:
                    if key == "name":
                        self.tasks.append(task[key])

    def debug(self):
        print(self.comments)
        print(self.tasks)