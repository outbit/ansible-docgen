from pathlib import Path
from jinja2 import Template


class Formatter:
    def __init__(
        self, style: str, parserdata: dict, paths: dict, project: str, params: dict
    ) -> None:
        self.parserdata = parserdata
        self.paths = paths
        self.project = project
        self.params = params
        self.render_files: dict[str, dict[str, str]] = dict(
            playbook=dict(), roles=dict(), host=dict()
        )
        self.templates_dir = Path(__file__).parent / "templates"
        self.templates_files = {
            "playbook": f"{style}_playbook.j2",
            "role": f"{style}_role.j2",
            "host": f"{style}_host.j2",
        }

    def parse_data(self) -> None:
        self._make_playbook_template()
        self._make_role_template()
        self._make_host_vars()

    def write_files(self, filename: str = "README") -> None:
        for type_, content in self.render_files.items():
            for path_content, render_file in content.items():
                path_obj = Path(path_content)
                readme_top = path_obj / "README-TOP.md"
                readme_bottom = path_obj / "README-BOTTOM.md"
                readme_top_content = (
                    readme_top.read_text(encoding="utf-8")
                    if readme_top.exists()
                    else ""
                )
                readme_bottom_content = (
                    readme_bottom.read_text(encoding="utf-8")
                    if readme_bottom.exists()
                    else ""
                )
                if path_obj.is_dir():
                    (path_obj / f"{filename}.md").write_text(
                        readme_top_content
                        + "\n"
                        + render_file
                        + "\n"
                        + readme_bottom_content,
                        encoding="utf-8",
                    )

    def _make_playbook_template(self) -> None:
        template = Template(
            (self.templates_dir / self.templates_files["playbook"]).read_text(
                encoding="utf-8"
            )
        )
        for content in self.parserdata["playbooks"]:
            self.render_files["playbook"][content] = template.render(
                data=self.parserdata["playbooks"][content], params=self.params
            )

    def _make_role_template(self) -> None:
        template = Template(
            (self.templates_dir / self.templates_files["role"]).read_text(
                encoding="utf-8"
            )
        )
        for content in self.parserdata["roles"]:
            self.render_files["roles"][content] = template.render(
                data=self.parserdata["roles"][content], params=self.params
            )

    def _make_host_vars(self) -> None:
        template = Template(
            (self.templates_dir / self.templates_files["host"]).read_text(
                encoding="utf-8"
            )
        )
        self.render_files["host"][self.paths["host"][0]] = template.render(
            data=self.parserdata["host_vars"], params=self.params
        )
