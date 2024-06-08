from app.services.langchain.llm import get_llm, get_stream_llm
from app.services.langchain.callback_handler import AsyncIteratorCallbackHandler
from app.services.prompt.summary_prompt import (
    map_prompt,
    reduce_prompt,
    document_insights_prompt,
)


def get_map_llmchain():
    llm = get_llm()
    map_chain = map_prompt | llm
    return map_chain


def get_reduce_chain(callback: AsyncIteratorCallbackHandler):
    llm = get_stream_llm(callback=callback)
    reduce_chain = reduce_prompt | llm
    return reduce_chain


def get_document_insights_chain(callback: AsyncIteratorCallbackHandler):
    llm = get_stream_llm(callback=callback)
    document_insights_chain = document_insights_prompt | llm
    return document_insights_chain
