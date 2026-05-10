import sys
from ansibledocgen.cli import Cli


def test_project():
    sys.argv = [sys.argv[0], "-p", "testdir"]
    cli = Cli()
    assert cli.project == "testdir/"
    assert cli.style == "markdown"

    sys.argv = [sys.argv[0]]
    cli = Cli()
    assert cli.project == "./"
    assert cli.style == "markdown"


def test_style():
    sys.argv = [sys.argv[0], "-s", "markdown"]
    cli = Cli()
    assert cli.style == "markdown"


def test_filename():
    sys.argv = [sys.argv[0], "-f", "test_filename.md"]
    cli = Cli()
    assert cli.filename == "test_filename"


def test_ignore_attrs_multiple():
    sys.argv = [sys.argv[0], "-i", "author,task"]
    cli = Cli()
    assert cli.params["ignore_attrs"] == ["author", "task"]


def test_ignore_attrs_single():
    sys.argv = [sys.argv[0], "-i", "author"]
    cli = Cli()
    assert cli.params["ignore_attrs"] == ["author"]


def test_ignore_attrs_default_empty():
    sys.argv = [sys.argv[0]]
    cli = Cli()
    assert cli.params["ignore_attrs"] == []


def test_ignore_attrs_strips_whitespace():
    sys.argv = [sys.argv[0], "-i", " author , task "]
    cli = Cli()
    assert cli.params["ignore_attrs"] == ["author", "task"]
