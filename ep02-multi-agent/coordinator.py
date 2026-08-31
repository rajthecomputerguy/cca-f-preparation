import anthropic
import os
import asyncio
from dotenv import load_dotenv

from sub_agent import run_sub_agent, research_agent, analysis_agent


load_dotenv()


client = anthropic.Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"]
)


async def run_research():
    return research_agent(
        "What is a multi-agent system?"
    )


async def run_analysis():
    return analysis_agent(
        "Why use specialized sub-agents?"
    )


async def main():

    research_result, analysis_result = await asyncio.gather(
        run_research(),
        run_analysis()
    )

    synthesis_prompt = f"""
You are the Coordinator.

Combine the following outputs from two specialized sub-agents
into one concise final answer.

Research Agent:
{research_result}

Analysis Agent:
{analysis_result}

Provide a clear final answer about:

Why use a multi-agent system with specialized sub-agents?
"""

    final_result = run_sub_agent(synthesis_prompt)

    print("\nResearch Agent:")
    print(research_result)

    print("\nAnalysis Agent:")
    print(analysis_result)

    print("\nFinal Coordinator Result:")
    print(final_result)


asyncio.run(main())