"""
Store retail data

This agent is responsible for gathering previous year store retail data.
"""

from google.adk.agents import LlmAgent

from .tools import get_retail_data

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Disk Information Agent
retail_data_agent = LlmAgent(
    name="RetailDataAgent",
    model=GEMINI_MODEL,
    instruction="""You are a store retail agent.
    
    Use tool 'get_retail_data' to get the json data about the previous year store retail data.
    You need to analyse the data and provide the summary of the data in final response.
    Make sure that the summary must have two key points:
    
    1. product name
    2. ProfitCategory
    
    IMPORTANT: You MUST call the get_retail_data tool. Do not make up information.
    """,
    description="Gathers and analyzes store retail data",
    tools=[get_retail_data],
    output_key="retail_data",
)
