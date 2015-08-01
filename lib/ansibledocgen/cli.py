""" Command Line Interface Module """
import optparse
import sys
from ansibledocgen.parser.dir import DirParser
from ansibledocgen.formatter.markup import FormatterMarkup


class Cli(object):
    """ Command Line Interface for ansible-docgen """

    def __init__(self):
        """ Setup Arguments and Options for CLI """
        # Parse CLI Arguments
        parser = optparse.OptionParser()
        parser.add_option("-p", "--project", dest="project",
                          help="Path to Ansible project",
                          metavar="PROJECT",
                          default="./")
        parser.add_option("-s", "--style", dest="style",
                          help="Choose the format for the documentation.\
                          Default is markup. Example: --style=[markup]",
                          metavar="STYLE",
                          default="markup")
        (self.options, self.args) = parser.parse_args()

        # Used to Parse Roles and Playbooks
        self.dirparser = None
        self.formatter = None

    def run(self):
        """ Entry Point Of Application """
        # Parse Project for Roles and Playbooks
        self.dirparser = DirParser(self.options.project)

        # Based on chosen style, use the associated formatter
        if self.options.style == "markup":
            self.formatter = FormatterMarkup(
                self.dirparser.get_parserdata(), self.options.project)
        else:
            print("Error: Use of an unsupported style.\
                The supported styles are: markup")
            sys.exit(1)

        sys.exit(0)
