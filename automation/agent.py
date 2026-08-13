"""
Velora Autonomous Development Agent — main orchestrator.

Usage:
    python automation/agent.py

Environment variables required:
    GEMINI_API_KEY
    GITHUB_TOKEN
    GITHUB_REPOSITORY  (optional, default: AlirezaNezami96/Velora)
    GITHUB_USER_NAME   (optional)
    GITHUB_USER_EMAIL  (optional)
    REPO_PATH          (optional, default: .)
"""

from __future__ import annotations

import logging
import os
import sys
from datetime import datetime, timezone

# Make sure the automation/ directory is importable
sys.path.insert(0, os.path.dirname(__file__))

from config import AgentConfig
from gemini_client import GeminiClient
from git_manager import GitManager
from repository_manager import RepositoryManager
from roadmap_manager import RoadmapManager
from state_manager import StateManager
from task_planner import TaskPlanner
from code_executor import CodeExecutor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("velora.agent")


def run_cycle() -> None:
    logger.info("=" * 60)
    logger.info("Velora Autonomous Development Agent — starting cycle")
    logger.info("=" * 60)

    # ---------------------------------------------------------------- bootstrap
    config = AgentConfig.from_env()
    git = GitManager(config)
    git.configure_identity()

    repo = RepositoryManager(config)
    roadmap = RoadmapManager(config)
    state = StateManager(config)
    planner = TaskPlanner(config, roadmap, repo, git, state)
    gemini = GeminiClient(config)
    executor = CodeExecutor(config, repo, git)

    # ---------------------------------------------------------------- plan
    execution_number = state.get("execution_count", 0) + 1
    current_phase = state.get("current_phase", "Phase 1 — Foundation")
    next_task = state.get(
        "next_recommended_task",
        "Inspect repository and begin Phase 1 foundation work",
    )

    logger.info("Cycle #%d | Phase: %s", execution_number, current_phase)
    logger.info("Planned task: %s", next_task)

    state.record_execution_start(next_task)

    # ---------------------------------------------------------------- generate
    context = planner.build_context()
    logger.info("Sending context to Gemini (%d chars)...", len(context))

    try:
        raw_response = gemini.generate_cycle(context)
    except Exception as exc:
        logger.error("Gemini request failed: %s", exc)
        state.record_execution_end(0, next_task, [str(exc)], [])
        sys.exit(1)

    # ---------------------------------------------------------------- execute
    result = executor.execute(raw_response)

    # ---------------------------------------------------------------- logging
    roadmap.append_log_entry(
        execution_number=execution_number,
        phase=current_phase,
        objective=next_task,
        commits=result["commits_made"],
        files_changed=result["files_changed"],
        debt_discovered=result["technical_debt"],
        next_task=result["next_recommended_task"],
        problems="; ".join(result["errors"]) if result["errors"] else None,
    )

    if result["technical_debt"]:
        roadmap.append_technical_debt(result["technical_debt"])

    # Commit documentation updates if changed
    if git.has_uncommitted_changes():
        git.stage_all()
        git.commit("docs: update development log and technical debt")

    state.record_execution_end(
        commits_made=result["commits_made"],
        next_task=result["next_recommended_task"],
        debt=result["technical_debt"],
        completed=result["roadmap_updates"],
    )

    # ---------------------------------------------------------------- push
    logger.info("Pushing %d commits to GitHub...", result["commits_made"])
    try:
        git.push()
    except Exception as exc:
        logger.error("Push failed: %s", exc)
        sys.exit(1)

    logger.info(
        "Cycle #%d complete. %d commits pushed.",
        execution_number,
        result["commits_made"],
    )


if __name__ == "__main__":
    run_cycle()
