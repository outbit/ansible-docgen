import nose
from ansibledocgen.parser.role import RoleParser
import unittest
import sys
import os

class TestRole(unittest.TestCase):
    def test_all(self):
        localdir = os.path.dirname(os.path.realpath(__file__))
        projectunit = os.path.join(localdir, "../integration/projectunit")
        # TODO
