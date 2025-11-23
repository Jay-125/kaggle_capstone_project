"""
System Monitor Root Agent

This module defines the root agent for the system monitoring application.
It uses a parallel agent for system information gathering and a sequential
pipeline for the overall flow.
"""

from google.adk.agents import ParallelAgent, SequentialAgent

from .subagents.local_news_agent import local_news_agent
from .subagents.retail_data_agent import retail_data_agent
from .subagents.trending_fashion_agent import trending_fashion_agent
from .subagents.synthesizer_agent import fashion_report_synthesizer

# --- 1. Create Parallel Agent to gather information concurrently ---
system_info_gatherer = ParallelAgent(
    name="system_info_gatherer",
    sub_agents=[retail_data_agent, local_news_agent, trending_fashion_agent],
)

# --- 2. Create Sequential Pipeline to gather info in parallel, then synthesize ---
root_agent = SequentialAgent(
    name="fashion_agent",
    sub_agents=[system_info_gatherer, fashion_report_synthesizer],
)

# INITIALIZING RUNNER FOR DEBUGGING

from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.adk.plugins.logging_plugin import (
    LoggingPlugin,
)  # <---- 1. Import the Plugin
from google.genai import types
import asyncio
import os
import logging
from datetime import datetime
import uuid
from google.adk.runners import Runner

os.environ["GOOGLE_API_KEY"] = "<api-key>"

# Create logs directory
os.makedirs("logs", exist_ok=True)

MODEL_NAME = 'gemini-2.0-flash'

# Timestamped filename
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f"logs/agent_{timestamp}.log"

# Configure logging
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s",
)

session_service = InMemorySessionService()

initial_state = {
    "store_name": "Fashion Bug",
    "type_of_store": "fashion",
    "city": "Mumbai",
    "country": "India"
}

# Create a NEW session
APP_NAME = "fashion_upsell"
USER_ID = "John Doe"
SESSION_ID = str(uuid.uuid4())
stateful_session = session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state,
)
print("CREATED NEW SESSION:")
print(f"\tSession ID: {SESSION_ID}")

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

# Define helper functions that will be reused throughout the notebook
async def run_session(
    runner_instance: Runner,
    user_queries: list[str] | str = None,
    session_name: str = "default",
):
    print(f"\n ### Session: {session_name}")

    # Get app name from the Runner
    app_name = runner_instance.app_name

    # Attempt to create a new session or retrieve an existing one
    try:
        session = await session_service.create_session(
            app_name=app_name, user_id=USER_ID, session_id=session_name
        )
    except:
        session = await session_service.get_session(
            app_name=app_name, user_id=USER_ID, session_id=session_name
        )

    # Process queries if provided
    if user_queries:
        # Convert single query to list for uniform processing
        if type(user_queries) == str:
            user_queries = [user_queries]

        # Process each query in the list sequentially
        for query in user_queries:
            print(f"\nUser > {query}")

            # Convert the query string to the ADK Content format
            query = types.Content(role="user", parts=[types.Part(text=query)])

            # Stream the agent's response asynchronously
            async for event in runner_instance.run_async(
                user_id=USER_ID, session_id=session.id, new_message=query
            ):
                # Check if the event contains valid content
                if event.content and event.content.parts:
                    # Filter out empty or "None" responses before printing
                    if (
                        event.content.parts[0].text != "None"
                        and event.content.parts[0].text
                    ):
                        print(f"{MODEL_NAME} > ", event.content.parts[0].text)
    else:
        print("No queries!")


async def main():
    response = await run_session(
        runner,
        [
            "How can I increase my sales",
        ],
        "stateful-agentic-session",
    )


# runner = InMemoryRunner(
#     agent=root_agent,
#     plugins=[
#         LoggingPlugin()
#     ],  # <---- 2. Add the plugin. Handles standard Observability logging across ALL agents
# )

# print("✅ Runner configured")

# print("🚀 Running agent with LoggingPlugin...")
# print("📊 Watch the comprehensive logging output below:\n")

# async def main():
#     response = await runner.run_debug("How can I increase my sales?")
#     print("\n\n=== RESPONSE ===")
#     logging.info(f"Agent response: {response}")
#     print(response)


# Run the async function
asyncio.run(main())
# print(f"\n📁 Logs saved to: {log_filename}")
