from crewai import Task

class ArticleTasks:
    def __init__(self, pdf_reader, article_writer, title_creator, editor):
        self.pdf_reading_task = Task(
            description = "Read and preprocess the PDF",
            agent=pdf_reader,
            expected_output= "Extracted and preprocessed text from a PDF",
        )


        self.task_article_writing = Task (
            description= "Create a concise article with 8-10 paragraphs based on the extracted PDF content.",
            agent = article_writer,
            expected_output= "8-10 paragraphs describing the key points of the PDF",
        )

        self.task_title_generation = Task(
            description= "Generate an engaging and relevant title for the article.",
            agent = title_creator,
            expected_output= "A Title of About 5-7 Words",
        )


        self.edit_task = Task(
            description= "Proofread and structure the article to ensure it is publication-ready.",
            agent = editor,
            expected_output= "A finalized article, ready for publication. Each section should be captivating and have 5 paragraphs",
        )


    def get_tasks(self):
        return [
            self.pdf_reading_task,
            self.task_article_writing,
            self.task_title_generation,
            self.edit_task
        ]