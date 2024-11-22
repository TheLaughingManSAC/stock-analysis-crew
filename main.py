from crewai import Crew
from textwrap import dedent

from stock_analysis_agents import StockAnalysisAgents
from stock_analysis_tasks import StockAnalysisTasks
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from groq import Groq

# Initialize Groq Client
groq_api_key = os.environ.get("GROQ_API_KEY")
if not groq_api_key:
    raise EnvironmentError("GROQ_API_KEY not found in environment variables.")

llm = Groq(api_key=groq_api_key)  # Initialize the Groq instance

class FinancialCrew:
  def __init__(self, company:str):
    self.company = company

  def run(self) -> str:
    agents = StockAnalysisAgents()
    tasks = StockAnalysisTasks()

    research_analyst_agent = agents.research_analyst()
    financial_analyst_agent = agents.financial_analyst()
    investment_advisor_agent = agents.investment_advisor()

    research_task = tasks.research(research_analyst_agent, self.company)
    financial_task = tasks.financial_analysis(financial_analyst_agent, self.company)
    filings_task = tasks.filings_analysis(financial_analyst_agent, self.company)
    recommend_task = tasks.recommend(investment_advisor_agent, self.company)

    crew = Crew(
      agents=[
        research_analyst_agent,
        financial_analyst_agent,
        investment_advisor_agent
      ],
      tasks=[
        research_task,
        financial_task,
        filings_task,
        recommend_task
      ],
      verbose=True,
      llm=llm
    )

    result = crew.kickoff()
    return result

if __name__ == "__main__":
  print("## Welcome to Financial Analysis Crew")
  print('-------------------------------')
  company = input(
    dedent("""
      What is the company you want to analyze?
    """))
  
  financial_crew = FinancialCrew(company)

  result = financial_crew.run()
  print("\n\n########################")
  print("## Here is the Report")
  print("########################\n")
  print(result)
  
  os.remove('financial_data.json')