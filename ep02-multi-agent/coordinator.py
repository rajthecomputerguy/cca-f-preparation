import anthropic
import os
from dotenv import load_dotenv
from sub_agent import run_sub_agent

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"]
)

result = run_sub_agent(
    "Explain what a multi-agent system is in one sentence."
)

print("Sub-agent result:")
print(result)

