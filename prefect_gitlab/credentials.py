"""Module used to enable authenticated interactions with GitLab"""

from prefect.blocks.core import Block
from pydantic import Field, HttpUrl, SecretStr


class GitLabCredentials(Block):
    """
    Store a GitLab personal access token to interact with private GitLab
    repositories.

    Attributes:
        token: The token to authenticate into GitLab.

    Examples:
        Load stored GitLab credentials:
        ```python
        from prefect_gitlab import GitLabCredentials
        gitlab_credentials_block = GitLabCredentials.load("BLOCK_NAME")
        ```
    """

    _block_type_name = "GitLab Credentials"
    _logo_url = HttpUrl(
        url="https://images.ctfassets.net/gm98wzqotmnx/55edIimT4g9gbjhkh5a3Sp/dfdb9391d8f45c2e93e72e3a4d350771/gitlab-logo-500.png?h=250",  # noqa
        scheme="https",
    )

    token: SecretStr = Field(
        name="Personal Access Token",
        default=None,
        description="A GitLab Personal Access Token with repo scope.",
    )
