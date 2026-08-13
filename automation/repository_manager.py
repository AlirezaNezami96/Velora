"""
Repository manager — reads source files and builds context for Gemini.
"""

from __future__ import annotations

import logging
from pathlib import Path

from config import AgentConfig

logger = logging.getLogger(__name__)

_INCLUDE_EXTENSIONS = {".kt", ".kts", ".toml", ".xml", ".json", ".yaml", ".yml", ".md"}
_SKIP_DIRS = {
    ".git", "build", ".gradle", ".idea", "node_modules",
    "__pycache__", ".kotlin", "DerivedData", "xcuserdata",
    "Pods", ".build",
}
_MAX_FILE_CHARS = 8_000
_MAX_TOTAL_CHARS = 120_000


class RepositoryManager:
    def __init__(self, config: AgentConfig) -> None:
        self.repo = Path(config.repo_path).resolve()

    def file_tree(self, max_depth: int = 5) -> str:
        """Return a compact directory tree."""
        lines: list[str] = []
        self._walk(self.repo, lines, 0, max_depth)
        return "\n".join(lines)

    def _walk(
        self, path: Path, lines: list[str], depth: int, max_depth: int
    ) -> None:
        if depth > max_depth:
            return
        for child in sorted(path.iterdir()):
            if child.name in _SKIP_DIRS:
                continue
            prefix = "  " * depth
            if child.is_dir():
                lines.append(f"{prefix}{child.name}/")
                self._walk(child, lines, depth + 1, max_depth)
            else:
                lines.append(f"{prefix}{child.name}")

    def read_source_context(self, max_chars: int = _MAX_TOTAL_CHARS) -> str:
        """Read relevant source files and return concatenated context string."""
        parts: list[str] = []
        total = 0
        for f in self._iter_source_files():
            try:
                text = f.read_text(errors="replace")
                snippet = text[:_MAX_FILE_CHARS]
                rel = f.relative_to(self.repo)
                block = f"\n### {rel}\n```\n{snippet}\n```\n"
                if total + len(block) > max_chars:
                    break
                parts.append(block)
                total += len(block)
            except Exception as exc:
                logger.warning("Could not read %s: %s", f, exc)
        return "\n".join(parts)

    def _iter_source_files(self):
        for path in sorted(self.repo.rglob("*")):
            if path.is_file() and path.suffix in _INCLUDE_EXTENSIONS:
                if not any(p in _SKIP_DIRS for p in path.parts):
                    yield path

    def write_file(self, relative_path: str, content: str) -> Path:
        """Write content to a file relative to repo root."""
        target = self.repo / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        logger.info("Wrote %s", target)
        return target
