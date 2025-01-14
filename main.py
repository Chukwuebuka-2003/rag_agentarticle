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
    def __init__(self, inputs):
        self.inputs = inputs
        self.rag_tool = CustomPDFSearchTool()
        self.agents = ArticleAgents(llm=None, rag_tool = self.rag_tool)
        self.tasks = ArticleTasks(self.agents.get_agents()["pdf_reader"],
                                  self.agents.get_agents()["article_writer"],
                                  self.agents.get_agents()["title_creator"],
                                  self.agents.get_agents()["editor"]
        )


    def run(self):
        pdf_reader = self.agents.get_agents()["pdf_reader"]
        article_writer = self.agents.get_agents()["article_writer"]
        title_creator = self.agents.get_agents()["title_creator"]
        editor =self.agents.get_agents()["editor"]

        tasks = self.tasks.get_tasks()

        crew = Crew(
            agents=[pdf_reader, article_writer, title_creator, editor],
            tasks=tasks,
            process= Process.sequential,
            planning=True,
            verbose=True
        )

        
        return crew.kickoff(inputs={"user_input": self.inputs})