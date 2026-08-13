"""
Task planner — assembles the Gemini context prompt for one development cycle.
"""

from __future__ import annotations

from config import AgentConfig
from roadmap_manager import RoadmapManager
from repository_manager import RepositoryManager
from git_manager import GitManager
from state_manager import StateManager


class TaskPlanner:
    def __init__(
        self,
        config: AgentConfig,
        roadmap: RoadmapManager,
        repo: RepositoryManager,
        git: GitManager,
        state: StateManager,
    ) -> None:
        self.config = config
        self.roadmap = roadmap
        self.repo = repo
        self.git = git
        self.state = state

    def build_context(self) -> str:
        execution_count = self.state.get("execution_count", 0)
        current_phase = self.state.get("current_phase", "Phase 1 — Foundation")
        next_task = self.state.get("next_recommended_task", "Set up KMM project structure")
        completed = self.state.get("completed_tasks", [])

        return f"""
# Velora Autonomous Development Cycle #{execution_count}

## Configuration
- Commits per run: {self.config.commits_per_run_min}–{self.config.commits_per_run_max}
- Max changed lines per commit: {self.config.max_changed_lines_per_commit}

## Current Roadmap Phase
{current_phase}

## Next Recommended Task
{next_task}

## Completed Tasks (so far)
{chr(10).join(f"- {t}" for t in completed) or "None yet"}

## Full Roadmap
{self.roadmap.read_roadmap()}

## Architecture
{self.roadmap.read_architecture()}

## Technical Debt
{self.roadmap.read_technical_debt()}

## Last Development Log Entry
{self.roadmap.read_last_log_entry()}

## Recent Git History
{self.git.recent_log(20)}

## Repository File Tree
{self.repo.file_tree()}

## Current Source Code
{self.repo.read_source_context()}

---
Based on all the above context, determine the SMALLEST meaningful set of
{self.config.commits_per_run_min}–{self.config.commits_per_run_max} commits that advance
the roadmap. Each commit must change at most {self.config.max_changed_lines_per_commit} lines.
Respond with valid JSON only (no markdown fences).
""".strip()
