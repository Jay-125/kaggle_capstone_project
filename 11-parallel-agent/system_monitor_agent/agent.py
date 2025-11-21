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
    sub_agents=[local_news_agent, trending_fashion_agent, retail_data_agent],
)

# --- 2. Create Sequential Pipeline to gather info in parallel, then synthesize ---
root_agent = SequentialAgent(
    name="fashion_agent",
    sub_agents=[system_info_gatherer, fashion_report_synthesizer],
)
