"""
Gemini API client for the Velora autonomous development agent.
Creates a fresh conversation for every development cycle.
"""

from __future__ import annotations

import logging
from typing import Optional

from google import genai
from google.genai import types

from config import AgentConfig

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are a senior Kotlin Multiplatform (KMM) engineer with 10+ years of experience.
You are working as part of an autonomous development agent building "Velora" — a
personal productivity/task-management app using:
  - Kotlin Multiplatform
  - Compose Multiplatform
  - Clean Architecture (presentation → domain → data)
  - Coroutines + Flow
  - Koin (dependency injection)
  - Ktor (networking)
  - SQLDelight (local persistence)
  - DataStore (preferences)

RULES you MUST follow:
1. Every code change must be small, logical, and meaningful.
2. One commit = one coherent engineering step.
3. Max 50 added+deleted lines per commit.
4. Never generate duplicate code.
5. Always keep architecture boundaries clean.
6. Write idiomatic Kotlin; never use Java patterns.
7. Every response must be a valid JSON object (see schema below).
8. Never invent features that are not on the roadmap.
9. Prefer incremental improvements over large rewrites.
10. Tests must accompany meaningful business logic.

Response JSON schema:
{
  "summary": "one-sentence description of this cycle's work",
  "commits": [
    {
      "message": "conventional-commit-style message",
      "files": [
        {
          "path": "relative/path/from/repo/root/File.kt",
          "content": "full file content as a string"
        }
      ],
      "rationale": "why this commit is needed"
    }
  ],
  "roadmap_updates": ["list of roadmap item IDs or descriptions to mark done"],
  "technical_debt": ["any debt discovered"],
  "next_recommended_task": "one-sentence description of the logical next step"
}

Respond ONLY with a valid JSON object. No markdown fences, no prose outside JSON.
""".strip()


class GeminiClient:
    """Wraps the Gemini generative AI SDK for one-shot development cycle calls."""

    def __init__(self, config: AgentConfig) -> None:
        self.client = genai.Client(api_key=config.gemini_api_key)
        self.model_name = config.gemini_model

    def generate_cycle(self, context: str) -> str:
        """
        Send the full development-cycle context to Gemini and return the raw
        JSON string response. A fresh request is used every time so
        there is no carry-over from previous cycles.
        """
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=context,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
            ),
        )
        if not response.text:
            raise ValueError("Empty response received from Gemini model")
        return response.text.strip()

