import os
import re

from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_google_genai import ChatGoogleGenerativeAI

from prompts import (
    RESEARCHER_PROMPT,
    WRITER_PROMPT,
    CRITIC_PROMPT
)

load_dotenv()

# Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Tavily Client
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def researcher_agent(topic):
    search = tavily.search(
        query=topic,
        max_results=5
    )

    research = llm.invoke(
        f"""
        {RESEARCHER_PROMPT}

        Topic:
        {topic}

        Search Results:

        {search}
        """
    )

    return research.content

def writer_agent(topic, research_notes, feedback=""):

    report = llm.invoke(
        f"""
        {WRITER_PROMPT}

        Topic:

        {topic}

        Research Notes:

        {research_notes}

        Reviewer Feedback:

        {feedback}
        """
    )

    return report.content

def critic_agent(report):

    review = llm.invoke(
        f"""
        {CRITIC_PROMPT}

        Report:

        {report}
        """
    )

    text = review.content

    match = re.search(r"Score:\s*(\d+)", text)

    score = int(match.group(1)) if match else 0

    approved = score >= 8

    return {
        "score": score,
        "feedback": text,
        "approved": approved
    }