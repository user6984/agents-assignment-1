"""
Source Hunter Agent

TODO: Implement this agent that searches the curated paper corpus
to find relevant passages for each sub-question in the query strategy.

Hints:
- This agent MUST use the search_papers tool from tools.paper_rag_tool
- Define a role focused on investigation and source discovery
- Set a goal to find 8-12 relevant passages
- Write a backstory emphasizing thoroughness and not stopping at first results
"""

from dotenv import load_dotenv

load_dotenv()

from crewai import Agent
from tools.paper_rag_tool import search_papers

source_hunter = Agent(
    role="Source Hunter",
    goal=(
        "Using the search_papers tool, exhaustively search the 15-paper corpus "
        "for passages that address every sub-question and keyword provided by "
        "the Query Strategist, returning 8-12 distinct, well-attributed "
        "passages (with paper title noted) that together cover the relevant "
        "ground -- agent theory, reasoning, multi-agent systems, tool use, "
        "and planning/safety -- for the question at hand."
    ),
    backstory=(
        "You are an investigative research assistant who has read every paper "
        "in this corpus, but you never rely on memory alone -- you always "
        "verify and surface evidence through search. You learned early on that "
        "the first search result is rarely the best one: you run several "
        "variations of a query (different phrasing, narrower and broader "
        "versions, synonyms) before deciding a topic is covered. You are "
        "deliberately suspicious of stopping early, and you cross-check that "
        "your passages span multiple papers rather than over-relying on one "
        "source. For every passage you keep, you note which paper it came from "
        "so nothing gets lost on the way to the writer."
    ),
    tools=[search_papers],  # required
    verbose=True,
    memory=True,
)
