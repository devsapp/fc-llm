"""The main server module."""
import time
import uuid
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from sse_starlette.sse import EventSourceResponse
from app.model.llm import BaseLLM, load_model
from app.schema import CreateChatCompletionRequest, ChatCompletionChunkChoice, ChatCompletionChunkDelta, ChatCompletionChunkDeltaEmpty, ChatCompletionChunk, ChatCompletionMessage, ChatCompletionChoice, ChatCompletion  # pylint: disable=no-name-in-module

llm: BaseLLM = load_model()
app = FastAPI()

assert llm is not None


@app.get("/")
def index():
    """Redirect to docs."""
    return RedirectResponse(url="/docs")


@app.post("/v1/chat/completions",)
async def create_chat_completion(
    body: CreateChatCompletionRequest,
):
    """Create a chat completion."""
    stream = body.stream
    params = {k: v for k, v in vars(body).items() if v is not None}
    params.pop("stream")
    model_name = llm.__class__.__name__
    completion_id = str(uuid.uuid4())
    created = int(time.time())
    if stream:
        def generate(**kwargs):
            """Generate"""
            for resp in llm.stream_chat(**kwargs):
                if not resp:
                    continue
                delta = ChatCompletionChunkDelta(role="assistant", content=resp)
                choice = ChatCompletionChunkChoice(index=0, delta=delta)
                chunk = ChatCompletionChunk(
                    id=completion_id, created=created,
                    model=model_name, choices=[choice],
                    object="chat.completion.chunk")
                yield chunk.json(exclude_unset=True, ensure_ascii=False)
            delta = ChatCompletionChunkDeltaEmpty()
            choice = ChatCompletionChunkChoice(index=0, delta=delta, finish_reason="stop")
            chunk = ChatCompletionChunk(
                id=completion_id, created=created,
                model=model_name, choices=[choice],
                object="chat.completion.chunk")
            yield chunk.json(exclude_unset=True, ensure_ascii=False)
            yield '[Done]'
        return EventSourceResponse(generate(**params), media_type="text/event-stream")
    resp = llm.chat(**params)
    choice = ChatCompletionChoice(index=0, message=ChatCompletionMessage(
        role="assistant", content=resp), finish_reason="stop")
    return ChatCompletion(
        id=completion_id, created=created, model=model_name, choices=[choice],
        object="chat.completion")
