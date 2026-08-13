"""
Roadmap manager — reads and updates ROADMAP.md and DEVELOPMENT_LOG.md.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from config import AgentConfig

logger = logging.getLogger(__name__)


class RoadmapManager:
    def __init__(self, config: AgentConfig) -> None:
        self.repo = Path(config.repo_path)
        self.roadmap_path = self.repo / config.roadmap_path
        self.architecture_path = self.repo / config.architecture_path
        self.debt_path = self.repo / config.technical_debt_path
        self.log_path = self.repo / config.development_log_path

    def read_roadmap(self) -> str:
        if self.roadmap_path.exists():
            return self.roadmap_path.read_text()
        return "(No ROADMAP.md found)"

    def read_architecture(self) -> str:
        if self.architecture_path.exists():
            return self.architecture_path.read_text()
        return "(No ARCHITECTURE.md found)"

    def read_technical_debt(self) -> str:
        if self.debt_path.exists():
            return self.debt_path.read_text()
        return "(No TECHNICAL_DEBT.md found)"

    def read_last_log_entry(self) -> str:
        """Return the last development log entry (last 50 lines) for context."""
        if not self.log_path.exists():
            return "(No DEVELOPMENT_LOG.md found)"
        lines = self.log_path.read_text().splitlines()
        return "\n".join(lines[-50:]) if len(lines) > 50 else "\n".join(lines)

    def append_log_entry(
        self,
        execution_number: int,
        phase: str,
        objective: str,
        commits: int,
        files_changed: list[str],
        debt_discovered: list[str],
        next_task: str,
        problems: Optional[str] = None,
    ) -> None:
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        entry_lines = [
            f"## Entry #{execution_number} — {now}",
            f"**Phase:** {phase}",
            f"**Objective:** {objective}",
            f"**Commits created:** {commits}",
            f"**Files changed:** {', '.join(files_changed) if files_changed else 'none'}",
        ]
        if debt_discovered:
            entry_lines.append(
                f"**Technical debt discovered:** {'; '.join(debt_discovered)}"
            )
        if problems:
            entry_lines.append(f"**Problems:** {problems}")
        entry_lines.append(f"**Next recommended task:** {next_task}")
        entry_lines.append("")

        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_path.exists():
            self.log_path.write_text("# Velora Development Log\n\n")
        with open(self.log_path, "a") as f:
            f.write("\n" + "\n".join(entry_lines))
        logger.info("Development log updated.")

    def append_technical_debt(self, items: list[str]) -> None:
        if not items:
            return
        self.debt_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.debt_path.exists():
            self.debt_path.write_text("# Technical Debt\n\n")
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        with open(self.debt_path, "a") as f:
            for item in items:
                f.write(f"- [{now}] {item}\n")
        logger.info("Technical debt file updated.")
