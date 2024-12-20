from crewai import Agent

from tools.browser_tools import BrowserTools
from tools.calculator_tools import CalculatorTools
from tools.search_tools import SearchTools
from tools.finance_tools import FinanceTools
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from dotenv import load_dotenv
import os

load_dotenv()
from groq import Groq

# Initialize Groq Client
groq_api_key = os.environ.get("GROQ_API_KEY")
if not groq_api_key:
    raise EnvironmentError("GROQ_API_KEY not found in environment variables.")

llm = Groq(api_key=groq_api_key)  # Initialize the Groq instance


class StockAnalysisAgents():
  def financial_analyst(self):
    return Agent(
      role='The Best Financial Analyst',
      goal="""Impress all customers with your financial data 
      and market trends analysis""",
      backstory="""The most seasoned financial analyst with 
      lots of expertise in the indian stock market analysis and investment
      strategies that is working for a super important customer.""",
      verbose=True,
      tools=[
        BrowserTools.scrape_and_summarize_website,
        SearchTools.search_internet,
        CalculatorTools.calculate,
        FinanceTools.search_annual_income_statement,
        FinanceTools.search_quarterly_income_statement,
        FinanceTools.search_stock_fundamentals
      ],
      llm=llm,
      memory=True
    )

  def research_analyst(self):
    return Agent(
      role='Staff Research Analyst',
      goal="""Being the best at gather, interpret data and amaze
      your customer with it""",
      backstory="""Known as the BEST research analyst, you're
      skilled in sifting through news, company announcements, 
      and indian market sentiments. Now you're working on a super 
      important customer.""",
      verbose=True,
      tools=[
        BrowserTools.scrape_and_summarize_website,
        SearchTools.search_internet,
        CalculatorTools.calculate,
        FinanceTools.search_annual_income_statement,
        FinanceTools.search_quarterly_income_statement,
        FinanceTools.search_stock_fundamentals
      ],
      llm=llm,
      memory=True
  )

  def investment_advisor(self):
    return Agent(
      role='Private Investment Advisor',
      goal="""Impress your customers with full analyses over stocks
      and completer investment recommendations""",
      backstory="""You're the most experienced investment advisor
      and you combine various analytical insights to formulate
      strategic investment advice. You are now working for
      a super important customer you need to impress.""",
      verbose=True,
      tools=[
        BrowserTools.scrape_and_summarize_website,
        SearchTools.search_internet,
        SearchTools.search_news,
        CalculatorTools.calculate
      ],
      llm=llm,
      memory=True
    )