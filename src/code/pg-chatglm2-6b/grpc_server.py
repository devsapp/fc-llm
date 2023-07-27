"""Module providingFunction printing python version."""
import sys
import asyncio
import grpc
from logger import logger
import model
import config
from rpc.chat_pb2 import ChatReply, ChatRequest  # pylint: disable = no-name-in-module
from rpc.chat_pb2_grpc import ChatServiceServicer, add_ChatServiceServicer_to_server


listen_addr = f"0.0.0.0:{config.PORT}"
llm: model.BaseLLM = None
if config.LLM_MODEL.startswith("internlm"):
    from model.internlm import InternLM
    llm = InternLM(config.MODEL_PATH, config.MAX_TOKEN,
                   config.TEMPERATURE, config.TOP_P, config.LLM_DEVICE)
else:
    from model.chatglm import ChatGLM
    llm = ChatGLM(config.MODEL_PATH, config.MAX_TOKEN,
                  config.TEMPERATURE, config.TOP_P, config.LLM_DEVICE, config.LLM_MODEL)


class Chat(ChatServiceServicer):  # pylint: disable = too-few-public-methods
    """Module providingFunction printing python version."""

    def chat(self, request: ChatRequest, _: grpc.aio.ServicerContext) -> ChatReply:
        """Module providingFunction printing python version."""
        try:
            yield ChatReply(answer=llm.stream_chat(request.question, request.history))
        except RuntimeError as error:
            logger.error(error)
            sys.exit(1)


async def serve() -> None:
    """Module providingFunction printing python version."""
    server = grpc.aio.server()
    add_ChatServiceServicer_to_server(Chat(), server)
    server.add_insecure_port(listen_addr)
    logger.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


def run():
    """Module providingFunction printing python version."""
    asyncio.run(serve())


if __name__ == "__main__":
    run()
