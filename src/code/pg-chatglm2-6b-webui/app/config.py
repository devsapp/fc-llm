"""Config file for the app."""
import os

MODEL_DIR = "/mnt/auto/llm"

LLM_MODEL_DICT = {
    "chatglm-6b-int8": f"{MODEL_DIR}/chatglm-6b-int8",
    "chatglm-6b": f"{MODEL_DIR}/local-chatglm-model",
    "chatglm2-6b": f"{MODEL_DIR}/chatglm2-6b",
    "chatglm2-6b-int4": f"{MODEL_DIR}/chatglm2-6b-int4",
    "internlm-chat-7b": f"{MODEL_DIR}/internlm-chat-7b",
    "llama-2-7b-chat": f"{MODEL_DIR}/Llama-2-7b-chat-hf",
    "codegeex2-6b": f"{MODEL_DIR}/codegeex2-6b", "qwen-7b-chat": f"{MODEL_DIR}/qwen-7b-chat"}

PORT = 7860
LLM_MODEL = os.environ.get("LLM_MODEL", "chatglm2-6b-int4")
MODEL_PATH = LLM_MODEL_DICT[LLM_MODEL]
