import json
import asyncio
from typing import Any, AsyncIterator, Dict, List, Literal, Union, cast

from langchain_core.outputs import LLMResult
from langchain_core.callbacks import AsyncCallbackHandler


class AsyncIteratorCallbackHandler(AsyncCallbackHandler):
    queue: asyncio.Queue[str]
    done: asyncio.Event

    @property
    def always_verbose(self) -> bool:
        return True

    def __init__(self) -> None:
        self.queue = asyncio.Queue()
        self.done = asyncio.Event()
        self.flag = False
        self.key = ""
        self.index = 0

    async def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        self.done.clear()

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        if token == ' "$':
            self.flag = True
            self.index = 0
        if (
            token is not None
            and token != ""
            and token != ' "$'
            and token != "}"
            and token != "```"
        ):
            if self.flag:
                self.key = token
                self.flag = False
            data = {"data": f"{token}", "type": f"{self.key}", "index": self.index}
            self.queue.put_nowait(json.dumps(data) + "\n")
        self.index += 1

    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        self.done.set()

    async def on_llm_error(self, error: BaseException, **kwargs: Any) -> None:
        self.done.set()

    async def aiter(self) -> AsyncIterator[str]:
        while not self.queue.empty() or not self.done.is_set():
            # Wait for the next token in the queue,
            # but stop waiting if the done event is set
            done, other = await asyncio.wait(
                [
                    # NOTE: If you add other tasks here, update the code below,
                    # which assumes each set has exactly one task each
                    asyncio.ensure_future(self.queue.get()),
                    asyncio.ensure_future(self.done.wait()),
                ],
                return_when=asyncio.FIRST_COMPLETED,
            )

            # Cancel the other task
            if other:
                other.pop().cancel()

            # Extract the value of the first completed task
            token_or_done = cast(Union[str, Literal[True]], done.pop().result())

            # If the extracted value is the boolean True, the done event was set
            if token_or_done is True:
                break

            # Otherwise, the extracted value is a token, which we yield
            yield token_or_done
