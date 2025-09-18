"""
Tools for analyzing financial document text.

This includes a fallback local analyzer when CrewAI (or another LLM) is not available.
The goal is to make the repository runnable for debugging and testing without external
API keys by providing deterministic, simple analysis behavior.
"""
import re
from typing import Any, Dict, List, Optional

class FinancialDocumentTool:
    def __init__(self, llm: Optional[Any] = None):
        # Accept an optional llm. If a real LLM (like CrewAI) is provided, it will be used.
        self.llm = llm

    def analyze(self, text: str, filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze the extracted text and return a structured dict including:
          - summary: short text summary
          - word_count: number of words
          - top_numbers: list of numeric figures found in the document
          - recommendation: a naive recommendation (BUY/HOLD/SELL or CAUTION)
        """
        # If CrewAI (or other) is available and attached, prefer that.
        try:
            if self.llm is not None:
                # If the user has provided a real LLM object, try to use it.
                response = self._analyze_with_llm(text)
                if response:
                    return response
        except Exception:
            # Fall back to local analyzer if llm usage fails
            pass

        # Deterministic local analysis
        return self._local_analyze(text, filename)

    def _analyze_with_llm(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Placeholder for LLM-based analysis. Integrate with CrewAI or other LLMs here.
        For the debug assignment we don't assume the environment has CrewAI configured,
        so this function is intentionally conservative and will return None if integration
        isn't set up.
        """
        try:
            # Example (non-functional) placeholder showing how an LLM might be called:
            # response = self.llm.generate(prompt=..., max_tokens=500)
            # return {"summary": response.text, ...}
            return None
        except Exception:
            return None

    def _local_analyze(self, text: str, filename: Optional[str]) -> Dict[str, Any]:
        words = re.findall(r"\w+", text)
        word_count = len(words)

        # Extract currency-like numbers (e.g., $1,234.56 or 1234.56)
        num_pattern = re.compile(r"\$?\d[\d,]*\.?\d*")
        found = num_pattern.findall(text)
        # Normalize numbers (strip $ and commas)
        numbers = []
        for n in found:
            n_clean = n.replace("$", "").replace(",", "")
            try:
                numbers.append(float(n_clean))
            except Exception:
                pass

        # Pick top 6 absolute-valued numbers (likely financial figures)
        numbers_sorted = sorted(numbers, key=lambda x: abs(x), reverse=True)[:6]

        # Simple sentiment-ish heuristic
        lower = text.lower()
        negative_markers = ["loss", "losses", "decline", "drop", "down", "cut", "risk"]
        positive_markers = ["increase", "growth", "up", "beat", "profit", "gain", "record"]
        score = 0
        for m in negative_markers:
            if m in lower:
                score -= 1
        for m in positive_markers:
            if m in lower:
                score += 1

        if score > 0:
            recommendation = "BUY (positive indicators detected)"
        elif score < 0:
            recommendation = "CAUTION (negative indicators detected)"
        else:
            recommendation = "HOLD (no clear signal)"

        summary = text.strip()[:800].replace("\n", " ")
        return {
            "filename": filename,
            "summary": summary,
            "word_count": word_count,
            "top_numbers": numbers_sorted,
            "recommendation": recommendation,
        }
