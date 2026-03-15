from __future__ import annotations

from github import Github
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from ..config import GitHubConfig


class GitHubReadInput(BaseModel):
    path: str = Field(..., description="File path in the configured repository")
    ref: str = Field(default="main", description="Git ref/branch/tag")


class GitHubWriteInput(BaseModel):
    path: str = Field(..., description="File path in the configured repository")
    content: str = Field(..., description="New file content")
    commit_message: str = Field(..., description="Commit message")
    branch: str = Field(default="main", description="Target branch")


class GitHubReadTool(BaseTool):
    name: str = "github_read_file"
    description: str = "Read file content from GitHub repository."
    args_schema: type[BaseModel] = GitHubReadInput
    config: GitHubConfig

    def _run(self, path: str, ref: str = "main") -> str:
        repo = self._repo()
        file = repo.get_contents(path, ref=ref)
        return file.decoded_content.decode("utf-8")

    def _repo(self):
        if not self.config.github_token or not self.config.github_repo:
            raise ValueError("Set GITHUB_TOKEN and GITHUB_REPO to use GitHub tools.")
        client = Github(self.config.github_token)
        return client.get_repo(self.config.github_repo)


class GitHubWriteTool(BaseTool):
    name: str = "github_write_file"
    description: str = "Create/update files in GitHub repository."
    args_schema: type[BaseModel] = GitHubWriteInput
    config: GitHubConfig

    def _run(self, path: str, content: str, commit_message: str, branch: str = "main") -> str:
        repo = self._repo()

        try:
            existing = repo.get_contents(path, ref=branch)
            repo.update_file(
                path=path,
                message=commit_message,
                content=content,
                sha=existing.sha,
                branch=branch,
            )
            return f"Updated {path} on branch {branch}."
        except Exception:
            repo.create_file(path=path, message=commit_message, content=content, branch=branch)
            return f"Created {path} on branch {branch}."

    def _repo(self):
        if not self.config.github_token or not self.config.github_repo:
            raise ValueError("Set GITHUB_TOKEN and GITHUB_REPO to use GitHub tools.")
        client = Github(self.config.github_token)
        return client.get_repo(self.config.github_repo)
