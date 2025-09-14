import os
from pathlib import Path

import pytest

from workflow import MultiAgentWorkflow
from tools.search_tool import SearchTool
from tools.calc_tool import CalculatorTool
from tools.file_tool import FileTool


class _Resp:
    def __init__(self, content: str):
        self.content = content


class FakeLLM:
    """Minimal stub to mimic .invoke(messages)->object with .content"""

    def invoke(self, messages):
        # Return a short, deterministic response regardless of messages
        return _Resp("stubbed response")


def test_workflow_happy_path(tmp_path: Path, monkeypatch):
    # Constrain file outputs to a temp directory
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))

    # Build workflow with injected fake LLM and real tools (search uses fallback)
    llm = FakeLLM()
    tools = [SearchTool(), CalculatorTool(), FileTool()]
    wf = MultiAgentWorkflow(llm=llm, tools=tools)

    state = wf.run("Analyze Apple stock performance in 2024")

    # Basic invariants
    assert state.get("completed") is True
    assert "final_report" in state and isinstance(state["final_report"], str)
    assert state["final_report"].strip() != ""

    # Ensure a report file is written under OUTPUT_DIR
    assert state.get("save_result", "").startswith("Successfully created report:")
    files = list(tmp_path.iterdir())
    assert len(files) >= 1
    # Validate extension heuristic
    assert any(p.suffix in {".md", ".txt"} for p in files)

