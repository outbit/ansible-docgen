from ansibledocgen.cli import Cli
import unittest
import sys
import os


class TestCli(unittest.TestCase):

    def test_project(self):
        # Test Specified Path
        sys.argv = [sys.argv[0]]
        sys.argv.append("-p")
        sys.argv.append("testdir")
        cli = Cli()
        assert(cli.project == "testdir/")
        assert(cli.style == "markdown")

        # Test No Path Given
        sys.argv = [sys.argv[0]]
        cli = Cli()
        assert(cli.project == "./")
        assert(cli.style == "markdown")

    def test_style(self):
        sys.argv = [sys.argv[0]]
        sys.argv.append("-s")
        sys.argv.append("markdown")
        cli = Cli()
        assert(cli.style == "markdown")

