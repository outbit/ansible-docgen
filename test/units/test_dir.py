import nose
from ansibledocgen.parser.dir import DirParser
import unittest
import sys
import os


class TestDir(unittest.TestCase):

    def test_parserdata(self):
        localdir = os.path.dirname(os.path.realpath(__file__))
        projectunit = os.path.join(localdir, "../integration/projectunit")
        dirparser = DirParser(projectunit)
        parserdata = dirparser.get_parserdata()

        # Check for expected attribures in sourcedata
        for sourcedata in parserdata:
            assert("rolename" in sourcedata)
            assert("relative_path" in sourcedata)
