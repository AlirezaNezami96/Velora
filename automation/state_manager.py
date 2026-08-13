"""
State manager — persists agent state between executions in automation/state.json.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config import AgentConfig

logger = logging.getLogger(__name__)


class StateManager:
    def __init__(self, config: AgentConfig) -> None:
        self.path = Path(config.repo_path) / config.state_path
        self.state: dict[str, Any] = self._load()

    def _load(self) -> dict[str, Any]:
        if self.path.exists():
            with open(self.path) as f:
                return json.load(f)
        return {
            "execution_count": 0,
            "current_phase": "Phase 1 — Foundation",
            "current_task": None,
            "completed_tasks": [],
            "failed_tasks": [],
            "total_commits": 0,
            "last_execution": None,
            "next_recommended_task": None,
            "technical_debt": [],
        }

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(self.state, f, indent=2, default=str)
        logger.info("State saved to %s", self.path)

    def record_execution_start(self, task: str) -> None:
        self.state["execution_count"] = self.state.get("execution_count", 0) + 1
        self.state["current_task"] = task
        self.state["last_execution"] = datetime.now(timezone.utc).isoformat()
        self.save()

    def record_execution_end(
        self,
        commits_made: int,
        next_task: str,
        debt: list[str],
        completed: list[str],
    ) -> None:
        self.state["total_commits"] = (
            self.state.get("total_commits", 0) + commits_made
        )
        self.state["next_recommended_task"] = next_task
        self.state["technical_debt"] = list(
            set(self.state.get("technical_debt", []) + debt)
        )
        done = self.state.get("completed_tasks", [])
        for item in completed:
            if item not in done:
                done.append(item)
        self.state["completed_tasks"] = done
        self.save()

    def get(self, key: str, default: Any = None) -> Any:
        return self.state.get(key, default)
