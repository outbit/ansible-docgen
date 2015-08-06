""" Command Line Interface Module """
import optparse
import sys
import os
from ansibledocgen.parser.dir import DirParser
from ansibledocgen.formatter.markup import MarkupFormatter


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
        (options, args) = parser.parse_args()

        # Make sure there is a trailing /
        self.project = os.path.join(options.project, "")
        self.style = options.style

        # Used to Parse Roles and Playbooks
        self.dirparser = None
        self.formatter = None

    def run(self):
        """ EntryPoint Of Application """
        # Parse Project for Roles and Playbooks
        self.dirparser = DirParser(self.project)

        # Based on chosen style, use the associated formatter
        if self.style == "markup":
            self.formatter = MarkupFormatter(
                self.dirparser.get_parserdata(), self.project)
            self.formatter.parse_data()
            self.formatter.write_files()
        else:
            print("Error: Use of an unsupported style.\
                The supported styles are: markup")
            sys.exit(1)
