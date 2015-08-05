import unittest
import sys
import os
from ansibledocgen.parser.playbook import PlaybookParser

class TestPlaybook(unittest.TestCase):
    def test_parser_playbook(self):
        localdir = os.path.dirname(os.path.realpath(__file__))
        testfile = os.path.join(localdir, ".output/testplaybook.yml")
        with open(testfile, "w") as f:
             f.write("---\n")
             f.write("# Author: Me\n")
             f.write("# description: this is a test\n")
             f.write("- hosts: testhosts\n")
             f.write("  tasks:\n")
             f.write("     - name: 'Install Apache'\n")
             f.write("       yum: name=httpd state=installed\n")

        playbook = PlaybookParser([testfile], is_role=False)

        playbook.parse_playbooks()

        # One Element in Array
        assert( len(playbook.parserdata) == 1 )

        assert( "author" in playbook.parserdata[0] )

        assert( "description" in playbook.parserdata[0] )

        assert( "task_names" in playbook.parserdata[0] )

        assert( playbook.parserdata[0]["rolename"] is None)
