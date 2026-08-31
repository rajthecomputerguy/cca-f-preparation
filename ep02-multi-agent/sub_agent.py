import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"]
)


def run_sub_agent(task):
    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": task
            }
        ]
    )

    return message.content[0].text

def research_agent(task):
    return run_sub_agent(
        f"""
You are the Research Sub-Agent.

Your responsibility is only research and information gathering.

Task:
{task}
"""
    )


def analysis_agent(task):
    return run_sub_agent(
        f"""
You are the Analysis Sub-Agent.

Your responsibility is only analysis of the given task.

Task:
{task}
"""
    )