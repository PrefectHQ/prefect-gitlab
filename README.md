> [!NOTE]
> Active development of this project has moved within PrefectHQ/prefect. The code can be found [here](https://github.com/PrefectHQ/prefect/tree/main/src/integrations/prefect-gitlab) and documentation [here](https://docs.prefect.io/latest/integrations/prefect-gitlab).
> Please open issues and PRs against PrefectHQ/prefect instead of this repository.


# prefect-gitlab

<p align="center">
    <a href="https://pypi.python.org/pypi/prefect-gitlab/" alt="PyPI version">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/prefect-gitlab?color=26272B&labelColor=090422"></a>
    <a href="https://github.com/prefecthq/prefect-gitlab/" alt="Stars">
        <img src="https://img.shields.io/github/stars/prefecthq/prefect-gitlab?color=26272B&labelColor=090422" /></a>
    <a href="https://pepy.tech/badge/prefect-gitlab/" alt="Downloads">
        <img src="https://img.shields.io/pypi/dm/prefect-gitlab?color=26272B&labelColor=090422" /></a>
    <a href="https://github.com/prefecthq/prefect-gitlab/pulse" alt="Activity">
        <img src="https://img.shields.io/github/commit-activity/m/prefecthq/prefect-gitlab?color=26272B&labelColor=090422" /></a>
    <br>
    <a href="https://prefect-community.slack.com" alt="Slack">
        <img src="https://img.shields.io/badge/slack-join_community-red.svg?color=26272B&labelColor=090422&logo=slack" /></a>
</p>

## Welcome!

`prefect-gitlab` is a Prefect collection for working with GitLab repositories.

## Getting Started

### Python setup

Requires an installation of Python 3.8 or higher.

We recommend using a Python virtual environment manager such as pipenv, conda, or virtualenv.

This integration is designed to work with Prefect 2.3.0 or higher. For more information about how to use Prefect, please refer to the [Prefect documentation](https://docs.prefect.io/).

### Installation

Install `prefect-gitlab` with `pip`:

```bash
pip install prefect-gitlab
```

Then, register the [block types](https://docs.prefect.io/concepts/blocks/)) in this integration to view the storage block type on Prefect Cloud:

```bash
prefect block register -m prefect_gitlab
```

Note, to use the `load` method on a block, you must already have a block document [saved](https://docs.prefect.io/concepts/blocks/).

## Creating a GitLab storage block

### In Python

```python
from prefect_gitlab import GitLabRepository

# public GitLab repository
public_gitlab_block = GitLabRepository(
    name="my-gitlab-block",
    repository="https://gitlab.com/testing/my-repository.git"
)

public_gitlab_block.save()


# specific branch or tag of a GitLab repository
branch_gitlab_block = GitLabRepository(
    name="my-gitlab-block",
    reference="branch-or-tag-name",
    repository="https://gitlab.com/testing/my-repository.git"
)

branch_gitlab_block.save()


# Get all history of a specific branch or tag of a GitLab repository
branch_gitlab_block = GitLabRepository(
    name="my-gitlab-block",
    reference="branch-or-tag-name",
    git_depth=None,
    repository="https://gitlab.com/testing/my-repository.git"
)

branch_gitlab_block.save()

# private GitLab repository
private_gitlab_block = GitLabRepository(
    name="my-private-gitlab-block",
    repository="https://gitlab.com/testing/my-repository.git",
    access_token="YOUR_GITLAB_PERSONAL_ACCESS_TOKEN"
)

private_gitlab_block.save()
```

### In the UI
Click on the **Blocks** menu, then click the **+** button in the page header to open the block catalog:
![blocks menu](https://github.com/PrefectHQ/prefect-gitlab/blob/main/docs/img/blocks-menu.png?raw=true)

Then, find the **GitLab** block and click the **Add** button:
![GitLab block catalog entry](https://github.com/PrefectHQ/prefect-gitlab/blob/main/docs/img/gitlab-blocks.png?raw=true)


Finally, enter your repository information in the form and click **Create**:
![GitLab repository information form](https://github.com/PrefectHQ/prefect-gitlab/blob/main/docs/img/create-gitlab-repository.png?raw=true)

## Resources

If you encounter any bugs while using `prefect-gitlab`, feel free to open an issue in the [prefect-gitlab](https://github.com/prefecthq/prefect-gitlab) repository.

If you have any questions or issues while using `prefect-gitlab`, you can find help in the [Prefect Slack community](https://prefect.io/slack).

Feel free to ⭐️ or watch [`prefect-gitlab`](https://github.com/prefecthq/prefect-gitlab) for updates!

## Development

If you'd like to install a version of `prefect-gitlab` for development, clone the repository and perform an editable install with `pip`:

```bash
git clone https://github.com/prefecthq/prefect-gitlab.git

cd prefect-gitlab/

pip install -e ".[dev]"

# Install linting pre-commit hooks
pre-commit install
```
