from __future__ import annotations

from git import InvalidGitRepositoryError, NoSuchPathError, Repo
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import get_plugin_logger
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

from shadcn.plugins.mixins.base import Mixin

REPO_CONFIG_KEY = "git_repository"
CREATED_AT_META_KEY = "created_at"
UPDATED_AT_META_KEY = "updated_at"


logger = get_plugin_logger("mixins/git")


def find_repo(abs_src_file: str) -> Repo | None:
    """
    Find the git repository for the given source file.
    Returns None if no repository is found.
    """
    try:
        return Repo(abs_src_file, search_parent_directories=True)
    except (InvalidGitRepositoryError, NoSuchPathError):
        print(f"Could not find git repository starting from {abs_src_file}")
        return None


class GitTimestampsMixin(Mixin):
    has_commits = False

    def on_config(self, config: MkDocsConfig):
        """Called when the config is loaded.

        Attributes:
            config (dict): The MkDocs configuration dictionary.

        """
        repo = find_repo(config.config_file_path)
        config[REPO_CONFIG_KEY] = repo
        logger.info("Git mixin activated.")
        logger.debug(f"Git repository: {config[REPO_CONFIG_KEY]}")

        self.has_commits = repo is not None and repo.head.is_valid()
        if not self.has_commits:
            logger.warning("No git commit found.")
        return super().on_config(config)

    def on_page_markdown(
        self,
        markdown: str,
        /,
        *,
        page: Page,
        config: MkDocsConfig,
        files: Files,
    ):
        if self.has_commits:
            repo = config.get(REPO_CONFIG_KEY, None)
            if isinstance(repo, Repo) and page.file.abs_src_path:
                dates = [
                    commit.committed_datetime
                    for commit in repo.iter_commits(paths=page.file.abs_src_path)
                ]
                if len(dates) > 0:
                    page.meta[CREATED_AT_META_KEY] = dates[-1]
                    page.meta[UPDATED_AT_META_KEY] = dates[0]

        return super().on_page_markdown(markdown, page=page, config=config, files=files)
