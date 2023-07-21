"""Base class for LLM models."""
from abc import abstractmethod
from typing import List, Generator
from transformers import AutoTokenizer, AutoModel, AutoConfig


class BaseLLM:
    """Base class for LLM models."""

    def __init__(
            self, model_name_or_path: str, max_token: int = 10000, temperature: float = 0.8, top_p=0.9,
            llm_device: str = "cuda", config: AutoConfig = None, tokenizer: AutoTokenizer = None,
            model: AutoModel = None):
        self.max_token = max_token
        self.temperature = temperature
        self.top_p = top_p
        self.config = config if config else AutoConfig.from_pretrained(
            model_name_or_path, trust_remote_code=True)
        self.tokenizer = tokenizer if tokenizer else AutoTokenizer.from_pretrained(
            model_name_or_path, trust_remote_code=True)
        self.model = model if model else AutoModel.from_pretrained(
            model_name_or_path, config=self.config, trust_remote_code=True)
        if llm_device.startswith("cuda"):
            self.model = self.model.cuda()
        else:
            self.model = self.model.to(llm_device)
        self.model.eval()

    @abstractmethod
    def stream_chat(self, prompt: str, history: List[str] = None) -> Generator[str, None, None]:
        """stream chat"""

    @abstractmethod
    def chat(self, prompt: str, history: List[str] = None) -> str:
        """chat"""
