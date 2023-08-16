"""This module defines the schemas for the API."""
# pylint: disable=too-few-public-methods
from typing import List, Optional, Union
from typing_extensions import Literal, NotRequired, TypedDict
from pydantic import BaseModel, Field, validator  # pylint: disable = no-name-in-module


class ChatCompletionChunkDelta(TypedDict):
    """Delta Message for Chat Completion Stream Response"""
    role: NotRequired[Literal["assistant"]]
    content: NotRequired[str]


class ChatCompletionChunkDeltaEmpty(TypedDict):
    """Empty Delta Message for Chat Completion Stream Response"""


class ChatCompletionChunkChoice(TypedDict):
    """Choice for Chat Completion Stream Response"""
    index: int
    delta: Union[ChatCompletionChunkDelta, ChatCompletionChunkDeltaEmpty]
    finish_reason: NotRequired[str]


class ChatCompletionMessage(BaseModel):
    """A message in a chat completion request."""
    role: Literal["system", "user", "assistant"] = Field(
        default="user", description="The role of the message."
    )
    content: str = Field(default="", description="The content of the message.")


class ChatCompletionChunk(BaseModel):
    """A chunk of a chat completion stream response."""
    id: str
    model: str
    object: Literal["chat.completion.chunk"]
    created: int
    choices: List[ChatCompletionChunkChoice]


class ChatCompletionChoice(TypedDict):
    """Choice for Chat Completion Response"""
    index: int
    message: ChatCompletionMessage
    finish_reason: NotRequired[str]


class ChatCompletion(BaseModel):
    """A chat completion response."""
    id: str
    object: Literal["chat.completion"]
    created: int
    model: str
    choices: List[ChatCompletionChoice]


class CreateChatCompletionRequest(BaseModel):
    """
    All parameters are ported from HuggingFace's `GenerationConfig`.
    The alias of parameters are meant to be consistent with OpenAI's API.
    See also [Text Generation](https://huggingface.co/docs/transformers/main/main_classes/text_generation)
    """
    messages: List[ChatCompletionMessage] = Field(
        default=[], description="A list of messages to generate completions for."
    )
    stream: bool = Field(default=False)
    # Parameters that control the length of the output
    max_length: Optional[int] = Field(alias='max_tokens')
    max_new_tokens: Optional[int]
    min_length: Optional[int]
    min_new_tokens: Optional[int]
    early_stopping: Optional[bool]
    max_time: Optional[float]
    # Parameters that control the generation strategy used
    do_sample: Optional[bool]
    num_beams: Optional[int]
    num_beam_groups: Optional[int]
    penalty_alpha: Optional[float]
    use_cache: Optional[bool]
    # Parameters for manipulation of the model output logits
    temperature: Optional[float]
    top_k: Optional[int]
    top_p: Optional[float]
    typical_p: Optional[float]
    epsilon_cutoff: Optional[float]
    eta_cutoff: Optional[float]
    diversity_penalty: Optional[float]
    repetition_penalty: Optional[float]
    encoder_repetition_penalty: Optional[float]
    length_penalty: Optional[float]
    no_repeat_ngram_size: Optional[int]
    bad_words_ids: Optional[List[List[int]]]
    renormalize_logits: Optional[bool]
    # constraints: Optional[List[Constraint]]
    forced_bos_token_id: Optional[int]
    forced_eos_token_id: Optional[Union[int, List[int]]]
    remove_invalid_values: Optional[bool]
    # exponential_decay_length_penalty: Optional[Tuple[int, float]]
    suppress_tokens: Optional[List[int]]
    begin_suppress_tokens: Optional[List[int]]
    force_decoder_ids: Optional[List[List[int]]]
    # sequence_bias:Optional[Dict[Tuple[int], float]]
    guidance_scale: Optional[float]
    low_memory: Optional[bool]
    # Parameters that define the output variables of `generate`
    num_return_sequences: Optional[int] = Field(alias='n')
    # Special tokens that can be used at generation time
    pad_token_id: Optional[int]
    bos_token_id: Optional[int]
    eos_token_id: Optional[Union[int, List[int]]]
    # Generation parameters exclusive to encoder-decoder models
    encoder_no_repeat_ngram_size: Optional[int]
    decoder_start_token_id: Optional[int]

    @validator("messages")
    def validate_messages(cls, messages: List[ChatCompletionMessage]):  # pylint: disable=no-self-argument
        """Validate messages"""
        meta_error = "messages should be user and assistant alternating, optionally starting with a system message."
        if not messages:
            raise ValueError("At least one message must be provided.")
        offset = 0
        if messages[0].role == "system":
            offset = 1
        if (len(messages)-offset) % 2 != 1 or messages[-1].role != "user":
            raise ValueError(meta_error)
        for i in range(offset, len(messages)-1, 2):
            if messages[i].role != "user" or messages[i+1].role != "assistant":
                raise ValueError(meta_error)
        return messages
