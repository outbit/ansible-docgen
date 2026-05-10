"""Host Vars Parser Module"""

from pathlib import Path
from ansibledocgen.core.docgenyaml import load_yaml
import re


class HostVarsParser:
    def __init__(self, paths: list[str]) -> None:
        self.paths = paths
        self.parserdata: dict = {}

    def parse_hosts_vars(self) -> None:
        for path in self.paths:
            path_obj = Path(path)
            if path_obj.is_dir():
                for folder in path_obj.iterdir():
                    host_vars = self.parse_host_vars(folder)
                    if host_vars is not None:
                        self.parserdata[folder.name] = host_vars

    def parse_host_vars(self, path: Path | str) -> dict | None:
        path_obj = Path(path)
        if not path_obj.is_dir():
            return None

        structure: dict = {}
        for item in path_obj.iterdir():
            if not item.is_file() or item.name.startswith(".") or "swp" in item.name:
                continue
            structure[item.name] = {"relative_path": str(item)}
            data = item.read_text(encoding="utf-8", errors="ignore")
            for line in data.splitlines():
                m = re.match(r"^[ ]*#[ ]*(.*?)[ ]*:[ ]*(.*?)$", line)
                if m:
                    attribute = m.group(1).lower()
                    if attribute in ("author", "description"):
                        structure[item.name][attribute] = m.group(2)
            yamldata = load_yaml(data)
            if yamldata is None:
                del structure[item.name]
                continue
            structure[item.name]["variables"] = dict(yamldata)

        return structure if structure else None
