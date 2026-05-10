"""Playbook Module"""

from pathlib import Path
from typing import Any
from ansibledocgen.core.docgenyaml import load_yaml
import re


class PlaybookParser:
    """Parse An Individual Playbook"""

    def __init__(self, playbooks: list[str], is_role: bool = False) -> None:
        self.playbooks = playbooks
        self.parserdata: dict[str, list[dict]] = {}
        self.is_role = is_role
        self.already_parsed_playbooks: list[str] = []

    def parse_playbooks(self) -> None:
        for playbook in self.playbooks:
            self.parse_playbook(playbook)

    def _get_task_info(self, tasks: Any) -> list[dict]:
        task_info_list: list[dict] = []
        if isinstance(tasks, list):
            for task in tasks:
                task_info_list += self._get_task_info(task)
        else:
            if "name" in tasks:
                task_info: dict = {"task_name": tasks["name"], "task_tags": None}
                if tasks.get("tags") is not None:
                    task_info["task_tags"] = tasks["tags"]
                task_info_list.append(task_info)
            for key in ("always", "block", "rescue"):
                if key in tasks:
                    task_info_list += self._get_task_info(tasks[key])
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

        for yaml_item in yamldata:
            tasks = (
                yaml_item.get("tasks", yaml_item)
                if isinstance(yaml_item, dict)
                else yaml_item
            )
            task_info = self._get_task_info(tasks)
            if task_info:
                playbookentry["task_info"] += task_info

        if folder_content not in self.parserdata:
            self.parserdata[folder_content] = []
        self.parserdata[folder_content].append(playbookentry)
