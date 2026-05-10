import pytest
from ansibledocgen.formatter.formatter import Formatter


@pytest.fixture
def playbook_entry():
    return {
        "name": "site",
        "relative_path": "/project/site.yml",
        "author": "Alice",
        "description": "Deploy everything",
        "is_role": False,
        "task_info": [
            {"task_name": "Install nginx", "task_tags": ["web"]},
            {"task_name": "Start nginx", "task_tags": None},
        ],
    }


@pytest.fixture
def role_entry():
    return {
        "name": "nginx",
        "relative_path": "/project/roles/nginx/tasks/main.yml",
        "author": "Bob",
        "description": "NGINX role",
        "is_role": True,
        "task_info": [
            {"task_name": "Install package", "task_tags": None},
        ],
    }


@pytest.fixture
def rendered(tmp_path, playbook_entry, role_entry):
    playbook_dir = tmp_path / "playbooks"
    playbook_dir.mkdir()
    role_dir = tmp_path / "roles"
    role_dir.mkdir()
    host_dir = tmp_path / "host_vars"
    host_dir.mkdir()

    parserdata = {
        "playbooks": {str(playbook_dir): [playbook_entry]},
        "roles": {str(role_dir): [role_entry]},
        "host_vars": {},
    }
    paths = {"role": [str(role_dir)], "playbooks": [[]], "host": [str(host_dir)]}
    fmt = Formatter("markdown", parserdata, paths, str(tmp_path), {"show_tags": True})
    fmt.parse_data()
    fmt.write_files()
    return tmp_path


def test_write_files_creates_readme_in_playbook_dir(rendered):
    assert (rendered / "playbooks" / "README.md").exists()


def test_write_files_creates_readme_in_role_dir(rendered):
    assert (rendered / "roles" / "README.md").exists()


def test_playbook_author_and_description_in_output(rendered):
    content = (rendered / "playbooks" / "README.md").read_text()
    assert "Alice" in content
    assert "Deploy everything" in content


def test_task_names_in_playbook_output(rendered):
    content = (rendered / "playbooks" / "README.md").read_text()
    assert "Install nginx" in content
    assert "Start nginx" in content


def test_tags_shown_when_show_tags_true(rendered):
    content = (rendered / "playbooks" / "README.md").read_text()
    assert "web" in content


def test_tags_hidden_when_show_tags_false(tmp_path, playbook_entry, role_entry):
    playbook_dir = tmp_path / "playbooks"
    playbook_dir.mkdir()
    role_dir = tmp_path / "roles"
    role_dir.mkdir()
    host_dir = tmp_path / "host_vars"
    host_dir.mkdir()
    parserdata = {
        "playbooks": {str(playbook_dir): [playbook_entry]},
        "roles": {str(role_dir): [role_entry]},
        "host_vars": {},
    }
    paths = {"role": [str(role_dir)], "playbooks": [[]], "host": [str(host_dir)]}
    fmt = Formatter("markdown", parserdata, paths, str(tmp_path), {"show_tags": False})
    fmt.parse_data()
    fmt.write_files()
    assert "web" not in (playbook_dir / "README.md").read_text()


def test_role_rendered_with_role_heading(rendered):
    content = (rendered / "roles" / "README.md").read_text()
    assert "## Role: [nginx]" in content
    assert "Bob" in content
    assert "NGINX role" in content


def test_readme_top_prepended(tmp_path, playbook_entry, role_entry):
    playbook_dir = tmp_path / "playbooks"
    playbook_dir.mkdir()
    (playbook_dir / "README-TOP.md").write_text("# My Project\n")
    role_dir = tmp_path / "roles"
    role_dir.mkdir()
    host_dir = tmp_path / "host_vars"
    host_dir.mkdir()
    parserdata = {
        "playbooks": {str(playbook_dir): [playbook_entry]},
        "roles": {str(role_dir): [role_entry]},
        "host_vars": {},
    }
    paths = {"role": [str(role_dir)], "playbooks": [[]], "host": [str(host_dir)]}
    fmt = Formatter("markdown", parserdata, paths, str(tmp_path), {"show_tags": True})
    fmt.parse_data()
    fmt.write_files()
    assert (playbook_dir / "README.md").read_text().startswith("# My Project\n")


def test_readme_bottom_appended(tmp_path, playbook_entry, role_entry):
    playbook_dir = tmp_path / "playbooks"
    playbook_dir.mkdir()
    (playbook_dir / "README-BOTTOM.md").write_text("# Footer\n")
    role_dir = tmp_path / "roles"
    role_dir.mkdir()
    host_dir = tmp_path / "host_vars"
    host_dir.mkdir()
    parserdata = {
        "playbooks": {str(playbook_dir): [playbook_entry]},
        "roles": {str(role_dir): [role_entry]},
        "host_vars": {},
    }
    paths = {"role": [str(role_dir)], "playbooks": [[]], "host": [str(host_dir)]}
    fmt = Formatter("markdown", parserdata, paths, str(tmp_path), {"show_tags": True})
    fmt.parse_data()
    fmt.write_files()
    assert (playbook_dir / "README.md").read_text().endswith("# Footer\n")


def test_custom_output_filename(tmp_path, playbook_entry, role_entry):
    playbook_dir = tmp_path / "playbooks"
    playbook_dir.mkdir()
    role_dir = tmp_path / "roles"
    role_dir.mkdir()
    host_dir = tmp_path / "host_vars"
    host_dir.mkdir()
    parserdata = {
        "playbooks": {str(playbook_dir): [playbook_entry]},
        "roles": {str(role_dir): [role_entry]},
        "host_vars": {},
    }
    paths = {"role": [str(role_dir)], "playbooks": [[]], "host": [str(host_dir)]}
    fmt = Formatter("markdown", parserdata, paths, str(tmp_path), {"show_tags": True})
    fmt.parse_data()
    fmt.write_files(filename="DOCS")
    assert (playbook_dir / "DOCS.md").exists()
    assert not (playbook_dir / "README.md").exists()
