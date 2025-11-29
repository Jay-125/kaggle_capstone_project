import json
import requests
import subprocess
import time
import uuid

from google.adk.agents import LlmAgent, Agent
from google.adk.tools import google_search
from google.adk.agents.remote_a2a_agent import (
    RemoteA2aAgent,
    AGENT_CARD_WELL_KNOWN_PATH,
)

from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import os

# Hide additional warnings in the notebook
import warnings

os.environ["GOOGLE_API_KEY"] = "<api-key>"

agent_for_a2a = Agent(
    name="agent_for_a2a",
    model="gemini-2.0-flash",
    description="Agent to fetch latest news",
    instruction=""" You are an agent fetches local news in the city.
    You need to use the tool 'google_search' to gather latest local news of city Mumbai in country India related to Fashion.
    Then you need analyze the news and give some points to show whether any of the news can affect the fashion sales.
    If there are some news related to that, just say now news for today.
    But if you found some news, then give a summary on how that news can affect the sales of fashion.
    Give your detailed response in points.
    
    IMPORTANT: You MUST call the google_search tool. Do not make up information.
    """,
    tools=[google_search],
)

# Convert the agent to an A2A-compatible application
# This creates a FastAPI/Starlette app that:
#   1. Serves the agent at the A2A protocol endpoints
#   2. Provides an auto-generated agent card
#   3. Handles A2A communication protocol
agent_for_a2a_app = to_a2a(
    agent_for_a2a, port=8001  # Port where this agent will be served
)

# 👇 REQUIRED: Uvicorn expects this name
app = agent_for_a2a_app

print("✅ Product Catalog Agent is now A2A-compatible!")
print("   Agent will be served at: http://localhost:8001")
print("   Agent card will be at: http://localhost:8001/.well-known/agent-card.json")

print("   Ready to start the server...")
