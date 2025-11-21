"""
Local news agent

This agent is responsible for gathering local news of a state.
"""

import os

from google.adk.agents import LlmAgent

from .tools import get_latest_news

# from ...input_json import city_name, country_name, type_of_store

city_name = "Mumbai"
country_name = "India"
type_of_store = "fashion"

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"


# CPU Information Agent
local_news_agent = LlmAgent(
    # name="CpuInfoAgent",
    name="LocalNewsAgent",
    model=GEMINI_MODEL,
    instruction="""You are a local news Agent.
    You need to use the tool 'get_latest_news' to gather latest local news of city Mumbai in country India related to Fashion.
    Then you need analyze the news and give some points to show whether there were no latest news related to Fashion.
    If there are some news related to that, it is positive and negative.
    Give your detailed response in points.
    
    IMPORTANT: You MUST call the get_cpu_info tool. Do not make up information.
    """,
    description="Gathers and analyzes latest news",
    tools=[get_latest_news],
    output_key="latest_news",
)
