from google.adk.agents import Agent
from google.adk.tools import google_search

get_latest_trending_fashion_news = Agent(
    name="get_latest_trending_fashion_news",
    model="gemini-2.0-flash",
    description="News analyst agent to get trending fashion news",
    instruction="""
    You are a helpful assistant that can fetches the news about what .

    Use 'google_search' tool to fetch the current trends.
    You must have answers for below 5 questions:

    1. Which product categories and styles are currently selling the most?
    2. What colors, fabrics, or designs are most popular among customers right now?
    3. What fashion items are trending on social media and influencing customer demand?
    4. Which customer segments (age, gender, region) are driving current trends?
    5. Which products are seeing a rapid increase in sales or searches compared to previous weeks/months?

    IMPORTANT: You MUST call the google_search tool to fetch answers of above 5 questions. Do not make up information.
    """,
    tools=[google_search],
)
