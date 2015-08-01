import re

class FormatterMarkup(object):
    def __init__(self, parserdata):
        self.parserdata = parserdata
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
                self.role_outfiles[roledir].append(sourcefile["rolename"])
                self.role_outfiles[roledir].append("========================")
                self.role_outfiles[roledir].append("author: %s" % sourcefile["author"])
                self.role_outfiles[roledir].append("description: %s" % sourcefile["description"])
                for task_name in sourcefile["task_names"]:
                    self.role_outfiles[roledir].append("Task: %s" % task_name)
                self.role_outfiles[roledir].append("")
        # Parse a Playbook
        else:
            pass

        # DEBUG DEBUG DEBUG
        # print(sourcefile)

    def write_files(self):
        for rolepath in self.role_outfiles:
            filename = "%s%s" % (rolepath, "README.md")
            with open(filename, "w") as p:
                for line in self.role_outfiles[rolepath]:
                    p.write("%s\n" % line)
