from unittest.mock import MagicMock
from prefect_gitlab.credentials import GitLabCredentials, Gitlab


def test_gitlab_credentials_get_client(monkeypatch):
    mock_gitlab = MagicMock()
    monkeypatch.setattr("prefect_gitlab.credentials.Gitlab", mock_gitlab)
    gitlab_credentials = GitLabCredentials(
        url="https://gitlab.example.com", token="my-token"
    )
    gitlab_credentials.get_client()
    mock_gitlab.assert_called_once_with(
        url=gitlab_credentials.url, oauth_token=gitlab_credentials.token
    )
    mock_gitlab.assert_called_once()
