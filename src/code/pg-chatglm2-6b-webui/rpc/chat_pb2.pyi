from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Optional, Text

DESCRIPTOR: _descriptor.FileDescriptor

class ChatReply(_message.Message):
    __slots__ = ["answer"]
    ANSWER_FIELD_NUMBER: ClassVar[int]
    answer: str
    def __init__(self, answer: Optional[str] = ...) -> None: ...

class ChatRequest(_message.Message):
    __slots__ = ["history", "question"]
    HISTORY_FIELD_NUMBER: ClassVar[int]
    QUESTION_FIELD_NUMBER: ClassVar[int]
    history: _containers.RepeatedScalarFieldContainer[str]
    question: str
    def __init__(self, question: Optional[str] = ..., history: Optional[Iterable[str]] = ...) -> None: ...
