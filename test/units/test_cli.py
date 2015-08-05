import nose
from ansibledocgen.cli import Cli
import unittest
import sys

class TestCli(unittest.TestCase):
    def test_help(self):
        sys.argv[1:] = "-h"
        clivar = Cli()
        assert("h" in clivar.args)

    def test_project(self):
        sys.argv[1] = "-p"
        sys.argv[2] = "testdir"
        clivar = Cli()
        assert(clivar.project is "testdir")

