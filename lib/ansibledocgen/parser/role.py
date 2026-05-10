"""Role Parser Module"""

from pathlib import Path
from ansibledocgen.parser.playbook import PlaybookParser


class RoleParser:
    """Parse Roles in Project"""

    def __init__(self, role_paths: list[str]) -> None:
        self.role_paths = role_paths
        self.main_tasks: list[str] = []
        self.parserdata: dict = {}
        self._task_roles_path: dict[str, Path] = {}

        self.find_main_tasks()
        self.parse_main_tasks()

    def find_main_tasks(self) -> None:
        for role_path in self.role_paths:
            rp = Path(role_path)
            for main_task in rp.rglob("tasks/main.yml"):
                task_str = str(main_task)
                self.main_tasks.append(task_str)
                self._task_roles_path[task_str] = rp

    def parse_main_tasks(self) -> None:
        self.playbookparser = PlaybookParser(
            self.main_tasks, is_role=True, roles_paths=self._task_roles_path
        )
        self.playbookparser.parse_playbooks()
        self.parserdata = self.playbookparser.parserdata
