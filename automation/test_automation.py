"""
Unit tests for the Velora automation agent components.
"""

import os
import unittest
from unittest.mock import MagicMock, patch

from config import AgentConfig
from gemini_client import GeminiClient, SYSTEM_PROMPT
from code_executor import _extract_json


class TestAgentConfig(unittest.TestCase):
    @patch.dict(os.environ, {"GEMINI_API_KEY": "test_key", "GITHUB_TOKEN": "test_token"}, clear=True)
    def test_default_model(self):
        config = AgentConfig.from_env()
        self.assertEqual(config.gemini_model, "gemini-2.5-flash")
        self.assertEqual(config.gemini_api_key, "test_key")

    @patch.dict(os.environ, {
        "GEMINI_API_KEY": "test_key",
        "GITHUB_TOKEN": "test_token",
        "GEMINI_MODEL": "gemini-2.5-flash"
    }, clear=True)
    def test_custom_model(self):
        config = AgentConfig.from_env()
        self.assertEqual(config.gemini_model, "gemini-2.5-flash")


class TestGeminiClient(unittest.TestCase):
    @patch("gemini_client.genai.Client")
    def test_generate_cycle(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client
        mock_response = MagicMock()
        mock_response.text = '{"summary": "test", "commits": []}'
        mock_client.models.generate_content.return_value = mock_response

        config = AgentConfig(
            gemini_api_key="fake-key",
            github_token="fake-token",
            gemini_model="gemini-2.5-flash",
        )
        client = GeminiClient(config)
        result = client.generate_cycle("context prompt")

        self.assertEqual(result, '{"summary": "test", "commits": []}')
        mock_client_cls.assert_called_once_with(api_key="fake-key")
        mock_client.models.generate_content.assert_called_once()
        _, kwargs = mock_client.models.generate_content.call_args
        self.assertEqual(kwargs["model"], "gemini-2.5-flash")
        self.assertIn("context prompt", kwargs["contents"])
        self.assertEqual(kwargs["config"].response_mime_type, "application/json")


class TestExtractJson(unittest.TestCase):
    def test_plain_json(self):
        raw = '{"key": "value"}'
        self.assertEqual(_extract_json(raw), raw)

    def test_fenced_json(self):
        raw = '```json\n{"key": "value"}\n```'
        self.assertEqual(_extract_json(raw), '{"key": "value"}')


if __name__ == "__main__":
    unittest.main()
