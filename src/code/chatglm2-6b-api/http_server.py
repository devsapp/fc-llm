"""Module providingFunction printing python version."""
from typing import List
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel  # pylint: disable = no-name-in-module
import uvicorn
import model
import config

llm: model.BaseLLM = None
if config.LLM_MODEL.startswith("internlm"):
    from model.internlm import InternLM
    llm = InternLM(config.MODEL_PATH, config.MAX_TOKEN,
                   config.TEMPERATURE, config.TOP_P, config.LLM_DEVICE)
else:
    from model.chatglm import ChatGLM
    llm = ChatGLM(config.MODEL_PATH, config.MAX_TOKEN,
                  config.TEMPERATURE, config.TOP_P, config.LLM_DEVICE, config.LLM_MODEL)
app = FastAPI()


class ChatRequest(BaseModel):
    """Function printing python version."""
    question: str
    history: List[str]


class ChatResponse(BaseModel):
    """Function printing python version."""
    answer: str


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Function printing python version."""
    return {"answer": llm.chat(req.question, req.history)}


async def stream_response(question: str, history: List[str]):
    """Function printing python version."""
    last_len = 0
    for resp in llm.stream_chat(question, history):
        yield resp[last_len:]
        last_len = len(resp)


@app.post("/chat/stream")
async def stream_chat(req: ChatRequest):
    """Function printing python version."""
    return StreamingResponse(stream_response(req.question, req.history))


def run():
    """Function printing python version."""
    uvicorn.run(app=app, host="0.0.0.0", port=config.PORT)


if __name__ == "__main__":
    run()
