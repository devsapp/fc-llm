"""Base class for LLM models."""
# pylint: disable=import-outside-toplevel
from abc import abstractmethod
from typing import List, Tuple, Generator
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
from app import config
from app.schema import ChatCompletionMessage

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
DEFAULT_SYSTEM_PROMPT = """\
You are a helpful, respectful and honest assistant. 
Always answer as helpfully as possible, while being safe. 
Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. 
Please ensure that your responses are socially unbiased and positive in nature.
If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. 
If you don't know the answer to a question, please don't share false information.
"""


def load_model():
    """Module providingFunction printing python version."""
    model_args = {
        "model_name_or_path": config.MODEL_PATH,
    }
    if config.LLM_MODEL.startswith("qwen"):
        from app.model.qwen import Qwen
        return Qwen(**model_args)
    if config.LLM_MODEL.startswith("internlm"):
        from app.model.internlm import InternLM
        return InternLM(**model_args)
    if config.LLM_MODEL.startswith("llama"):
        from app.model.llama import Llama
        return Llama(**model_args)
    if config.LLM_MODEL.startswith("chatglm"):
        from app.model.chatglm import ChatGLM
        return ChatGLM(**model_args)


def format_messages_glm(messages: List[ChatCompletionMessage]) -> Tuple[str,
                                                                        List[Tuple[str, str]]]:
    """Format messages for GLM models."""
    if messages[0].role == 'system':
        system_message = messages[0].content
        messages = messages[1:]
        messages[0].content = f"{B_SYS}{system_message}{E_SYS}{messages[0].content}"
    history = []
    for i in range(0, len(messages)-1, 2):
        history.append((messages[i].content, messages[i+1].content))
    return messages[-1].content, history


def format_messages_llama(messages: List[ChatCompletionMessage]) -> str:
    """Format messages for Llama."""
    prompt = ""
    if messages[0].role == 'system':
        system_message = messages[0].content
        messages = messages[1:]
        prompt = f"{B_SYS}{system_message}{E_SYS}"
    else:
        prompt = f"{B_SYS}{DEFAULT_SYSTEM_PROMPT}{E_SYS}"
    for i in range(0, len(messages)-1, 2):
        prompt += f"{B_INST} {(messages[i].content)} {E_INST} {messages[i+1].content} "
    prompt += f"{B_INST} {(messages[-1].content)} {E_INST}"
    return prompt


class BaseLLM:
    """Base class for LLM models."""

    def __init__(self, model_name_or_path: str, tokenizer: AutoTokenizer = None,
                 model: AutoModelForCausalLM = None, generation_config: GenerationConfig = None):
        self.model_name_or_path = model_name_or_path
        self.tokenizer = tokenizer if tokenizer else AutoTokenizer.from_pretrained(
            model_name_or_path, trust_remote_code=True)
        self.model = model if model else AutoModelForCausalLM.from_pretrained(
            model_name_or_path, device_map="auto", trust_remote_code=True)
        self.generation_config = generation_config if generation_config else GenerationConfig.from_pretrained(
            model_name_or_path, trust_remote_code=True)
        self.model.generation_config = self.generation_config
        self.model.eval()

    @abstractmethod
    def stream_chat(self, messages: List[ChatCompletionMessage],
                    **kwargs) -> Generator[str, None, None]:
        """stream chat"""

    @abstractmethod
    def chat(self, messages: List[ChatCompletionMessage], **kwargs) -> str:
        """chat"""
