from . import _version
from .credentials import GitLabCredentials
from .repositories import GitLabRepository

__version__ = _version.get_versions()["version"]
__all__ = ["GitLabRepository", "GitLabCredentials"]
