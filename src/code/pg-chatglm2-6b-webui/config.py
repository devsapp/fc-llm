import torch.cuda
import torch.backends
import os


LLM_MODEL = os.environ.get("LLM_MODEL",  "chatglm2-6b-int4")

# supported LLM models
LLM_MODEL_DICT = {
    "chatglm-6b-int8": "/mnt/auto/chatglm/chatglm-6b-int8",
    "chatglm-6b": "/mnt/auto/chatglm/local-chatglm-model",
    "chatglm2-6b": "/mnt/auto/llm/chatglm2-6b",
    "chatglm2-6b-int4": "/mnt/auto/llm/chatglm2-6b-int4",
    "internlm-chat-7b": "/mnt/auto/chatglm/internlm-chat-7b",
    # "falcon-7b": "/mnt/auto/chatglm/falcon-7-instruct",
}

# LLM running device
LLM_DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

TEMPERATURE = 0.9
TOP_P = 0.9
MAX_TOKEN = 10000
PORT = 7860


MODEL_PATH = LLM_MODEL_DICT[LLM_MODEL]
