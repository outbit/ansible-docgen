"""Command Line Interface Module"""

import argparse
import sys
import os
from ansibledocgen.parser.dir import DirParser
from ansibledocgen.formatter.formatter import Formatter
from ansibledocgen import __version__


def main() -> None:
    cli = Cli()
    cli.run()
    sys.exit(0)


class Cli:
    """Command Line Interface for ansible-docgen"""

    def __init__(self) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-p",
            "--project",
            dest="project",
            help="Path to Ansible project",
            metavar="PROJECT",
            default="./",
        )
        parser.add_argument(
            "-f",
            "--filename",
            dest="filename",
            help="filename used for the output documentation file. Default is README",
            metavar="FILENAME",
            default="README",
        )
        parser.add_argument(
            "-s",
            "--style",
            dest="style",
            help="Choose the format for the documentation. Default is markdown. Example: --style=[markdown]",
            metavar="STYLE",
            default="markdown",
        )
        parser.add_argument(
            "-n",
            "--no-tags",
            dest="show_tags",
            help="This option disables show tags in the documentation",
            default=True,
            action="store_false",
        )
        parser.add_argument(
            "-v",
            "--version",
            dest="show_version",
            help="Print version",
            default=False,
            action="store_true",
        )

        args = parser.parse_args()
        self.project = os.path.join(args.project, "")
        self.filename, _ = os.path.splitext(args.filename)
        self.style = args.style
        self.params = {
            "show_tags": args.show_tags,
            "show_version": args.show_version,
        }
        self.dirparser: DirParser | None = None
        self.formatter: Formatter | None = None

    def run(self) -> None:
        if self.params["show_version"]:
            print(f"ansible-docgen version: {__version__}")
            sys.exit(0)

        self.dirparser = DirParser(self.project)
        parserdata = self.dirparser.get_parserdata()
        paths = self.dirparser.get_paths()

        if self.style == "markdown":
            self.formatter = Formatter(
                "markdown", parserdata, paths, self.project, self.params
            )
            self.formatter.parse_data()
            self.formatter.write_files(self.filename)
        else:
            print(
                "Error: Use of an unsupported style. The supported styles are: markdown"
            )
            sys.exit(1)
