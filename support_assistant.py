# Version 0.2

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("AI IT Support Assistant")
print("-----------------------")

problem = input("Describe your IT problem: ")

response = client.responses.create(
    model="gpt-5-mini",
    input=f"""
You are an IT troubleshooting assistant.

Analyze the following user-reported problem:

{problem}

Return:
1. Category
2. Likely cause
3. Troubleshooting steps
4. Escalation guidance

Keep the response concise and practical.
"""
)

print("\nAI Analysis:")
print(response.output_text)