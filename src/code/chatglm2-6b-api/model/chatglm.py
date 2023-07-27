"""ChatGLM"""
from typing import List
from .llm import BaseLLM


def format_history(history: List[str]):
    """Module providingFunction printing python version."""
    if not history or len(history) % 2 == 1:
        return []
    return [(history[i], history[i+1]) for i in range(0, len(history), 2)]


class ChatGLM(BaseLLM):
    """ChatGLM"""

    def stream_chat(self, prompt: str, history: List[str] = None):
        """stream chat"""
        for resp, _ in self.model.stream_chat(
                self.tokenizer,
                prompt,
                history=format_history(history),
                max_length=self.max_token,
                temperature=self.temperature,
                top_p=self.top_p,
        ):
            yield resp

    def chat(self, prompt: str, history: List[str] = None):
        """chat"""
        resp, _ = self.model.chat(
            self.tokenizer,
            prompt,
            history=format_history(history),
            max_length=self.max_token,
            temperature=self.temperature,
            top_p=self.top_p,
        )
        return resp
