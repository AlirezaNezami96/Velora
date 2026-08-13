"""
Code executor — writes files returned by Gemini and orchestrates commits.
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

from config import AgentConfig
from git_manager import GitManager
from repository_manager import RepositoryManager

logger = logging.getLogger(__name__)


def _extract_json(text: str) -> str:
    """Strip markdown code fences if Gemini wraps the JSON anyway."""
    text = text.strip()
    # Remove ```json ... ``` or ``` ... ```
    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if match:
        return match.group(1).strip()
    return text


class CodeExecutor:
    def __init__(
        self,
        config: AgentConfig,
        repo: RepositoryManager,
        git: GitManager,
    ) -> None:
        self.config = config
        self.repo = repo
        self.git = git

    def execute(self, raw_response: str) -> dict[str, Any]:
        """
        Parse Gemini's JSON response, write files, and commit each change.
        Returns a result dict with metadata about the execution.
        """
        result: dict[str, Any] = {
            "commits_made": 0,
            "files_changed": [],
            "roadmap_updates": [],
            "technical_debt": [],
            "next_recommended_task": "",
            "errors": [],
        }

        try:
            data = json.loads(_extract_json(raw_response))
        except json.JSONDecodeError as exc:
            logger.error("Failed to parse Gemini response as JSON: %s", exc)
            result["errors"].append(f"JSON parse error: {exc}")
            return result

        result["roadmap_updates"] = data.get("roadmap_updates", [])
        result["technical_debt"] = data.get("technical_debt", [])
        result["next_recommended_task"] = data.get("next_recommended_task", "")

        commits: list[dict] = data.get("commits", [])
        for commit in commits:
            message = commit.get("message", "")
            files = commit.get("files", [])
            if not message or not files:
                logger.warning("Skipping malformed commit entry.")
                continue

            # Write all files for this commit
            written_paths: list[str] = []
            for file_spec in files:
                path = file_spec.get("path", "")
                content = file_spec.get("content", "")
                if not path or content is None:
                    continue
                self.repo.write_file(path, content)
                self.git.stage_file(path)
                written_paths.append(path)

            # Validate diff size and commit
            total_diff = self.git.total_diff_lines()
            if total_diff == 0:
                logger.info("No changes staged for: %s — skipping.", message)
                continue
            if total_diff > self.config.max_changed_lines_per_commit:
                logger.warning(
                    "Diff too large (%d lines) for '%s'. Skipping commit.",
                    total_diff,
                    message,
                )
                result["errors"].append(
                    f"Oversized diff ({total_diff} lines) for: {message}"
                )
                # Unstage to avoid partial commits
                self.git._run("reset", "HEAD")
                continue

            success = self.git.commit(message)
            if success:
                result["commits_made"] += 1
                result["files_changed"].extend(written_paths)

        logger.info("Execution complete: %d commits made.", result["commits_made"])
        return result
