import nose
from ansibledocgen.cli import Cli
import unittest
import sys

class TestCli(unittest.TestCase):
    def test_help(self):
        sys.argv[1:] = "-h"
        cli = Cli()
        assert(cli.options is None and cli.args is None)