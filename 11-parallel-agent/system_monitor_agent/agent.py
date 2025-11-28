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
    # sub_agents=[retail_data_agent, trending_fashion_agent],
)

# --- 2. Create Sequential Pipeline to gather info in parallel, then synthesize ---
root_agent = SequentialAgent(
    name="fashion_agent",
    sub_agents=[system_info_gatherer, fashion_report_synthesizer],
)

# INITIALIZING RUNNER FOR DEBUGGING

from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService, DatabaseSessionService
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
import sqlite3

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

# Step 2: Switch to DatabaseSessionService
# SQLite database will be created automatically
db_url = "sqlite:///my_agent_data.db"  # Local SQLite file
session_service = DatabaseSessionService(db_url=db_url)

# session_service = InMemorySessionService()

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
            "How can I increase my sales", "Hello! What is my name?",
        ],
        "test-db-session-01",
    )

# CHECK LOGS START ==================

runner = InMemoryRunner(
    agent=root_agent,
    plugins=[
        LoggingPlugin()
    ],  # <---- 2. Add the plugin. Handles standard Observability logging across ALL agents
)

print("✅ Runner configured")

print("🚀 Running agent with LoggingPlugin...")
print("📊 Watch the comprehensive logging output below:\n")

async def main():
    response = await runner.run_debug("How can I increase my sales?")
    print("\n\n=== RESPONSE ===")
    logging.info(f"Agent response: {response}")
    print(response)


Run the async function
asyncio.run(main()) =============================
print(f"\n📁 Logs saved to: {log_filename}")

# CHECK LOGS END ===================

def check_data_in_db():
    with sqlite3.connect("my_agent_data.db") as connection:
        cursor = connection.cursor()
        result = cursor.execute(
            "select app_name, session_id, author, content from events"
        )
        print([_[0] for _ in result.description])
        for each in result.fetchall():
            print(each)


check_data_in_db()


# # CONTEXT ENGINEERING
# async def run_session_compact(
#     runner_instance: Runner,
#     user_queries: list[str] | str = None,
#     session_name: str = "default",
# ):
#     print(f"\n\n### Session: {session_name}")

#     if isinstance(user_queries, str):
#         user_queries = [user_queries]

#     for query in user_queries:
#         print(f"\nUser > {query}")

#         message = types.Content(
#             role="user",
#             parts=[types.Part(text=query)]
#         )

#         async for event in runner_instance.run_async(
#             user_id=USER_ID,
#             session_id=session_name,   # ✔ use the SAME session name every turn
#             new_message=message,
#         ):
#             if event.content and event.content.parts:
#                 text = event.content.parts[0].text
#                 if text and text.strip() != "None":
#                     print(f"{MODEL_NAME} > {text}")



# research_app_compacting = App(
#     name=APP_NAME,
#     root_agent=root_agent,
#     # This is the new part!
#     events_compaction_config=EventsCompactionConfig(
#         compaction_interval=2,  # Trigger compaction every 3 invocations
#         overlap_size=1,  # Keep 1 previous turn for context
#     ),
# )

# db_url = "sqlite:///my_agent_data_compact.db"  # Local SQLite file
# session_service = DatabaseSessionService(db_url=db_url)

# # Create a new runner for our upgraded app
# research_runner_compacting = Runner(
#     app=research_app_compacting, session_service=session_service
# )

# print("✅ Research App upgraded with Events Compaction!")

# SESSION_NAME = "test-db-session-03"

# async def main_turns():
#     await run_session_compact(
#         research_runner_compacting,
#         "How can I increase my sales?",
#         SESSION_NAME,
#     )

#     await run_session_compact(
#         research_runner_compacting,
#         "What are the products that gave me high profit based on my retail data?",
#         SESSION_NAME,
#     )

#     await run_session_compact(
#         research_runner_compacting,
#         "Based on trending fashion reports, which retail products might trend next?",
#         SESSION_NAME,
#     )

#     await run_session_compact(
#         research_runner_compacting,
#         "Suggest me, how can I do invest money in ads to increase my sales",
#         SESSION_NAME,
#     )


# # CHECKING FOR COMPACT SESSIONS THAT PROVES THAT WE HAVE CONTEXT ENGINEERIG IN PLACE

# async def check_compactness():
#     print("\n===========================CHECKING COMPACTION===========================")

#     session = await session_service.get_session(
#         app_name=research_runner_compacting.app_name,
#         user_id=USER_ID,
#         session_id=SESSION_NAME,
#     )

#     print(f"\nTotal events stored: {len(session.events)}")

#     found = False
#     for event in session.events:
#         # ADK v0.3+ compaction events use type="compaction"
#         print(event)
#         if getattr(event, "type", None) == "compaction":
#             print("\n✅ FOUND COMPACTION EVENT!")
#             print("Summary contents:\n", event.compaction)
#             found = True
#             break

#     if not found:
#         print("\n❌ No compaction event found. (Did you run 3+ turns?)")


# print ("===========================CHECKING FOR COMPACT DATA=======================================")

# async def main_compact():
#     # ✅ Create DB session once so runner can write into it
#     try:
#         await session_service.create_session(
#             app_name=research_runner_compacting.app_name,
#             user_id=USER_ID,
#             session_id=SESSION_NAME,
#         )
#     except:
#         pass  # session already exists

#     await main_turns()
#     await check_compactness()

# # asyncio.run(main_compact()) ====================================
