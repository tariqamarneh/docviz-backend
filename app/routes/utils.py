import asyncio
from openai import BadRequestError
from fastapi import HTTPException, status
from typing import AsyncIterable, Awaitable

from app.common.logging.logger import mongo_logger
from app.services.langchain.summary import generate_summary, generate_insights
from app.services.langchain.callback_handler import AsyncIteratorCallbackHandler


async def wrap_done(fn: Awaitable, event: asyncio.Event):
    try:
        await fn
    except BadRequestError as e:
        mongo_logger.error(e)
    finally:
        event.set()


async def send_message(file_id: str, session_id: str) -> AsyncIterable[any]:
    callback = AsyncIteratorCallbackHandler()

    task = asyncio.create_task(
        wrap_done(
            generate_summary(file_id=file_id, session_id=session_id, callback=callback),
            callback.done,
        )
    )

    async for token in callback.aiter():
        yield token

    await task


async def send_message_insights(session_id: str) -> AsyncIterable[any]:
    callback = AsyncIteratorCallbackHandler()

    task = asyncio.create_task(
        wrap_done(
            generate_insights(session_id=session_id, callback=callback),
            callback.done,
        )
    )

    async for token in callback.aiter():
        yield token

    await task
