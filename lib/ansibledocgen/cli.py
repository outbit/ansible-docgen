import optparse
from ansibledocgen.parser.dir import DirParser
from ansibledocgen.formatter.markup import FormatterMarkup

class Cli(object):
    def __init__(self):
        parser = optparse.OptionParser()
        parser.add_option("-p", "--project", dest="project",
            help="Path to Ansible project", metavar="PROJECT", default="./")
        parser.add_option("-d", "--dest", dest="dest",
            help="Path to write documentation", metavar="DEST", default="./")
        parser.add_option("-s", "--style", dest="style",
            help="Choose the format for the documentation", metavar="STYLE", default="markup")
        (self.options, self.args) = parser.parse_args()

    def run(self):
        self.dirparser = DirParser(self.options.project)
        self.formatter = FormatterMarkup(self.dirparser.get_parserdata())
