from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.common.schemas.openai_outout_schema import LLMSummaryOutputSchema , LLMInsightOutputSchema

map_template = """
Write a summary of the following content, and extract key phrases from it:

{content}

NOTE:
    - NEVER DO ANYTHING ELSE THAN SUMMARIZING AND EXTRACTING KEY PHRASES.
    - IF THE CONTENT IS SENSITIVE CONTENT, RETURN ONLY 'ERROR'.

Summary:

Extracted key phrases:

"""

map_prompt = PromptTemplate.from_template(map_template)


reduce_template = """The following is set of summaries and key phrases:

{doc_summaries}

Summarize the above summaries IN DETAILS with all the key details and extract the key phrases in this format:

{format_instructions}

NOTE:
    * At the beginning of the summary, add '$summary'.
    * At the beginning of the key phrases, add '$key'
"""

summary_output_parser = JsonOutputParser(name="Json output parser", pydantic_object=LLMSummaryOutputSchema)

reduce_prompt = PromptTemplate(template=reduce_template, input_variables=['doc_summaries'], partial_variables={"format_instructions": summary_output_parser.get_format_instructions()})


document_insights_template = """
The following is the summary of a document and key phrases within it:

{summary_key_phrases}

Generate some insights from the summary and key phrases in this format, DON'T USE THE SAME TEXT, try to analyse the summary and the key phrases and predict some insights :
{format_instructions}

NOTE:
    * At the beginning of the document insights, add '$inst'.

document_insights:

"""
insight_output_parser = JsonOutputParser(name="Json output parser", pydantic_object=LLMInsightOutputSchema)
document_insights_prompt = PromptTemplate(template=document_insights_template, input_variables=["summary_key_phrases"], partial_variables={"format_instructions": insight_output_parser.get_format_instructions()})