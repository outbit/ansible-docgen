from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("ansible-docgen")
except PackageNotFoundError:
    __version__ = "unknown"

__author__ = "David Whiteside"
