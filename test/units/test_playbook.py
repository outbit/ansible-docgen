import unittest
import os
from pathlib import Path
from ansibledocgen.parser.playbook import PlaybookParser


class TestPlaybook(unittest.TestCase):
    def test_parser_playbook(self):
        localdir = os.path.dirname(os.path.realpath(__file__))
        testfile = os.path.join(localdir, ".output/testplaybook.yml")
        folder_testfile = os.path.join(localdir, ".output")
        Path(testfile).write_text(
            "---\n"
            "# Author: Me شيشه ب\n"
            "# description: this is a test شيشه ب\n"
            "- hosts: testhoشيشهsts\n"
            "  tasks:\n"
            "     - name: 'Install Apache شيشه ب'\n"
            "       yum: name=httpd state=inشtalled\n"
            "       tags:\n"
            "           - apache\n",
            encoding="utf-8",
        )

        playbook = PlaybookParser([testfile], is_role=False)
        playbook.parse_playbooks()

        assert len(playbook.parserdata) == 1
        assert "author" in playbook.parserdata[folder_testfile][0]
        assert "description" in playbook.parserdata[folder_testfile][0]
        assert "task_info" in playbook.parserdata[folder_testfile][0]
        assert "task_name" in playbook.parserdata[folder_testfile][0]["task_info"][0]
        assert "task_tags" in playbook.parserdata[folder_testfile][0]["task_info"][0]
        assert playbook.parserdata[folder_testfile][0]["is_role"] is False

    def test_parser_role_playbook(self):
        localdir = os.path.dirname(os.path.realpath(__file__))
        tasks_dir = Path(localdir) / ".output" / "tasks"
        tasks_dir.mkdir(parents=True, exist_ok=True)
        testfile = str(tasks_dir / "main.yml")
        folder_testfile = localdir
        Path(testfile).write_text(
            "---\n"
            "# Author: Me\n"
            "# description: this is a test\n"
            "- name: 'Install Apache'\n"
            "  yum: name=httpd state=installed\n"
            "  tags:\n"
            "    - apache\n",
            encoding="utf-8",
        )

        playbook = PlaybookParser([testfile], is_role=True)
        playbook.parse_playbooks()

        assert len(playbook.parserdata) == 1
        assert "author" in playbook.parserdata[folder_testfile][0]
        assert "description" in playbook.parserdata[folder_testfile][0]
        assert "task_info" in playbook.parserdata[folder_testfile][0]
        assert "task_name" in playbook.parserdata[folder_testfile][0]["task_info"][0]
        assert "task_tags" in playbook.parserdata[folder_testfile][0]["task_info"][0]
        assert playbook.parserdata[folder_testfile][0]["name"] == ".output"
