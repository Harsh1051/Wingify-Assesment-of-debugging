"""
agents.py

Provides a small Agent wrapper that will integrate with CrewAI if available.
For the debug/assignment purposes this file intentionally provides a safe fallback
so the repository is runnable without external API credentials.
"""
import os
from typing import Any, Optional

class Agent:
    def __init__(self, llm: Optional[Any] = None):
        # If a real LLM is passed (e.g., from CrewAI), store it. Otherwise operate locally.
        self.llm = llm

    def analyze_text(self, text: str) -> dict:
        # Use local heuristic analysis if no llm is available.
        from tools import FinancialDocumentTool
        tool = FinancialDocumentTool(llm=self.llm)
        return tool.analyze(text)
