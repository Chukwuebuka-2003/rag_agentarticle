from crewai import Agent
from langchain.chat_models import ChatOpenAI


class ArticleAgents:
    def __init__(self, llm):
        self.pdf_reader = Agent(
            llm= llm,
            role = "PDF Content Extractor",
            goal = "Extract and preprocess text from a PDF based on the user input: {user_input}",
            backstory = "Specializes in handling and interpreting PDF documents",

            allow_delegation= False,
            tools= [rag_tool],
            verbose=True
        )

        self.article_writer = Agent(
            llm=llm,
            role = "Article Creator",
            goal = "Write a concise and engaging article using the contents of the article_writer agent",
            backstory= "Expert in creating informative and engaging articles",
            allow_delegation= False,
            verbose=True

        )

        self.title_creator  = Agent(
            llm=llm,
            role = "Title Generator",
            goal = "Generate a compelling title for the article",
            backstory = "Skilled in crafting engaging and relevant titles",
            allow_delegation= False,
            verbose= True
        )


        self.editor = Agent(
            llm=llm,
            role = "Article Editor",
            goal = "Proofread, refine, and structure the article to ensure it is ready for publication.",
            backstory = "A meticulous editor responsible for reviewing and polishing the article content from the Article Creator. "
                  "Your focus is on improving readability, ensuring error-free copy, enhancing structure, and aligning the tone with the article's vision. "
                  "You ensure the article engages the audience, flows logically, and highlights key insights effectively.",
            allow_delegation= False,
            verbose = True
        )


    def get_agents(self):
        return {
            "pdf_reader": self.pdf_reader,
            "article_writer" : self.article_writer,
            "title_creator"  : self.title_creator,
            "editor": self.editor
        }