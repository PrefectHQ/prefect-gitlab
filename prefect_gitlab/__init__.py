from . import _version
from .filesystems import GitLab  # noqa

__version__ = _version.get_versions()["version"]
