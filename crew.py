"""
Research Crew Configuration

TODO: Configure and run the Research & Report Crew.

This module should:
1. Import your agents from the agents module
2. Create tasks using create_research_tasks()
3. Configure a Crew with sequential process
4. Provide a run_research() function to execute the crew
"""

# Load environment variables BEFORE importing crewai
from dotenv import load_dotenv

load_dotenv()

from agents import query_expander, report_writer, source_hunter, synthesizer
from crewai import Crew, Process
from tasks.task_definitions import create_research_tasks


def create_research_crew(research_question: str) -> Crew:
    """
    Create a Research Crew configured for the given question.

    Args:
        research_question: The research question to investigate

    Returns:
        Configured Crew ready to execute
    """
    tasks = create_research_tasks(research_question)

    crew = Crew(
        agents=[query_expander, source_hunter, synthesizer, report_writer],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
        memory=True,
    )
    return crew


def run_research(research_question: str) -> str:
    """
    Execute the research crew and return the final report.

    Args:
        research_question: The research question to investigate

    Returns:
        The final literature review as a string
    """
    crew = create_research_crew(research_question)
    result = crew.kickoff()
    return str(result)


# Allow running crew.py directly for testing
if __name__ == "__main__":
    test_question = (
        "What are the main approaches to building AI agents that can reason and act?"
    )
    print(f"Testing crew with question: {test_question}\n")
    result = run_research(test_question)
    print("\n" + "=" * 50)
    print("FINAL REPORT:")
    print("=" * 50)
    print(result)
