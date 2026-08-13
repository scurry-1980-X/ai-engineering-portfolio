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

Analyze this user-reported problem:

{problem}

Respond using exactly this format:

Category:
<one concise category>

Likely Cause:
<one or two concise likely causes>

Troubleshooting Steps:
1. <step>
2. <step>
3. <step>
4. <step>
5. <step>

Escalation Guidance:
<when or why this issue should be escalated>

Keep the response concise, practical, and suitable for a technical support engineer.
"""
)

print("\nAI Analysis:")
print(response.output_text)