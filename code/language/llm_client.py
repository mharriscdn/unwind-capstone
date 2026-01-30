"""
V1: no external LLM required to validate behavior under scenarios.
This stub exists to preserve architecture shape for v2.
"""

from dataclasses import dataclass


@dataclass
class LLMResult:
    text: str


class LLMClient:
    def generate(self, prompt: str) -> LLMResult:
        return LLMResult(text=prompt)