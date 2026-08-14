"""
Velora KMM Autonomous Development Agent
Configuration module — reads all settings from environment variables.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass
class AgentConfig:
    # Gemini
    gemini_api_key: str = field(default_factory=lambda: os.environ["GEMINI_API_KEY"])
    gemini_model: str = field(
        default_factory=lambda: os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
    )

    # GitHub
    github_token: str = field(default_factory=lambda: os.environ["GITHUB_TOKEN"])
    github_repository: str = field(
        default_factory=lambda: os.getenv(
            "GITHUB_REPOSITORY", "AlirezaNezami96/Velora"
        )
    )
    github_user_name: str = field(
        default_factory=lambda: os.getenv("GITHUB_USER_NAME", "AlirezaNezami96")
    )
    github_user_email: str = field(
        default_factory=lambda: os.getenv(
            "GITHUB_USER_EMAIL",
            "AlirezaNezami96@users.noreply.github.com",
        )
    )

    # Agent behaviour
    commits_per_run_min: int = field(
        default_factory=lambda: int(os.getenv("COMMITS_PER_RUN_MIN", "10"))
    )
    commits_per_run_max: int = field(
        default_factory=lambda: int(os.getenv("COMMITS_PER_RUN_MAX", "15"))
    )
    max_changed_lines_per_commit: int = field(
        default_factory=lambda: int(os.getenv("MAX_CHANGED_LINES_PER_COMMIT", "50"))
    )
    timezone: str = field(
        default_factory=lambda: os.getenv("TIMEZONE", "UTC")
    )

    # Paths (relative to repo root)
    repo_path: str = field(
        default_factory=lambda: os.getenv("REPO_PATH", ".")
    )
    state_path: str = "automation/state.json"
    roadmap_path: str = "ROADMAP.md"
    architecture_path: str = "ARCHITECTURE.md"
    technical_debt_path: str = "TECHNICAL_DEBT.md"
    development_log_path: str = "DEVELOPMENT_LOG.md"

    @classmethod
    def from_env(cls) -> "AgentConfig":
        return cls()
