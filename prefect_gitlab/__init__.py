from . import _version
from .repositories import GitLabRepository

__version__ = _version.get_versions()["version"]
__all__ = ["GitLabRepository"]
