"""
Trending data Agent

This agent is responsible for gathering and analyzing trending fashion data.
"""

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from ..get_latest_trending_fashion_news.agent import get_latest_trending_fashion_news

# from .tools import get_memory_info

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Memory Information Agent
trending_fashion_agent = LlmAgent(
    name="TrendingFashionAgent",
    model=GEMINI_MODEL,
    instruction="""You are a trending data analysis agent.
    
    Use tool 'get_latest_trending_fashion_news' to get all the latest news about fashion.
    You need to analyse the data to create a summary of what are the fashion trends going on and what are the driving factors of those.
    If you face some data missing issue, just create a summary with the data available.
    DO NOT say that the data is not available
    
    IMPORTANT: You MUST call the get_latest_trending_fashion_news tool. Do not make up information.
    """,
    description="Gathers and analyzes memory information",
    tools=[AgentTool(get_latest_trending_fashion_news)],
    output_key="trending_info",
)
