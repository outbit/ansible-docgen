from ansibledocgen.formatter.formatter import Formatter, apply_ignore_attrs


def test_apply_ignore_attrs_no_ignores():
    entry = {
        "author": "Alice",
        "description": "test",
        "task_info": [{"task_name": "t"}],
    }
    result = apply_ignore_attrs(entry, [])
    assert result == entry


def test_apply_ignore_attrs_removes_standard_attr():
    entry = {"author": "Alice", "description": "test", "task_info": []}
    result = apply_ignore_attrs(entry, ["author"])
    assert "author" not in result
    assert result["description"] == "test"


def test_apply_ignore_attrs_removes_multiple_attrs():
    entry = {"author": "Alice", "description": "test", "task_info": []}
    result = apply_ignore_attrs(entry, ["author", "description"])
    assert "author" not in result
    assert "description" not in result


def test_apply_ignore_attrs_task_clears_task_info():
    entry = {"author": "Alice", "task_info": [{"task_name": "deploy"}]}
    result = apply_ignore_attrs(entry, ["task"])
    assert result["task_info"] == []


def test_apply_ignore_attrs_missing_attr_is_noop():
    entry = {"author": "Alice"}
    result = apply_ignore_attrs(entry, ["nonexistent"])
    assert result == {"author": "Alice"}


def test_apply_ignore_attrs_does_not_mutate_original():
    entry = {"author": "Alice", "task_info": [{"task_name": "t"}]}
    apply_ignore_attrs(entry, ["author", "task"])
    assert entry["author"] == "Alice"
    assert len(entry["task_info"]) == 1


def test_apply_ignore_attrs_task_and_other_combined():
    entry = {"author": "Alice", "description": "d", "task_info": [{"task_name": "t"}]}
    result = apply_ignore_attrs(entry, ["author", "task"])
    assert "author" not in result
    assert result["task_info"] == []
    assert result["description"] == "d"


def _make_formatter(params):
    parserdata = {"playbooks": {}, "roles": {}, "host_vars": {}}
    paths = {"host": ["/tmp"]}
    return Formatter("markdown", parserdata, paths, "/tmp/", params)


def test_filter_data_no_ignores():
    entries = [{"author": "Alice", "task_info": [{"task_name": "t"}]}]
    f = _make_formatter({"ignore_attrs": []})
    result = f._filter_data(entries)
    assert result[0]["author"] == "Alice"
    assert result[0]["task_info"] == [{"task_name": "t"}]


def test_filter_data_ignores_author():
    entries = [{"author": "Alice", "description": "d", "task_info": []}]
    f = _make_formatter({"ignore_attrs": ["author"]})
    result = f._filter_data(entries)
    assert "author" not in result[0]
    assert result[0]["description"] == "d"


def test_filter_data_ignores_task():
    entries = [{"author": "Alice", "task_info": [{"task_name": "deploy"}]}]
    f = _make_formatter({"ignore_attrs": ["task"]})
    result = f._filter_data(entries)
    assert result[0]["task_info"] == []


def test_filter_data_empty_entries():
    f = _make_formatter({"ignore_attrs": ["author"]})
    assert f._filter_data([]) == []


def test_filter_data_missing_ignore_attrs_key():
    entries = [{"author": "Alice"}]
    f = _make_formatter({})
    result = f._filter_data(entries)
    assert result[0]["author"] == "Alice"
