"""
Git operations manager for the Velora autonomous development agent.
Handles: status, history, staged changes, committing, diff validation, push.
"""

from __future__ import annotations

import logging
import os
import subprocess
from pathlib import Path
from typing import Optional

from config import AgentConfig

logger = logging.getLogger(__name__)


class GitManager:
    def __init__(self, config: AgentConfig) -> None:
        self.repo = Path(config.repo_path).resolve()
        self.user_name = config.github_user_name
        self.user_email = config.github_user_email
        self.max_lines = config.max_changed_lines_per_commit

    # ------------------------------------------------------------------ helpers

    def _run(self, *args: str, check: bool = True) -> subprocess.CompletedProcess:
        result = subprocess.run(
            ["git", *args],
            cwd=self.repo,
            capture_output=True,
            text=True,
            check=False,
        )
        if check and result.returncode != 0:
            raise RuntimeError(
                f"git {' '.join(args)} failed:\n{result.stderr}"
            )
        return result

    # ------------------------------------------------------------------ public

    def configure_identity(self) -> None:
        self._run("config", "user.name", self.user_name)
        self._run("config", "user.email", self.user_email)

    def status(self) -> str:
        return self._run("status", "--short").stdout

    def recent_log(self, n: int = 20) -> str:
        return self._run(
            "log", f"-{n}", "--oneline", "--no-decorate"
        ).stdout

    def current_branch(self) -> str:
        return self._run("branch", "--show-current").stdout.strip()

    def diff_numstat(self) -> tuple[int, int]:
        """Return (added_lines, deleted_lines) for the current staged diff."""
        out = self._run("diff", "--cached", "--numstat").stdout
        added = deleted = 0
        for line in out.splitlines():
            parts = line.split("\t")
            if len(parts) >= 2:
                try:
                    added += int(parts[0])
                    deleted += int(parts[1])
                except ValueError:
                    pass  # binary files show "-"
        return added, deleted

    def total_diff_lines(self) -> int:
        added, deleted = self.diff_numstat()
        return added + deleted

    def stage_file(self, path: str) -> None:
        self._run("add", path)

    def stage_all(self) -> None:
        self._run("add", "-A")

    def commit(self, message: str) -> bool:
        """Stage already-written files and commit. Returns False if diff > limit."""
        total = self.total_diff_lines()
        if total == 0:
            logger.warning("Nothing staged — skipping commit.")
            return False
        if total > self.max_lines:
            logger.error(
                "Diff too large: %d lines (max %d). Skipping commit.",
                total,
                self.max_lines,
            )
            return False
        self._run(
            "commit",
            "-m", message,
            "--author", f"{self.user_name} <{self.user_email}>",
        )
        logger.info("Committed: %s", message)
        return True

    def commit_file(self, path: str, message: str) -> bool:
        """Stage a single file and commit it."""
        self.stage_file(path)
        return self.commit(message)

    def push(self, branch: Optional[str] = None) -> None:
        target_branch = branch or self.current_branch() or os.getenv("GITHUB_REF_NAME") or "main"
        self._run("push", "origin", f"HEAD:{target_branch}")
        logger.info("Pushed to origin/%s", target_branch)

    def has_uncommitted_changes(self) -> bool:
        return bool(self._run("status", "--porcelain").stdout.strip())
