"""Llama"""
# pylint: disable=no-member
from threading import Thread
from transformers import TextIteratorStreamer
from app.model.llm import BaseLLM, format_messages_llama


class Llama(BaseLLM):
    """Llama"""

    def stream_chat(self, messages, **kwargs):
        """stream chat"""
        streamer = TextIteratorStreamer(self.tokenizer, skip_special_tokens=True, skip_prompt=True)
        prompt = format_messages_llama(messages)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        thread = Thread(target=self.model.generate, kwargs={
                        "input_ids": inputs["input_ids"], "streamer": streamer, **kwargs})
        thread.start()
        return streamer

    def chat(self, messages, **kwargs):
        """chat"""
        prompt = format_messages_llama(messages)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(inputs.input_ids, **kwargs)
        resp = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
        return resp
