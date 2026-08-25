import os

import anthropic
from dotenv import load_dotenv

from tools import get_customer


load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

tools = [
    {
        "name": "get_customer",
        "description": "Get customer details and verification status using customer ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer ID"
                }
            },
            "required": ["customer_id"]
        }
    }
]


def main():
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        tools=tools,
        messages=[
            {
                "role": "user",
                "content": "Get the details for customer C001"
            }
        ]
    )

    print("Stop reason:", response.stop_reason)
    print("Response:", response)
    if response.stop_reason == "tool_use":
     for block in response.content:
        if block.type == "tool_use":
            print("Tool name:", block.name)
            print("Tool input:", block.input)

            if block.name == "get_customer":
                result = get_customer(**block.input)
                print("Tool result:", result)

    if block.name == "get_customer":
      result = get_customer(**block.input)

    messages = [
        {
            "role": "user",
            "content": "Get the details for customer C001"
        },
        {
            "role": "assistant",
            "content": response.content
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result)
                }
            ]
        }
    ]


if __name__ == "__main__":
    main()