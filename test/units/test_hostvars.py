from pathlib import Path
from ansibledocgen.parser.hostvars import HostVarsParser

INTEGRATION = Path(__file__).parent.parent / "integration"
PROJECT5 = INTEGRATION / "project5"


def test_parses_variables_from_host_vars_files():
    parser = HostVarsParser([str(PROJECT5 / "host_vars")])
    parser.parse_hosts_vars()
    assert "host_1" in parser.parserdata
    variables = parser.parserdata["host_1"]["position"]["variables"]
    assert "host_city" in variables
    assert variables["host_city"] == "San Carlos de Bariloche"
    assert "host_coor_lat" in variables


def test_multiple_var_files_per_host():
    parser = HostVarsParser([str(PROJECT5 / "host_vars")])
    parser.parse_hosts_vars()
    host = parser.parserdata["host_1"]
    assert "position" in host
    assert "ansible_settings" in host


def test_relative_path_stored_per_file():
    parser = HostVarsParser([str(PROJECT5 / "host_vars")])
    parser.parse_hosts_vars()
    assert "relative_path" in parser.parserdata["host_1"]["position"]


def test_nonexistent_host_vars_dir_produces_empty_parserdata(tmp_path):
    parser = HostVarsParser([str(tmp_path / "nonexistent")])
    parser.parse_hosts_vars()
    assert parser.parserdata == {}


def test_author_and_description_parsed_from_comments(tmp_path):
    host_dir = tmp_path / "host_vars" / "myhost"
    host_dir.mkdir(parents=True)
    (host_dir / "vars.yml").write_text(
        "# author: Alice\n# description: My host vars\nfoo: bar\n"
    )
    parser = HostVarsParser([str(tmp_path / "host_vars")])
    parser.parse_hosts_vars()
    entry = parser.parserdata["myhost"]["vars.yml"]
    assert entry["author"] == "Alice"
    assert entry["description"] == "My host vars"


def test_dotfiles_skipped(tmp_path):
    host_dir = tmp_path / "host_vars" / "myhost"
    host_dir.mkdir(parents=True)
    (host_dir / ".hidden").write_text("secret: value\n")
    (host_dir / "visible.yml").write_text("key: value\n")
    parser = HostVarsParser([str(tmp_path / "host_vars")])
    parser.parse_hosts_vars()
    assert ".hidden" not in parser.parserdata.get("myhost", {})
    assert "visible.yml" in parser.parserdata["myhost"]


def test_empty_yaml_file_excluded_from_results(tmp_path):
    host_dir = tmp_path / "host_vars" / "myhost"
    host_dir.mkdir(parents=True)
    (host_dir / "empty.yml").write_text("---\n")
    (host_dir / "real.yml").write_text("key: value\n")
    parser = HostVarsParser([str(tmp_path / "host_vars")])
    parser.parse_hosts_vars()
    assert "empty.yml" not in parser.parserdata.get("myhost", {})
    assert "real.yml" in parser.parserdata["myhost"]


def test_host_with_all_empty_files_not_in_parserdata(tmp_path):
    host_dir = tmp_path / "host_vars" / "emptyhost"
    host_dir.mkdir(parents=True)
    (host_dir / "empty.yml").write_text("---\n")
    parser = HostVarsParser([str(tmp_path / "host_vars")])
    parser.parse_hosts_vars()
    assert "emptyhost" not in parser.parserdata
