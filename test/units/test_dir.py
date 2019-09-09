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

        # Check for expected attributes in sourcedata
        assert("playbooks" in parserdata)
        for folder_content, sourcedata in parserdata["playbooks"].iteritems():
            assert("name" in sourcedata[0])
            assert("relative_path" in sourcedata[0])
        assert("roles" in parserdata)
        for folder_content, sourcedata in parserdata["roles"].iteritems():
            assert("name" in sourcedata[0])
            assert("relative_path" in sourcedata[0])
        assert("host_vars" in parserdata)
        for hostname, contents in parserdata["host_vars"].iteritems():
            assert("host_1" in hostname)
            assert("position" in contents)
            assert("relative_path" in contents["position"])
