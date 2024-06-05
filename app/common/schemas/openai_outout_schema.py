from pydantic import BaseModel, Field


class LLMSummaryOutputSchema(BaseModel):
    summary: str = Field(description="Summary of the document")
    keyphrases: str = Field(description="Extracted key phrases")


class LLMInsightOutputSchema(BaseModel):
    insights: str = Field(description="insights from the document")
