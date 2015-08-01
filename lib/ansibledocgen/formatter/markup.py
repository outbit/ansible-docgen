class FormatterMarkup(object):
    def __init__(self, parserdata):
        self.parserdata = parserdata
        """ Example:
        [ { "author": "test",
        "description": "test2",
        "task_names": ["str1", "str2"],
        "rolename" : None,
        "relative_path" : "./myplaybook.yml"}, ] """
        self.parse_data()

    def parse_data(self):
        for sourcefile in self.parserdata:
            self.write_doc(sourcefile)

    def write_doc(self, file):
        print(file)
