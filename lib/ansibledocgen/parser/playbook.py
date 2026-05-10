"""Playbook Module"""

from pathlib import Path
from typing import Any
from ansibledocgen.core.docgenyaml import load_yaml
import re

_INCLUDE_KEYS = ("include", "include_tasks", "import_tasks")


class PlaybookParser:
    """Parse An Individual Playbook"""

    def __init__(
        self,
        playbooks: list[str],
        is_role: bool = False,
        roles_paths: dict[str, Path] | None = None,
    ) -> None:
        self.playbooks = playbooks
        self.parserdata: dict[str, list[dict]] = {}
        self.is_role = is_role
        self.roles_paths: dict[str, Path] = roles_paths or {}
        self.already_parsed_playbooks: list[str] = []

    def parse_playbooks(self) -> None:
        for playbook in self.playbooks:
            self.parse_playbook(playbook)

    def _resolve_task_file(self, task: dict, base_path: Path) -> Path | None:
        """Return the path for the first task-file include directive found, or None."""
        for key in _INCLUDE_KEYS:
            if key not in task:
                continue
            include_val = task[key]
            if isinstance(include_val, str):
                return base_path / include_val.split()[0]
            if isinstance(include_val, dict) and "file" in include_val:
                return base_path / include_val["file"]
        return None

    def _resolve_role_file(self, task: dict, roles_path: Path) -> Path | None:
        """Return the tasks/main.yml path for an include_role/import_role directive, or None."""
        for key in ("include_role", "import_role"):
            if key not in task:
                continue
            role_def = task[key]
            if not isinstance(role_def, dict) or "name" not in role_def:
                continue
            tasks_from = role_def.get("tasks_from", "main.yml")
            if not tasks_from.endswith(".yml"):
                tasks_from += ".yml"
            return roles_path / role_def["name"] / "tasks" / tasks_from
        return None

    def _get_task_info(
        self, tasks: Any, base_path: Path | None = None, roles_path: Path | None = None
    ) -> list[dict]:
        task_info_list: list[dict] = []
        if isinstance(tasks, list):
            for task in tasks:
                task_info_list += self._get_task_info(task, base_path, roles_path)
        else:
            if "name" in tasks:
                task_info: dict = {"task_name": tasks["name"], "task_tags": None}
                if tasks.get("tags") is not None:
                    task_info["task_tags"] = tasks["tags"]
                task_info_list.append(task_info)
            for key in ("always", "block", "rescue"):
                if key in tasks:
                    task_info_list += self._get_task_info(
                        tasks[key], base_path, roles_path
                    )
            if base_path is not None:
                include_path = self._resolve_task_file(tasks, base_path)
                if include_path is not None:
                    include_str = str(include_path)
                    if (
                        include_str not in self.already_parsed_playbooks
                        and include_path.exists()
                    ):
                        self.already_parsed_playbooks.append(include_str)
                        included_data = load_yaml(
                            include_path.read_text(encoding="utf-8")
                        )
                        if included_data is not None:
                            task_info_list += self._get_task_info(
                                included_data, include_path.parent, roles_path
                            )
            if roles_path is not None:
                include_path = self._resolve_role_file(tasks, roles_path)
                if include_path is not None and include_path.exists():
                    included_data = load_yaml(include_path.read_text(encoding="utf-8"))
                    if included_data is not None:
                        task_info_list += self._get_task_info(
                            included_data, include_path.parent, roles_path
                        )
        return task_info_list

    def parse_playbook(self, playbook: str) -> None:
        if playbook in self.already_parsed_playbooks:
            return
        self.already_parsed_playbooks.append(playbook)

        playbook_path = Path(playbook)
        if self.is_role:
            name = playbook_path.parents[1].name
            folder_content = str(playbook_path.parents[2])
        else:
            folder_content = str(playbook_path.parent)
            name = playbook_path.stem

        playbookentry: dict = {
            "relative_path": playbook,
            "name": name,
            "task_info": [],
            "is_role": self.is_role,
        }

        data = playbook_path.read_text(encoding="utf-8")

        for line in data.splitlines():
            m = re.match(r"^[ ]*#[ ]*(.*?)[ ]*:[ ]*(.*?)$", line)
            if m:
                attribute = m.group(1).lower()
                if attribute in ("author", "description"):
                    playbookentry[attribute] = m.group(2)

        yamldata = load_yaml(data)
        if yamldata is None:
            return

        base_path = playbook_path.parent if self.is_role else None
        roles_path = self.roles_paths.get(playbook) if self.is_role else None
        for yaml_item in yamldata:
            tasks = (
                yaml_item.get("tasks", yaml_item)
                if isinstance(yaml_item, dict)
                else yaml_item
            )
            task_info = self._get_task_info(tasks, base_path, roles_path)
            if task_info:
                playbookentry["task_info"] += task_info

        if folder_content not in self.parserdata:
            self.parserdata[folder_content] = []
        self.parserdata[folder_content].append(playbookentry)
