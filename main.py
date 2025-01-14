__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import os

from crewai import Crew, Process
from rag_tool import CustomPDFSearchTool
from agents import ArticleAgents
from tasks import ArticleTasks

from dotenv import load_dotenv

load_dotenv()

class ArticleCrew:
    def __init__(self, inputs, file_path=None):
        self.inputs = inputs
        self.file_path = file_path
        self.rag_tool = CustomPDFSearchTool()
        self.agents = ArticleAgents(llm=None, rag_tool=self.rag_tool)
        self.tasks = ArticleTasks(
            self.agents.get_agents()["pdf_reader"],
            self.agents.get_agents()["article_writer"],
            self.agents.get_agents()["title_creator"],
            self.agents.get_agents()["editor"],
        )

    def run(self):
        pdf_reader = self.agents.get_agents()["pdf_reader"]
        article_writer = self.agents.get_agents()["article_writer"]
        title_creator = self.agents.get_agents()["title_creator"]
        editor = self.agents.get_agents()["editor"]

        tasks = self.tasks.get_tasks()

        crew = Crew(
            agents=[pdf_reader, article_writer, title_creator, editor],
            tasks=tasks,
            process=Process.sequential,
            planning=True,
            verbose=True,
        )

        # Add file_path as part of the input if provided
        inputs = {"user_input": self.inputs}
        if self.file_path:
            inputs["file_path"] = self.file_path

        return crew.kickoff(inputs=inputs)
