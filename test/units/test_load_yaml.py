from ansibledocgen.core.docgenyaml import load_yaml


def test_parses_simple_key_value():
    result = load_yaml("key: value\n")
    assert result["key"] == "value"


def test_parses_list_of_dicts():
    result = load_yaml("---\n- name: first task\n  shell: echo hi\n")
    assert isinstance(result, list)
    assert result[0]["name"] == "first task"


def test_vault_tag_returns_secret_instead_of_failing():
    yaml = (
        "---\n"
        "password: !vault |\n"
        "  $ANSIBLE_VAULT;1.1;AES256\n"
        "  30313837366338643364386232316562\n"
    )
    result = load_yaml(yaml)
    assert result["password"] == "secret"


def test_empty_yaml_returns_none():
    assert load_yaml("---\n") is None
    assert load_yaml("") is None
