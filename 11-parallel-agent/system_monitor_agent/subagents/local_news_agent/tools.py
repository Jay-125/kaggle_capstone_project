"""
web search Tool

This module provides a tool to search web to get latest news.
"""

import time
from typing import Any, Dict

import psutil

from langchain_tavily import TavilySearch

# from ...input_json import city_name, country_name, type_of_store

TAVILY_API_KEY = "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"

city_name = "Mumbai"
country_name = "India"
type_of_store = "fashion"


def get_latest_news() -> Any:
    """
    Gathers latest news.

    Returns:
        Any: latest news data
    """
    try:
        search_tool = TavilySearch(
            max_results=5,
            topic="general",
            tavily_api_key=TAVILY_API_KEY,
        )

        response = search_tool.invoke("What's the latest news in city Mumbai, India ? Give me everything related to Fashion in the news ?")
        return response
    except Exception as e:
        return {
            "result": {"error": f"Failed to gather latest news: {str(e)}"},
            "stats": {"success": False},
            "additional_info": {"error_type": str(type(e).__name__)},
        }
