import json
import asyncio

from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.services.langchain.utils import extract_content
from app.services.langchain.callback_handler import AsyncIteratorCallbackHandler
from app.auth.session_handlers import get_session, update_session, update_session_insights
from app.services.langchain.chain import get_map_llmchain, get_reduce_chain, get_document_insights_chain


async def generate_summary(file_id: str, session_id:str, callback:AsyncIteratorCallbackHandler):
    text, file_name = await extract_content(file_id)
    document_text = Document(page_content=text)
    splitter = RecursiveCharacterTextSplitter(chunk_size=100000, chunk_overlap=500)
    chunks = splitter.split_documents([document_text])
    chain = get_map_llmchain()
    async def invoke_chain(chunk):
        try:
            result = await chain.ainvoke(chunk)
            return result
        except Exception as e:
            return BaseMessage(content="This document may violate our content policy.", type="400 bad request")
        
    tasks = [invoke_chain(chunk) for chunk in chunks]
    
    results = await asyncio.gather(*tasks)
    results_content = [result.content for result in results]

    reduce_chain = get_reduce_chain(callback)
    summary = await reduce_chain.ainvoke({"doc_summaries":results_content})
    summary = summary.content.replace('$summary ', '').replace('$key ', '')
    json_data = summary.strip('```json\n').strip('\n```')
    json_data = json.loads(json_data)
    await update_session(session_id=session_id, data=dict({"file_name":file_name, 'summary':json_data['summary'], 'key_phrases':json_data['keyphrases']}))


async def generate_insights(session_id:str, callback:AsyncIteratorCallbackHandler):
    document_insights_chain = get_document_insights_chain(callback=callback)
    session = await get_session(session_id=session_id)
    session_data = session.data
    insights = await document_insights_chain.ainvoke({'summary_key_phrases':f"summary: {session_data['summary']}\n\n _key_phrases: {session_data["key_phrases"]}"})
    insights = insights.content.replace('$inst ', '')
    json_data = insights.strip('```json\n').strip('\n```')
    json_data = json.loads(json_data)
    await update_session_insights(session_id=session_id, data=json_data['insights'])
