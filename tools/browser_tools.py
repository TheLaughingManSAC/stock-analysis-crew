from crewai_tools import tool
from crewai import Agent, Task
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
load_dotenv()


from groq import Groq

# Initialize Groq Client
groq_api_key = os.environ.get("GROQ_API_KEY")
if not groq_api_key:
    raise EnvironmentError("GROQ_API_KEY not found in environment variables.")

llm = Groq(api_key=groq_api_key)  # Initialize the Groq instance



class BrowserTools():
    
    @tool("Scrape website content")
    def scrape_and_summarize_website(source_url: str) -> str:
        """Useful to scrape and summarize a website content with financial news, blog, etc."""
        response = requests.get(source_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            relevant_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'div', 'section', 'article'])    
            content = "\n\n".join([str(el) for el in relevant_elements])
            content_chunks = [content[i:i + 8000] for i in range(0, len(content), 8000)]
            summaries = []
            for chunk in content_chunks:
                agent = Agent(
                    role='Principal Researcher',
                    goal=
                    'Do amazing research and summaries based on the content you are working with',
                    backstory=
                    "You're a Principal Researcher at a big company and you need to do research about a given topic.",
                    allow_delegation=False,
                    llm=llm)
                task = Task(
                    agent=agent,
                    description=
                    f'Analyze and summarize the content below, make sure to include the most relevant information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n{chunk}',
                    expected_output='A paragraph of the summary of the content provided. Should be detailed.'
                )
                summary = task.execute()
                summaries.append(summary)
            return "\n\n".join(summaries)
        else:
           return f"Failed to fetch content from {source_url}. Status code: {response.status_code}"