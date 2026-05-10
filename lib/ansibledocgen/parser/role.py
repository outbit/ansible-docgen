"""Role Parser Module"""

from pathlib import Path
from ansibledocgen.parser.playbook import PlaybookParser


class RoleParser:
    """Parse Roles in Project"""

    def __init__(self, role_paths: list[str]) -> None:
        self.role_paths = role_paths
        self.main_tasks: list[str] = []
        self.parserdata: dict = {}

        self.find_main_tasks()
        self.parse_main_tasks()

    def find_main_tasks(self) -> None:
        for role_path in self.role_paths:
            for main_task in Path(role_path).rglob("tasks/main.yml"):
                self.main_tasks.append(str(main_task))

    def parse_main_tasks(self) -> None:
        self.playbookparser = PlaybookParser(self.main_tasks, is_role=True)
        self.playbookparser.parse_playbooks()
        self.parserdata = self.playbookparser.parserdata
