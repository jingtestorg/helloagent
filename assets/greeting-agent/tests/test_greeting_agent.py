"""Tests for the greeting agent."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Ensure app/ is on path
APP_PATH = str(Path(__file__).parent.parent / "app")
if APP_PATH not in sys.path:
    sys.path.insert(0, APP_PATH)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _mock_llm_response(text: str):
    """Build a mock ChatLiteLLM that returns a canned LangGraph-compatible result."""
    msg = MagicMock()
    msg.content = text
    result = {"messages": [msg]}

    # Mock the graph.ainvoke
    mock_graph = MagicMock()
    mock_graph.ainvoke = AsyncMock(return_value=result)
    return mock_graph


# ---------------------------------------------------------------------------
# Unit tests
# ---------------------------------------------------------------------------


class TestGreetingWithName:
    """A message containing a name returns a greeting with that name."""

    @pytest.mark.asyncio
    async def test_greeting_with_name(self, add_agent_to_path):
        from sap_cloud_sdk.aicore import set_aicore_config
        set_aicore_config()

        from agent import SampleAgent

        agent = SampleAgent()
        expected_response = "Hello, Alice! Welcome!"

        with patch.object(agent, "_invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
            msg = MagicMock()
            msg.content = expected_response
            mock_invoke.return_value = {"messages": [msg]}

            response = await agent._run_greeting("Hello, my name is Alice!", "ctx-001", [])

        assert "Alice" in response
        mock_invoke.assert_called_once()


class TestGreetingWithoutName:
    """A message without a name returns a friendly generic greeting."""

    @pytest.mark.asyncio
    async def test_greeting_without_name(self, add_agent_to_path):
        from sap_cloud_sdk.aicore import set_aicore_config
        set_aicore_config()

        from agent import SampleAgent

        agent = SampleAgent()
        expected_response = "Hello there! Welcome! How can I help you today?"

        with patch.object(agent, "_invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
            msg = MagicMock()
            msg.content = expected_response
            mock_invoke.return_value = {"messages": [msg]}

            response = await agent._run_greeting("Hi!", "ctx-002", [])

        assert len(response) > 0
        mock_invoke.assert_called_once()


class TestInvokeEndToEnd:
    """Integration test: invoke() with mocked LLM returns AgentResponse."""

    @pytest.mark.asyncio
    async def test_invoke_returns_completed_response(self, add_agent_to_path):
        from sap_cloud_sdk.aicore import set_aicore_config
        set_aicore_config()

        from agent import SampleAgent

        agent = SampleAgent()
        greeting_text = "Hello, Bob! Great to have you here!"

        with patch.object(agent, "_invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
            msg = MagicMock()
            msg.content = greeting_text
            mock_invoke.return_value = {"messages": [msg]}

            result = await agent.invoke("Hi, I'm Bob", "ctx-003", tools=[])

        assert result.status == "completed"
        assert result.message == greeting_text

    @pytest.mark.asyncio
    async def test_invoke_handles_error_gracefully(self, add_agent_to_path):
        from sap_cloud_sdk.aicore import set_aicore_config
        set_aicore_config()

        from agent import SampleAgent

        agent = SampleAgent()

        with patch.object(agent, "_invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.side_effect = Exception("LLM unavailable")

            result = await agent.invoke("Hello!", "ctx-004", tools=[])

        # The stream() method catches exceptions and returns completed with error message
        assert result.status == "completed"
        assert "error" in result.message.lower()


class TestSystemPrompt:
    """System prompt contains greeting-specific instructions."""

    def test_system_prompt_contains_greeting_instructions(self, add_agent_to_path):
        from sap_cloud_sdk.aicore import set_aicore_config
        set_aicore_config()

        from agent import get_system_prompt

        prompt = get_system_prompt()
        assert "greet" in prompt.lower()
        assert "name" in prompt.lower()

    def test_system_prompt_no_mcp_instruction(self, add_agent_to_path):
        from sap_cloud_sdk.aicore import set_aicore_config
        set_aicore_config()

        from agent import get_system_prompt

        prompt = get_system_prompt()
        # Should not instruct to use MCP tools for external data
        assert "DPQuery" not in prompt
        assert "ordids" not in prompt


class TestMilestoneInstrumentation:
    """M1 is logged on agent initialization."""

    def test_m1_logged_on_init(self, add_agent_to_path, caplog):
        import logging
        from sap_cloud_sdk.aicore import set_aicore_config
        set_aicore_config()

        from agent import SampleAgent

        with caplog.at_level(logging.INFO, logger="agent"):
            agent = SampleAgent()

        assert any("M1.achieved" in r.message for r in caplog.records)

    @pytest.mark.asyncio
    async def test_m2_missed_logged_on_error(self, add_agent_to_path, caplog):
        import logging
        from sap_cloud_sdk.aicore import set_aicore_config
        set_aicore_config()
        from agent import SampleAgent

        agent = SampleAgent()

        with patch.object(agent, "_invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.side_effect = Exception("boom")
            with caplog.at_level(logging.WARNING, logger="agent"):
                result = await agent.invoke("Hi!", "ctx-m2", tools=[])

        assert any("M2.missed" in r.message for r in caplog.records)

    @pytest.mark.asyncio
    async def test_m2_achieved_logged_on_success(self, add_agent_to_path, caplog):
        import logging
        from sap_cloud_sdk.aicore import set_aicore_config
        set_aicore_config()
        from agent import SampleAgent

        agent = SampleAgent()

        with patch.object(agent, "_invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
            msg = MagicMock()
            msg.content = "Hello, there!"
            mock_invoke.return_value = {"messages": [msg]}
            with caplog.at_level(logging.INFO, logger="agent"):
                await agent._run_greeting("Hi!", "ctx-m2-ok", [])

        assert any("M2.achieved" in r.message for r in caplog.records)


class TestStreamMethod:
    """Tests for the stream async generator."""

    @pytest.mark.asyncio
    async def test_stream_yields_processing_then_result(self, add_agent_to_path):
        from sap_cloud_sdk.aicore import set_aicore_config
        set_aicore_config()
        from agent import SampleAgent

        agent = SampleAgent()

        with patch.object(agent, "_invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
            msg = MagicMock()
            msg.content = "Welcome!"
            mock_invoke.return_value = {"messages": [msg]}

            chunks = []
            async for chunk in agent.stream("Hello!", "ctx-stream-1", tools=[]):
                chunks.append(chunk)

        assert len(chunks) >= 1
        last = chunks[-1]
        assert last["is_task_complete"] is True
        assert last["content"] == "Welcome!"

    @pytest.mark.asyncio
    async def test_stream_yields_error_on_failure(self, add_agent_to_path):
        from sap_cloud_sdk.aicore import set_aicore_config
        set_aicore_config()
        from agent import SampleAgent

        agent = SampleAgent()

        with patch.object(agent, "_invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.side_effect = RuntimeError("fail")

            chunks = []
            async for chunk in agent.stream("Hello!", "ctx-stream-err", tools=[]):
                chunks.append(chunk)

        last = chunks[-1]
        assert last["is_task_complete"] is True
        assert "error" in last["content"].lower()


class TestAgentConfiguration:
    """Agent configuration decorators return expected defaults."""

    def test_model_name_default(self, add_agent_to_path):
        from sap_cloud_sdk.aicore import set_aicore_config
        set_aicore_config()
        from agent import get_model_name
        assert "claude" in get_model_name()

    def test_temperature_default(self, add_agent_to_path):
        from sap_cloud_sdk.aicore import set_aicore_config
        set_aicore_config()
        from agent import get_temperature
        assert get_temperature() == 0.0

    def test_fallback_models_default_empty(self, add_agent_to_path):
        from sap_cloud_sdk.aicore import set_aicore_config
        set_aicore_config()
        from agent import get_fallback_model_names
        assert get_fallback_model_names() == ""
