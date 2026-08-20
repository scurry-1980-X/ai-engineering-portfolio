# Version 0.3

import os
from dotenv import load_dotenv
from openai import OpenAI


def load_client():
    """Load environment variables and create the OpenAI client."""
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY was not found. Check your .env file.")

    return OpenAI(api_key=api_key)


def get_categories():
    """Return the approved IT support categories."""
    return [
        "Network",
        "Endpoint / Hardware",
        "Windows / Operating System",
        "Email / Outlook",
        "Microsoft 365",
        "Identity & Access",
        "Applications / Software",
        "Security",
        "Printers & Peripherals",
        "File & Storage",
        "Performance",
        "General IT Support",
    ]


def build_prompt(problem, categories):
    """Build the AI prompt using the user's problem and approved categories."""
    category_list = "\n".join(f"- {category}" for category in categories)

    return f"""
You are an AI IT troubleshooting assistant.

Analyze the user's issue and select the single best category
from the approved categories below.

Approved categories:
{category_list}

User issue:
{problem}

Respond using exactly this format:

Category:
<choose one category from the approved list>

Subcategory:
<short subcategory such as Credentials, DNS, MFA, Hardware Failure, Performance, Phishing, etc.>

Priority:
<Low, Medium, High, or Critical>

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


def analyze_problem(client, prompt):
    """Send the prompt to OpenAI and return the AI response text."""
    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
    )

    return response.output_text


def main():
    """Run the AI IT Support Assistant."""
    client = load_client()
    categories = get_categories()

    print("AI IT Support Assistant")
    print("-----------------------")

    problem = input("Describe your IT problem: ").strip()

    if not problem:
        print("No problem entered. Please run the app again and describe the issue.")
        return

    prompt = build_prompt(problem, categories)
    analysis = analyze_problem(client, prompt)

    print("\nAI Analysis:")
    print(analysis)


if __name__ == "__main__":
    main()