import os
import unittest
from ansibledocgen.parser.ansiblecfg import AnsibleCfg


class TestAnsibleCfg(unittest.TestCase):
    def test_ansiblecfg(self):
        localdir = os.path.dirname(os.path.realpath(__file__))
        testfile = os.path.join(localdir, ".output/ansible.cfg")
        with open(testfile, "w") as f:
            f.write("\n roles_path = role1:role2\n")

        ansiblecfg = AnsibleCfg(os.path.dirname(testfile))

        assert "roles_path" in ansiblecfg.settings
        assert "role1" in ansiblecfg.settings["roles_path"]
        assert "role2" in ansiblecfg.settings["roles_path"]


def test_default_role_path_when_no_config(tmp_path):
    cfg = AnsibleCfg(str(tmp_path))
    paths = cfg.get_role_paths()
    assert paths == [str(tmp_path / "roles")]


def test_multiple_role_paths_from_config(tmp_path):
    (tmp_path / "ansible.cfg").write_text(
        "[defaults]\nroles_path = ./roles:./otherroles\n"
    )
    cfg = AnsibleCfg(str(tmp_path))
    paths = cfg.get_role_paths()
    assert str(tmp_path / "roles") in paths
    assert str(tmp_path / "otherroles") in paths


def test_default_roles_dir_appended_when_absent(tmp_path):
    (tmp_path / "ansible.cfg").write_text("[defaults]\nroles_path = ./custom\n")
    cfg = AnsibleCfg(str(tmp_path))
    paths = cfg.get_role_paths()
    assert str(tmp_path / "custom") in paths
    assert str(tmp_path / "roles") in paths


def test_get_playbook_paths_excludes_role_files(tmp_path):
    role_task = tmp_path / "roles" / "myrole" / "tasks"
    role_task.mkdir(parents=True)
    (role_task / "main.yml").write_text("---\n- name: role task\n  shell: echo hi\n")
    (tmp_path / "site.yml").write_text("---\n- hosts: all\n")
    cfg = AnsibleCfg(str(tmp_path))
    playbooks = cfg.get_playbook_paths()
    assert str(tmp_path / "site.yml") in playbooks
    assert str(role_task / "main.yml") not in playbooks


def test_get_playbook_paths_returns_sorted_list(tmp_path):
    for name in ("zebra.yml", "alpha.yml", "middle.yml"):
        (tmp_path / name).write_text("---\n")
    cfg = AnsibleCfg(str(tmp_path))
    playbooks = cfg.get_playbook_paths()
    assert playbooks == sorted(playbooks)


def test_get_hosts_paths_returns_host_vars_dir(tmp_path):
    cfg = AnsibleCfg(str(tmp_path))
    assert cfg.get_hosts_paths() == [str(tmp_path / "host_vars")]
