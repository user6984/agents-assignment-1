"""
Task Definitions for Research Crew

TODO: Define the four sequential tasks:
1. Query Expansion - Break down the research question
2. Source Hunting - Search the paper corpus
3. Synthesis - Analyze and synthesize findings
4. Report Writing - Generate the literature review

Each task should:
- Have a clear description telling the agent what to do
- Specify the agent responsible
- Define expected_output format
- Use context parameter to pass information between tasks
"""

from agents import query_expander, report_writer, source_hunter, synthesizer
from crewai import Task


def create_research_tasks(research_question: str) -> list[Task]:
    """
    Create the task pipeline for a research question.

    Args:
        research_question: The user's research question

    Returns:
        List of 4 tasks in execution order
    """

    # =========================================
    # Task 1: Query Expansion
    # =========================================
    expand_task = Task(
        description=(
            f"Analyze the following research question and break it into a "
            f'search strategy: "{research_question}"\n\n'
            "Produce:\n"
            "1. 4-6 specific sub-questions that together cover the different "
            "angles of the research question (e.g., theoretical definitions, "
            "architectural approaches, empirical comparisons, open challenges).\n"
            "2. For each sub-question, list 2-4 keyword/phrase variants "
            "(including synonyms and alternative terminology used in the "
            "agentic AI literature, e.g., 'tool use' vs 'function calling').\n"
            "3. Note which of the corpus's five topic areas (agent theory, "
            "reasoning, multi-agent systems, tool use/RAG, planning/safety) "
            "each sub-question most likely touches.\n\n"
            "Do not search anything yourself -- you are only planning the "
            "search strategy for the next agent to execute."
        ),
        agent=query_expander,
        expected_output=(
            "A structured list of 4-6 sub-questions, each with its associated "
            "keyword variants and likely topic area(s), formatted as a "
            "numbered list ready for another agent to execute as searches."
        ),
    )

    # =========================================
    # Task 2: Source Hunting
    # =========================================
    search_task = Task(
        description=(
            "Using the search_papers tool, search the corpus for every "
            "sub-question and keyword variant produced in the previous task. "
            "You MUST issue at least 6 separate search_papers calls with "
            "different queries -- do not stop after 1-2 searches even if the "
            "first results look relevant. Use k=8 on each call so you have a "
            "wide pool of candidates to choose from.\n\n"
            "After each search, track which paper(s) the results came from. "
            "Before finishing, check your running list of passages: if 4 or "
            "more of them come from the same single paper, you have NOT "
            "searched broadly enough -- run additional searches using "
            "different keywords or phrasing aimed specifically at other papers "
            "in the corpus. The corpus includes Wooldridge, Wang/Xi surveys, "
            "ReAct, Chain-of-Thought, Tree of Thoughts, Reflexion, CAMEL, "
            "Generative Agents, AutoGen, Toolformer, RAG (2020 and 2023 "
            "survey), Planning Abilities, and Constitutional AI -- if any of "
            "these are clearly relevant to the question and you haven't found "
            "them yet, search for them by name.\n\n"
            "Stop only once you have 8-12 non-redundant passages drawn from at "
            "least 6 different papers."
        ),
        agent=source_hunter,
        context=[expand_task],
        expected_output=(
            "A list of 8-12 passages, each labeled with its source paper, the "
            "sub-question it answers, and a short summary of its relevant "
            "content. The passages must be drawn from at least 6 different "
            "papers -- if your draft list has 4+ passages from a single paper, "
            "you have not searched broadly enough and must search again before "
            "finalizing."
        ),
    )

    # =========================================
    # Task 3: Synthesis
    # =========================================
    synthesis_task = Task(
        description=(
            "Review all the passages gathered by the Source Hunter in light "
            f'of the original research question: "{research_question}"\n\n'
            "Identify:\n"
            "1. 3-5 cross-cutting themes that organize the findings (not "
            "one theme per paper -- themes should group ideas across "
            "multiple papers).\n"
            "2. Points of clear agreement or consensus between sources.\n"
            "3. Explicit contradictions, tensions, or unresolved debates "
            "between sources.\n"
            "4. Gaps -- aspects of the research question that the corpus "
            "does not address well.\n\n"
            "Do not simply restate or summarize each paper one by one -- "
            "your value is in the connections and contrasts you draw across "
            "sources."
        ),
        agent=synthesizer,
        context=[expand_task, search_task],
        expected_output=(
            "A structured analysis organized under four headers -- Themes, "
            "Consensus, Debates/Contradictions, and Gaps -- with each point "
            "explicitly tied to the specific source paper(s) that support it."
        ),
    )

    # =========================================
    # Task 4: Report Writing
    # =========================================
    report_task = Task(
        description=(
            f"Write a complete literature review answering: "
            f'"{research_question}"\n\n'
            "Using the synthesis and source material from the previous "
            "tasks, produce a markdown document with exactly these sections:\n"
            "1. Executive Summary -- 3-4 sentences answering the question "
            "directly.\n"
            "2. Introduction -- context and why the question matters.\n"
            "3. Methodology -- briefly note this review draws on a curated "
            "15-paper corpus searched via RAG.\n"
            "4. Findings -- organized by the themes identified in the "
            "synthesis, not paper-by-paper.\n"
            "5. Discussion -- interpret the findings, note debates and gaps.\n"
            "6. Conclusion -- direct answer plus open questions.\n"
            "7. References -- list every paper actually cited in the body, in the "
            "format 'Lead-Author et al. (Year). Title. [paper_id]', using only the "
            "paper_id and paper_title fields returned by the search tool.\n\n"
            "Every substantive claim must cite the specific paper it comes "
            "Every substantive claim must cite its source paper using the exact "
            "paper_id returned by the search tool (e.g., 'wooldridge_1995', "
            "'xi_2023_survey') -- NOT invented author names or formatted citations. "
            "Many papers in this corpus have 10+ co-authors that you do not have "
            "full access to, so never write out specific multi-author citations "
            "like 'Xi & Wang (2023)' -- you cannot verify these and risk merging "
            "authors from two different papers. Use the format 'Lead-Author et al. "
            "(Year) [paper_id]' for readability, where Lead-Author is taken only "
            "from the paper_id slug itself (e.g., paper_id 'wang_2023_survey' -> "
            "'Wang et al. (2023) [wang_2023_survey]'), never from invented "
            "co-author lists."
            "from (e.g., '(Yao et al., ReAct)'). Do not invent or include "
            "claims that are not grounded in the passages gathered earlier. "
            "Before finalizing, cross-check your References section against "
            "the body text: remove any paper that is listed in References but "
            "never actually cited anywhere in the Findings or Discussion."
        ),
        agent=report_writer,
        context=[expand_task, search_task, synthesis_task],
        expected_output=(
            "A complete markdown literature review with all seven sections "
            "listed above, properly attributed citations throughout, and a "
            "References section listing only papers actually cited in the body."
        ),
    )

    return [expand_task, search_task, synthesis_task, report_task]
