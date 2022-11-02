import os
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Set, Tuple

import pytest
from prefect.exceptions import InvalidRepositoryURLError
from prefect.testing.utilities import AsyncMock
from pydantic import SecretStr

import prefect_gitlab
from prefect_gitlab.filesystems import GitLab


class TestGitLab:
    def setup_test_directory(
        self, tmp_src: str, sub_dir: str = "puppy"
    ) -> Tuple[Set[str], Set[str]]:
        """Add files and directories to a temporary directory. Returns a tuple with the
        expected parent-level contents and the expected child-level contents.
        """
        # add file to tmp_src
        f1_name = "dog.text"
        f1_path = Path(tmp_src) / f1_name
        f1 = open(f1_path, "w")
        f1.close()

        # add sub-directory to tmp_src
        sub_dir_path = Path(tmp_src) / sub_dir
        os.mkdir(sub_dir_path)

        # add file to sub-directory
        f2_name = "cat.txt"
        f2_path = sub_dir_path / f2_name
        f2 = open(f2_path, "w")
        f2.close()

        parent_contents = {f1_name, sub_dir}
        child_contents = {f2_name}

        assert set(os.listdir(tmp_src)) == parent_contents
        assert set(os.listdir(sub_dir_path)) == child_contents

        return parent_contents, child_contents

    class MockTmpDir:
        """Utility for having `TemporaryDirectory` return a known location."""

        dir = None

        def __init__(self, *args, **kwargs):
            pass

        def __enter__(self):
            return self.dir

        def __exit__(self, *args, **kwargs):
            pass

    async def test_subprocess_errors_are_surfaced(self):
        g = GitLab(repository="incorrect-url-scheme")
        with pytest.raises(
            OSError, match="fatal: repository 'incorrect-url-scheme' does not exist"
        ):
            await g.get_directory()

    async def test_repository_default(self, monkeypatch):
        class p:
            returncode = 0

        mock = AsyncMock(return_value=p())
        monkeypatch.setattr(prefect_gitlab.filesystems, "run_process", mock)
        g = GitLab(repository="prefect")
        await g.get_directory()

        assert mock.await_count == 1
        expected_cmd = ["git", "clone", "prefect"]
        assert mock.await_args[0][0][: len(expected_cmd)] == expected_cmd

    async def test_reference_default(self, monkeypatch):
        class p:
            returncode = 0

        mock = AsyncMock(return_value=p())
        monkeypatch.setattr(prefect_gitlab.filesystems, "run_process", mock)
        g = GitLab(repository="prefect", reference="2.0.0")
        await g.get_directory()

        assert mock.await_count == 1
        expected_cmd = ["git", "clone", "prefect", "-b", "2.0.0", "--depth", "1"]
        assert mock.await_args[0][0][: len(expected_cmd)] == expected_cmd

    async def test_token_added_correctly_from_credential(self, monkeypatch):
        """Ensure that the repo url is in the format `https://<oauth-key>@github.com/<username>/<repo>.git`."""  # noqa: E501

        class p:
            returncode = 0

        mock = AsyncMock(return_value=p())
        monkeypatch.setattr(prefect_gitlab.filesystems, "run_process", mock)
        credential = "XYZ"
        repo = "https://gitlab.com/PrefectHQ/prefect.git"
        g = GitLab(
            repository=repo,
            access_token=SecretStr(credential),
        )
        await g.get_directory()
        assert mock.await_count == 1
        expected_cmd = [
            "git",
            "clone",
            f"https://oauth2:{credential}@gitlab.com/PrefectHQ/prefect.git",
            "--depth",
            "1",
        ]
        assert mock.await_args[0][0][: len(expected_cmd)] == expected_cmd

    async def test_ssh_fails_with_credential(self, monkeypatch):
        """Ensure that credentials cannot be passed in if the URL is not in the HTTPS
        format.
        """

        class p:
            returncode = 0

        mock = AsyncMock(return_value=p())
        monkeypatch.setattr(prefect_gitlab.filesystems, "run_process", mock)
        credential = "XYZ"
        error_msg = (
            "Crendentials can only be used with GitHub repositories "
            "using the 'HTTPS' format. You must either remove the "
            "credential if you wish to use the 'SSH' format and are not "
            "using a private repository, or you must change the repository "
            "URL to the 'HTTPS' format."
        )
        with pytest.raises(InvalidRepositoryURLError, match=error_msg):
            GitLab(
                repository="git@github.com:PrefectHQ/prefect.git",
                access_token=SecretStr(credential),
            )

    async def test_dir_contents_copied_correctly_with_get_directory(
        self, monkeypatch
    ):  # noqa
        """Check that `get_directory` is able to correctly copy contents from src->dst"""  # noqa

        class p:
            returncode = 0

        mock = AsyncMock(return_value=p())
        monkeypatch.setattr(prefect_gitlab.filesystems, "run_process", mock)

        sub_dir_name = "puppy"

        with TemporaryDirectory() as tmp_src:
            parent_contents, child_contents = self.setup_test_directory(
                tmp_src, sub_dir_name
            )
            self.MockTmpDir.dir = tmp_src

            # move file contents to tmp_dst
            with TemporaryDirectory() as tmp_dst:
                monkeypatch.setattr(
                    prefect_gitlab.filesystems,
                    "TemporaryDirectory",
                    self.MockTmpDir,
                )

                g = GitLab(
                    repository="https://github.com/PrefectHQ/prefect.git",
                )
                await g.get_directory(local_path=tmp_dst)

                assert set(os.listdir(tmp_dst)) == parent_contents
                assert set(os.listdir(Path(tmp_dst) / sub_dir_name)) == child_contents

    async def test_dir_contents_copied_correctly_with_get_directory_and_from_path(
        self, monkeypatch
    ):  # noqa
        """Check that `get_directory` is able to correctly copy contents from src->dst
        when `from_path` is included.
        It is expected that the directory specified by `from_path` will be moved to the
        specified destination, along with all of its contents.
        """

        class p:
            returncode = 0

        mock = AsyncMock(return_value=p())
        monkeypatch.setattr(prefect_gitlab.filesystems, "run_process", mock)

        sub_dir_name = "puppy"

        with TemporaryDirectory() as tmp_src:
            parent_contents, child_contents = self.setup_test_directory(
                tmp_src, sub_dir_name
            )
            self.MockTmpDir.dir = tmp_src

            # move file contents to tmp_dst
            with TemporaryDirectory() as tmp_dst:
                monkeypatch.setattr(
                    prefect_gitlab.filesystems,
                    "TemporaryDirectory",
                    self.MockTmpDir,
                )

                g = GitLab(
                    repository="https://github.com/PrefectHQ/prefect.git",
                )
                await g.get_directory(local_path=tmp_dst, from_path=sub_dir_name)

                assert set(os.listdir(tmp_dst)) == set([sub_dir_name])
                assert set(os.listdir(Path(tmp_dst) / sub_dir_name)) == child_contents
