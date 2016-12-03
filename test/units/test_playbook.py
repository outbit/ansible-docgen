# coding=UTF-8
import unittest
import sys
import os
import codecs
from ansibledocgen.parser.playbook import PlaybookParser


class TestPlaybook(unittest.TestCase):

    def test_parser_playbook(self):
        localdir = os.path.dirname(os.path.realpath(__file__))
        testfile = os.path.join(localdir, ".output/testplaybook.yml")
        with codecs.open(testfile, "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write(u"# Author: Me شيشه ب\n")
            f.write(u"# description: this is a test شيشه ب\n")
            f.write(u"- hosts: testhoشيشهsts\n")
            f.write("  tasks:\n")
            f.write(u"     - name: 'Install Apache شيشه ب'\n")
            f.write(u"       yum: name=httpd state=inشtalled\n")

        playbook = PlaybookParser([testfile], is_role=False)

        playbook.parse_playbooks()

        # One Element in Array
        assert(len(playbook.parserdata) == 1)

        assert("author" in playbook.parserdata[0])

        assert("description" in playbook.parserdata[0])

        assert("task_names" in playbook.parserdata[0])

        assert(playbook.parserdata[0]["rolename"] is None)

    def test_parser_role_playbook(self):
        # Find Directory Of This Test
        localdir = os.path.dirname(os.path.realpath(__file__))
        # Create Tasks Directory
        if not os.path.exists(os.path.join(localdir, ".output/tasks/")):
            os.makedirs(os.path.join(localdir, ".output/tasks/"))
        # Set Output File
        testfile = os.path.join(localdir, ".output/tasks/main.yml")
        with open(testfile, "w") as f:
            f.write("---\n")
            f.write("# Author: Me\n")
            f.write("# description: this is a test\n")
            f.write("- name: 'Install Apache'\n")
            f.write("  yum: name=httpd state=installed\n")

        playbook = PlaybookParser([testfile], is_role=True)

        playbook.parse_playbooks()

        # One Element in Array
        assert(len(playbook.parserdata) == 1)

        assert("author" in playbook.parserdata[0])

        assert("description" in playbook.parserdata[0])

        assert("task_names" in playbook.parserdata[0])

        assert(playbook.parserdata[0]["rolename"] == ".output")
