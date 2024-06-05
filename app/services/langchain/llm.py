from langchain_openai import AzureChatOpenAI

from app.config import OPENAI_API_KEY, AZURE_ENDPOINT


def get_llm():
    llm = AzureChatOpenAI(
        name="docVizLLM",
        deployment_name="gpt4o",
        azure_endpoint=AZURE_ENDPOINT,
        openai_api_key=OPENAI_API_KEY,
        api_version="2024-02-15-preview",
        temperature=0,
    )
    return llm

def get_stream_llm(callback):
    llm = AzureChatOpenAI(
        name="docVizStreamLLM",
        deployment_name="gpt4o",
        azure_endpoint=AZURE_ENDPOINT,
        openai_api_key=OPENAI_API_KEY,
        api_version="2024-02-15-preview",
        temperature=0,
        callbacks=[callback],
        streaming=True,
    )
    return llm