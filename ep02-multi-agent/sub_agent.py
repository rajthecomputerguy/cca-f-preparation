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


def run_sub_agent(prompt):

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )

    if response.stop_reason == "tool_use":

        for block in response.content:

            if block.type == "tool_use":

                if block.name == "get_customer":

                    result = get_customer(**block.input)

                    messages.append({
                        "role": "assistant",
                        "content": response.content
                    })

                    messages.append({
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": str(result)
                            }
                        ]
                    })

        final_response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )

        return final_response.content[0].text

    return response.content[0].text