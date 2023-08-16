"""InternLM"""
# pylint: disable=no-member
from threading import Thread
import torch
from transformers import AutoTokenizer, AutoModel, TextIteratorStreamer
from app.model.llm import BaseLLM, format_messages_glm


class InternLMStreamer(TextIteratorStreamer):
    """Streamer"""

    def __init__(
            self, tokenizer: "AutoTokenizer", skip_prompt: bool = False, timeout: float = None, **
            decode_kwargs):
        super().__init__(tokenizer, skip_prompt, timeout, **decode_kwargs)
        self.stop_signal = '<eoa>'
        self.skip_header = True

    def put(self, value):
        """
        Receives tokens, decodes them, and prints them to stdout as soon as they form entire words.
        """
        if len(value.shape) > 1 and value.shape[0] > 1:
            raise ValueError("TextStreamer only supports batch size 1")
        elif len(value.shape) > 1:
            value = value[0]
        text = self.tokenizer.decode([value[-1]], **self.decode_kwargs)
        if self.skip_header and text == ">:":
            self.skip_header = False
            return
        self.on_finalized_text(text)


class InternLM(BaseLLM):
    """InternLM"""

    def __init__(self, model_name_or_path: str, **kwargs):
        model = AutoModel.from_pretrained(
            model_name_or_path, torch_dtype=torch.float16, device_map="auto",
            trust_remote_code=True)
        super().__init__(model_name_or_path, model=model, **kwargs)

    def stream_chat(self, messages, **kwargs):
        """stream chat"""
        prompt, history = format_messages_glm(messages)
        inputs = self.model.build_inputs(self.tokenizer, prompt, history)
        inputs = {k: v.to(self.model.device) for k, v in inputs.items() if torch.is_tensor(v)}
        streamer = InternLMStreamer(self.tokenizer, skip_special_tokens=True)
        thread = Thread(target=self.model.generate, kwargs={
                        **inputs, "streamer": streamer, **kwargs})
        thread.start()
        return streamer

    def chat(self, messages, **kwargs):
        """chat"""
        prompt, history = format_messages_glm(messages)
        inputs = self.model.build_inputs(self.tokenizer, prompt, history)
        inputs = {k: v.to(self.model.device) for k, v in inputs.items() if torch.is_tensor(v)}
        outputs = self.model.generate(**inputs, **kwargs)
        outputs = outputs[0].cpu().tolist()[len(inputs["input_ids"][0]):]
        resp = self.tokenizer.decode(outputs, skip_special_tokens=True)
        resp = resp.split("<eoa>")[0]
        return resp
