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

    # 1. Original user message
    messages = [
        {
            "role": "user",
            "content": "Get the details for customer C001"
        }
    ]

    # 2. First call to Claude
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )

    print("Stop reason:", response.stop_reason)
    print("Response:", response)

    # 3. Check whether Claude wants to use a tool
    if response.stop_reason == "tool_use":

        for block in response.content:

            if block.type == "tool_use":

                print("Tool name:", block.name)
                print("Tool input:", block.input)

                # 4. Execute the requested tool
                if block.name == "get_customer":

                    result = get_customer(**block.input)

                    print("Tool result:", result)

                    # 5. Add Claude's tool-use response
                    # to the conversation history
                    messages.append(
                        {
                            "role": "assistant",
                            "content": response.content
                        }
                    )

                    # 6. Add the tool result
                    # back to Claude
                    messages.append(
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
                    )

        # 7. Send the updated message history
        # back to Claude
        final_response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )

        # 8. Final Claude response
        print("Final response:", final_response.content[0].text)


if __name__ == "__main__":
    main()