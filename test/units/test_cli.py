import nose
from ansibledocgen.cli import Cli
import unittest
import sys
import os


class TestCli(unittest.TestCase):

    def test_project(self):
        # Test Specified Path
        sys.argv[1] = "-p"
        sys.argv[2] = "testdir"
        cli = Cli()
        assert(cli.project == "testdir/")
        assert(cli.style == "markup")

        # Test No Path Given
        sys.argv[1] = ""
        sys.argv[2] = ""
        cli = Cli()
        assert(cli.project == "./")
        assert(cli.style == "markup")

    def test_style(self):
        sys.argv[1] = "-s"
        sys.argv[2] = "markup"
        cli = Cli()
        assert(cli.style == "markup")

    def test_run(self):
        localdir = os.path.dirname(os.path.realpath(__file__))
        projectunit = os.path.join(localdir, "../integration/projectunit")
        sys.argv[1] = "-p"
        sys.argv[2] = projectunit
        cli = Cli()
        cli.run()

        assert(os.path.isfile(os.path.join(projectunit, "README.md")))

        assert(os.path.isfile(os.path.join(projectunit, "roles/README.md")))

        assert(
            os.path.isfile(
                os.path.join(
                    projectunit,
                    "rolestest/README.md")))
