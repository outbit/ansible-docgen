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
