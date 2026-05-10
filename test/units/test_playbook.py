import unittest
import os
from pathlib import Path
from ansibledocgen.parser.playbook import PlaybookParser

INTEGRATION = Path(__file__).parent.parent / "integration"


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


def test_author_and_description_parsed(tmp_path):
    f = tmp_path / "site.yml"
    f.write_text(
        "---\n# author: Alice\n# description: My playbook\n- hosts: all\n  tasks:\n    - name: t\n      shell: echo hi\n"
    )
    parser = PlaybookParser([str(f)])
    parser.parse_playbooks()
    entry = parser.parserdata[str(tmp_path)][0]
    assert entry["author"] == "Alice"
    assert entry["description"] == "My playbook"


def test_block_rescue_always_tasks_extracted(tmp_path):
    f = tmp_path / "site.yml"
    f.write_text(
        "---\n"
        "- hosts: all\n"
        "  tasks:\n"
        "    - block:\n"
        "        - name: Block task\n"
        "          shell: echo block\n"
        "      rescue:\n"
        "        - name: Rescue task\n"
        "          shell: echo rescue\n"
        "      always:\n"
        "        - name: Always task\n"
        "          shell: echo always\n"
    )
    parser = PlaybookParser([str(f)])
    parser.parse_playbooks()
    names = [t["task_name"] for t in parser.parserdata[str(tmp_path)][0]["task_info"]]
    assert "Block task" in names
    assert "Rescue task" in names
    assert "Always task" in names


def test_playbook_without_comments_has_no_author_or_description(tmp_path):
    f = tmp_path / "site.yml"
    f.write_text(
        "---\n- hosts: all\n  tasks:\n    - name: My task\n      shell: echo hi\n"
    )
    parser = PlaybookParser([str(f)])
    parser.parse_playbooks()
    entry = parser.parserdata[str(tmp_path)][0]
    assert "author" not in entry
    assert "description" not in entry


def test_empty_yaml_file_produces_no_entries(tmp_path):
    f = tmp_path / "empty.yml"
    f.write_text("---\n")
    parser = PlaybookParser([str(f)])
    parser.parse_playbooks()
    assert len(parser.parserdata) == 0


def test_tasks_without_name_key_are_not_included(tmp_path):
    f = tmp_path / "site.yml"
    f.write_text(
        "---\n"
        "- hosts: all\n"
        "  tasks:\n"
        "    - shell: echo unnamed\n"
        "    - name: Named task\n"
        "      shell: echo named\n"
    )
    parser = PlaybookParser([str(f)])
    parser.parse_playbooks()
    tasks = parser.parserdata[str(tmp_path)][0]["task_info"]
    assert len(tasks) == 1
    assert tasks[0]["task_name"] == "Named task"


def test_same_file_not_parsed_twice(tmp_path):
    f = tmp_path / "site.yml"
    f.write_text(
        "---\n- hosts: all\n  tasks:\n    - name: My task\n      shell: echo hi\n"
    )
    path = str(f)
    parser = PlaybookParser([path, path])
    parser.parse_playbooks()
    assert len(parser.parserdata[str(tmp_path)]) == 1


def test_task_tags_stored(tmp_path):
    f = tmp_path / "site.yml"
    f.write_text(
        "---\n"
        "- hosts: all\n"
        "  tasks:\n"
        "    - name: Tagged task\n"
        "      shell: echo hi\n"
        "      tags:\n"
        "        - web\n"
        "        - nginx\n"
    )
    parser = PlaybookParser([str(f)])
    parser.parse_playbooks()
    task = parser.parserdata[str(tmp_path)][0]["task_info"][0]
    assert task["task_tags"] == ["web", "nginx"]


def test_real_playbook_with_blocks(tmp_path):
    src = INTEGRATION / "project1" / "basic_playbook.yml"
    import shutil

    dest = tmp_path / "basic_playbook.yml"
    shutil.copy(src, dest)
    parser = PlaybookParser([str(dest)])
    parser.parse_playbooks()
    entry = parser.parserdata[str(tmp_path)][0]
    assert entry["author"] == "David Whiteside"
    assert entry["description"] == "Installs and Configured Apache"
    names = [t["task_name"] for t in entry["task_info"]]
    assert "Install apache" in names
    assert "Second task in the playbook, first in the do block" in names
    assert "Third task in playbook, first in the rescue block" in names
    assert "Fourth task in playbook, first in the always block" in names
