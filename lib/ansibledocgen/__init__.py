from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("ansible-docgen")
except PackageNotFoundError:
    __version__ = "unknown"

__author__ = "David Whiteside"
