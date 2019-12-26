import nose
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
        assert(cli.style == "markup")

        # Test No Path Given
        sys.argv = [sys.argv[0]]
        cli = Cli()
        assert(cli.project == "./")
        assert(cli.style == "markup")

    def test_style(self):
        sys.argv = [sys.argv[0]]
        sys.argv.append("-s")
        sys.argv.append("markup")
        cli = Cli()
        assert(cli.style == "markup")

    def test_run(self):
        localdir = os.path.dirname(os.path.realpath(__file__))
        projectunit = os.path.join(localdir, "../integration/projectunit")
        sys.argv = [sys.argv[0]]
        sys.argv.append("-p")
        sys.argv.append(projectunit)
        cli = Cli()
        cli.run()

        assert(os.path.isfile(os.path.join(projectunit, "README.md")))
        assert(os.path.isfile(os.path.join(projectunit, "roles/README.md")))

        assert(
            os.path.isfile(
                os.path.join(
                    projectunit,
                    "rolestest/README.md")))
