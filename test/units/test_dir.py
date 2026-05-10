from ansibledocgen.parser.dir import DirParser
import unittest
import os
from pathlib import Path

INTEGRATION = Path(__file__).parent.parent / "integration"


class TestDir(unittest.TestCase):
    def test_parserdata(self):
        localdir = os.path.dirname(os.path.realpath(__file__))
        projectunit = os.path.join(localdir, "../integration/projectunit")
        dirparser = DirParser(projectunit)
        parserdata = dirparser.get_parserdata()

        # Check for expected attributes in sourcedata
        assert "playbooks" in parserdata
        for folder_content, sourcedata in parserdata["playbooks"].items():
            assert "name" in sourcedata[0]
            assert "relative_path" in sourcedata[0]
        assert "roles" in parserdata
        for folder_content, sourcedata in parserdata["roles"].items():
            assert "name" in sourcedata[0]
            assert "relative_path" in sourcedata[0]
        assert "host_vars" in parserdata
        for hostname, contents in parserdata["host_vars"].items():
            assert "host_1" in hostname
            assert "position" in contents
            assert "relative_path" in contents["position"]


def test_role_task_files_not_in_playbooks():
    dirparser = DirParser(str(INTEGRATION / "project1"))
    parserdata = dirparser.get_parserdata()
    all_playbook_paths = [
        e["relative_path"]
        for entries in parserdata["playbooks"].values()
        for e in entries
    ]
    assert (
        str(INTEGRATION / "project1" / "roles" / "basic" / "tasks" / "main.yml")
        not in all_playbook_paths
    )
    assert (
        str(INTEGRATION / "project1" / "roles" / "advanced" / "tasks" / "main.yml")
        not in all_playbook_paths
    )
    assert (
        str(INTEGRATION / "project1" / "rolestest" / "apache" / "tasks" / "main.yml")
        not in all_playbook_paths
    )


def test_multiple_roles_discovered():
    dirparser = DirParser(str(INTEGRATION / "project1"))
    parserdata = dirparser.get_parserdata()
    all_entries = [e for entries in parserdata["roles"].values() for e in entries]
    role_names = {e["name"] for e in all_entries}
    assert "basic" in role_names
    assert "advanced" in role_names
    assert "apache" in role_names


def test_host_vars_parsed_when_present():
    dirparser = DirParser(str(INTEGRATION / "project5"))
    parserdata = dirparser.get_parserdata()
    assert "host_1" in parserdata["host_vars"]
    assert "position" in parserdata["host_vars"]["host_1"]


def test_parserdata_top_level_keys():
    dirparser = DirParser(str(INTEGRATION / "project1"))
    parserdata = dirparser.get_parserdata()
    assert set(parserdata.keys()) == {"playbooks", "roles", "host_vars"}


def test_custom_roles_path_in_ansible_cfg():
    # project3 has roles_path = ./otherroles in ansible.cfg
    dirparser = DirParser(str(INTEGRATION / "project3"))
    parserdata = dirparser.get_parserdata()
    all_entries = [e for entries in parserdata["roles"].values() for e in entries]
    role_names = {e["name"] for e in all_entries}
    assert "apache" in role_names
