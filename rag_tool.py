# rag_tool.py

from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from crewai_tools import PDFSearchTool

# Define the input schema for the tool
class PDFSearchToolInput(BaseModel):
    pdf_path: str = Field(..., description="Path to the PDF file to search within.")
    query: str = Field(..., description="The search query to find in the PDF.")

class CustomPDFSearchTool(BaseTool):
    name: str = "Custom PDF Search Tool"
    description: str = "Searches within a PDF document for a given query."
    args_schema: Type[BaseModel] = PDFSearchToolInput

    def _run(self, pdf_path: str, query: str) -> str:
        # Initialize the PDFSearchTool with the provided PDF path
        rag_tool = PDFSearchTool(
            pdf=pdf_path,
            config=dict(
                llm=dict(
                    provider="groq",  # or google, openai, anthropic, llama2, ...
                    config=dict(
                        model="mixtral-8x7b-32768",
                        temperature=0.5,
                    ),
                ),
                embedder=dict(
                    provider="google",  # or openai, ollama, ...
                    config=dict(
                        model="models/embedding-001",
                    ),
                ),
            )
        )
        # Perform the search with the provided query
        result = rag_tool.run(query)
        return result
