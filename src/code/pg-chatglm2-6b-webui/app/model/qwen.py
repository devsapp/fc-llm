"""Qwen"""
# pylint: disable=no-member
from app.model.llm import BaseLLM, format_messages_glm


class Qwen(BaseLLM):
    """Qwen"""

    def stream_chat(self, messages, **kwargs):
        """stream chat"""
        prompt, history = format_messages_glm(messages)
        last_len = 0
        if 'max_length' in kwargs:
            kwargs['max_new_tokens'] = kwargs.pop('max_length')
        for resp in self.model.chat_stream(
                self.tokenizer, query=prompt, history=history, **kwargs):
            yield resp[last_len:]
            last_len = len(resp)

    def chat(self, messages, **kwargs):
        """chat"""
        prompt, history = format_messages_glm(messages)
        resp, _ = self.model.chat(self.tokenizer, query=prompt, history=history, **kwargs)
        return resp
