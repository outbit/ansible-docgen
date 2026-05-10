from pathlib import Path
from ansibledocgen.parser.role import RoleParser

INTEGRATION = Path(__file__).parent.parent / "integration"


def test_finds_role_main_tasks():
    parser = RoleParser([str(INTEGRATION / "project1" / "roles")])
    assert any("basic" in t for t in parser.main_tasks)
    assert any("advanced" in t for t in parser.main_tasks)


def test_role_names_extracted_from_directory_structure():
    parser = RoleParser([str(INTEGRATION / "project1" / "roles")])
    all_entries = [e for entries in parser.parserdata.values() for e in entries]
    role_names = {e["name"] for e in all_entries}
    assert "basic" in role_names
    assert "advanced" in role_names


def test_all_roles_marked_as_is_role():
    parser = RoleParser([str(INTEGRATION / "project1" / "roles")])
    all_entries = [e for entries in parser.parserdata.values() for e in entries]
    assert all_entries, "Expected at least one role entry"
    assert all(e["is_role"] is True for e in all_entries)


def test_role_tasks_parsed():
    parser = RoleParser([str(INTEGRATION / "project1" / "roles")])
    all_entries = [e for entries in parser.parserdata.values() for e in entries]
    basic = next(e for e in all_entries if e["name"] == "basic")
    assert len(basic["task_info"]) > 0
    assert basic["task_info"][0]["task_name"] == "install nginx from roles"


def test_role_author_and_description_parsed():
    parser = RoleParser([str(INTEGRATION / "project1" / "roles")])
    all_entries = [e for entries in parser.parserdata.values() for e in entries]
    basic = next(e for e in all_entries if e["name"] == "basic")
    assert basic["author"] == "David Whiteside"
    assert basic["description"] == "Basic NGINX config"


def test_multiple_role_paths_all_discovered():
    parser = RoleParser(
        [
            str(INTEGRATION / "project1" / "roles"),
            str(INTEGRATION / "project1" / "rolestest"),
        ]
    )
    all_entries = [e for entries in parser.parserdata.values() for e in entries]
    role_names = {e["name"] for e in all_entries}
    assert "basic" in role_names
    assert "advanced" in role_names
    assert "apache" in role_names


def test_empty_role_dir_produces_no_results(tmp_path):
    parser = RoleParser([str(tmp_path)])
    assert parser.main_tasks == []
    assert parser.parserdata == {}


def test_role_include_tasks_followed(tmp_path):
    tasks_dir = tmp_path / "myrole" / "tasks"
    tasks_dir.mkdir(parents=True)
    (tasks_dir / "main.yml").write_text(
        "---\n- name: Main task\n  shell: echo main\n- include_tasks: extra.yml\n"
    )
    (tasks_dir / "extra.yml").write_text(
        "---\n- name: Extra task\n  shell: echo extra\n"
    )
    parser = RoleParser([str(tmp_path)])
    all_entries = [e for entries in parser.parserdata.values() for e in entries]
    names = [t["task_name"] for t in all_entries[0]["task_info"]]
    assert "Main task" in names
    assert "Extra task" in names


def test_role_include_followed(tmp_path):
    tasks_dir = tmp_path / "myrole" / "tasks"
    tasks_dir.mkdir(parents=True)
    (tasks_dir / "main.yml").write_text(
        '---\n- name: First task\n  shell: echo first\n- include: "extra.yml"\n'
    )
    (tasks_dir / "extra.yml").write_text(
        "---\n- name: Included task\n  shell: echo included\n"
    )
    parser = RoleParser([str(tmp_path)])
    all_entries = [e for entries in parser.parserdata.values() for e in entries]
    names = [t["task_name"] for t in all_entries[0]["task_info"]]
    assert "First task" in names
    assert "Included task" in names


def test_advanced_role_include_followed():
    parser = RoleParser([str(INTEGRATION / "project1" / "roles")])
    all_entries = [e for entries in parser.parserdata.values() for e in entries]
    advanced = next(e for e in all_entries if e["name"] == "advanced")
    names = [t["task_name"] for t in advanced["task_info"]]
    assert "install nginx" in names
    assert "Do Extra" in names


def test_playbook_include_not_followed(tmp_path):
    main_pb = tmp_path / "site.yml"
    other_pb = tmp_path / "other.yml"
    main_pb.write_text(
        "---\n"
        "- hosts: all\n"
        "  tasks:\n"
        "    - name: Main task\n"
        "      shell: echo main\n"
        "    - import_tasks: other_tasks.yml\n"
    )
    other_pb.write_text(
        "---\n- hosts: all\n  tasks:\n    - name: Other task\n      shell: echo other\n"
    )
    from ansibledocgen.parser.playbook import PlaybookParser

    parser = PlaybookParser([str(main_pb)], is_role=False)
    parser.parse_playbooks()
    names = [t["task_name"] for t in parser.parserdata[str(tmp_path)][0]["task_info"]]
    assert "Main task" in names
    assert "Other task" not in names
