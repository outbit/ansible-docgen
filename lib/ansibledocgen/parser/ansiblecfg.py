"""Ansible Config Module"""

from pathlib import Path
import os
import re


class AnsibleCfg:
    """Parse an Ansible Config File"""

    def __init__(self, project: str) -> None:
        self.project = project
        self.config: str | None = None
        self.settings: dict[str, str] = {}
        self.find_config()

    def find_config(self) -> None:
        config_files = (
            os.environ.get("ANSIBLE_CFG"),
            str(Path(self.project) / "ansible.cfg"),
            str(Path.home() / ".ansible.cfg"),
            "/etc/ansible/ansible.cfg",
        )
        for config in config_files:
            if config is not None and Path(config).is_file():
                self.load_config(config)
                break

    def load_config(self, filename: str) -> None:
        self.config = Path(filename).read_text(encoding="utf-8")
        for line in self.config.splitlines():
            m = re.match(r"^[ ]*(.*?)[ ]*=[ ]*(.*?)$", line)
            if m:
                self.settings[m.group(1)] = m.group(2)

    def get_role_paths(self) -> list[str]:
        if "roles_path" not in self.settings:
            return [str(Path(self.project) / "roles")]
        role_paths = self.settings["roles_path"].split(":")
        role_full_paths = [
            str(Path(self.project) / rp.strip("./")) for rp in role_paths
        ]
        if not any("/roles" in rp for rp in role_full_paths):
            role_full_paths.append(str(Path(self.project) / "roles"))
        return role_full_paths

    def get_playbook_paths(self) -> list[str]:
        role_paths = [Path(rp) for rp in self.get_role_paths()]
        return sorted(
            str(p)
            for p in Path(self.project).rglob("*.yml")
            if not any(p.is_relative_to(rp) for rp in role_paths)
        )

    def get_hosts_paths(self) -> list[str]:
        return [str(Path(self.project) / "host_vars")]
