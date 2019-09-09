""" Command Line Interface Module """
import optparse
import sys
import os
from ansibledocgen.parser.dir import DirParser
from ansibledocgen.formatter.formatter import Formatter


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
        parser.add_option("-n", "--no-tags", dest="show_tags",
                          action='store_false',
                          help="This option disables show tags in the documentation",
                          metavar="TAGS",
                          default=True)
        (options, args) = parser.parse_args()

        # Make sure there is a trailing /
        self.project = os.path.join(options.project, "")
        self.style = options.style
        self.params = {}
        self.params['show_tags'] = options.show_tags

        # Used to Parse Roles and Playbooks
        self.dirparser = None
        self.formatter = None

    def run(self):
        """ EntryPoint Of Application """
        # Parse Project for Roles and Playbooks
        self.dirparser = DirParser(self.project)

        # Based on chosen style, use the associated formatter
        parserdata = self.dirparser.get_parserdata()
        
        paths = self.dirparser.get_paths()
        if self.style == "markup":
            self.formatter = Formatter('markup', parserdata, paths,\
                                        self.project, self.params)
            self.formatter.parse_data()
            self.formatter.write_files()
        else:
            print("Error: Use of an unsupported style.\
                The supported styles are: markup")
            sys.exit(1)
