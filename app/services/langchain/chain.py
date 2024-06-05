from langchain.chains.combine_documents.map_reduce import MapReduceDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.combine_documents.reduce import ReduceDocumentsChain
from app.services.langchain.callback_handler import AsyncIteratorCallbackHandler
from langchain.chains.llm import LLMChain
from app.services.langchain.llm import get_llm, get_stream_llm
from app.services.prompt.summary_prompt import map_prompt, reduce_prompt, document_insights_prompt


def get_chain():
    llm = get_llm()
    map_chain = LLMChain(prompt=map_prompt, llm=llm)
    
    reduce_chain = LLMChain(prompt=reduce_prompt, llm=llm)
    stuff_chain = StuffDocumentsChain(
        llm_chain=reduce_chain, document_variable_name="doc_summaries"
    )
    reduce_chain = ReduceDocumentsChain(
        combine_documents_chain=stuff_chain,
    )
    map_reduce_chain = MapReduceDocumentsChain(
        llm_chain=map_chain,
        document_variable_name="content",
        reduce_documents_chain=reduce_chain,
        output_key='outout'
    )
    return map_reduce_chain


def get_map_llmchain():
    llm = get_llm()
    map_chain = map_prompt | llm
    return map_chain

def get_reduce_chain(callback:AsyncIteratorCallbackHandler):
    llm = get_stream_llm(callback=callback)
    reduce_chain = reduce_prompt | llm
    return reduce_chain

def get_document_insights_chain(callback:AsyncIteratorCallbackHandler):
    llm = get_stream_llm(callback=callback)
    document_insights_chain = document_insights_prompt | llm
    return document_insights_chain