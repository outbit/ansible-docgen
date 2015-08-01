import re

class FormatterMarkup(object):
    def __init__(self, parserdata, project):
        self.parserdata = parserdata
        self.project = project
        """ Example parserdata:
        [ { "author": "test",
        "description": "test2",
        "task_names": ["str1", "str2"],
        "rolename" : None,
        "relative_path" : "./myplaybook.yml"}, ] """
        self.role_outfiles = {}
        self.playbook_outfiles = {}

        self.parse_data()

        self.write_files()

    def parse_data(self):
        for sourcefile in self.parserdata:
            self.write_doc(sourcefile)

    def write_doc(self, sourcefile):
        # sourcefile expected: { "author": "", "description": "", "task_names": "", .....}
        # Parse a Role
        if sourcefile["rolename"] is not None:
            m = re.match("^(.*?)%s/tasks" % sourcefile["rolename"], sourcefile["relative_path"])
            if m :
                roledir = m.group(1)
                if roledir not in self.role_outfiles:
                    self.role_outfiles[roledir] = []
                self.role_outfiles[roledir].append("Role: %s" % sourcefile["rolename"])
                self.role_outfiles[roledir].append("========================")
                self.role_outfiles[roledir].append("author: %s\n" % sourcefile["author"])
                self.role_outfiles[roledir].append("description: %s\n" % sourcefile["description"])
                for task_name in sourcefile["task_names"]:
                    self.role_outfiles[roledir].append("Task: %s\n" % task_name)
                self.role_outfiles[roledir].append("")
        # Parse a Playbook
        else:
            playbookpath = self.project
            if playbookpath not in self.playbook_outfiles:
                self.playbook_outfiles[playbookpath] = []
            self.playbook_outfiles[playbookpath].append("Playbook: %s" % sourcefile["relative_path"].strip(playbookpath))
            self.playbook_outfiles[playbookpath].append("========================")
            self.playbook_outfiles[playbookpath].append("author: %s\n" % sourcefile["author"])
            self.playbook_outfiles[playbookpath].append("description: %s\n" % sourcefile["description"])
            for task_name in sourcefile["task_names"]:
                self.playbook_outfiles[playbookpath].append("Task: %s\n" % task_name)
            self.playbook_outfiles[playbookpath].append("")

        # DEBUG DEBUG DEBUG
        # print(sourcefile)

    def write_files(self):
        # Write Role Markup Files
        for rolepath in self.role_outfiles:
            filename = "%s%s" % (rolepath, "README.md")
            with open(filename, "w") as p:
                for line in self.role_outfiles[rolepath]:
                    p.write("%s\n" % line)

        # Write Playbook Markup Files
        for playbookpath in self.playbook_outfiles:
            filename = "%s%s" % (playbookpath, "README.md")
            with open(filename, "w") as p:
                for line in self.playbook_outfiles[playbookpath]:
                    p.write("%s\n" % line)
