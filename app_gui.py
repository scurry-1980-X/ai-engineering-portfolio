# Version 0.5

import os
import threading
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

from dotenv import load_dotenv
from openai import OpenAI


APP_TITLE = "AI IT Support Assistant"
APP_SIZE = "850x720"
MODEL_NAME = "gpt-5-mini"

CATEGORIES = [
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

DISCLAIMER_TEXT = (
    "Disclaimer: AI-generated troubleshooting suggestions should be reviewed "
    "by a qualified technician before being applied in a production environment."
)


def load_client():
    """Load the OpenAI API key and return an OpenAI client."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY was not found. Check your .env file.")

    return OpenAI(api_key=api_key)


def build_category_list():
    """Format the approved category list for the prompt."""
    return "\n".join(f"- {category}" for category in CATEGORIES)


def build_prompt(problem):
    """Build the AI troubleshooting prompt."""
    category_list = build_category_list()

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
""".strip()


def analyze_problem(client, problem):
    """Send the user issue to OpenAI and return the AI analysis."""
    response = client.responses.create(
        model=MODEL_NAME,
        input=build_prompt(problem),
    )

    return response.output_text


class TroubleshootingApp:
    """Desktop GUI for the AI IT Support Assistant."""

    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(APP_SIZE)

        self.client = None
        self.problem_input = None
        self.result_output = None
        self.analyze_button = None

        self.create_widgets()

    def create_widgets(self):
        """Create the full GUI layout."""
        self.create_title_section()
        self.create_problem_section()
        self.create_button_section()
        self.create_result_section()

    def create_title_section(self):
        """Create the title, subtitle, and disclaimer."""
        title_label = tk.Label(
            self.root,
            text=APP_TITLE,
            font=("Arial", 22, "bold"),
        )
        title_label.pack(pady=(15, 5))

        subtitle_label = tk.Label(
            self.root,
            text="Classify IT issues, suggest troubleshooting steps, and provide escalation guidance.",
            font=("Arial", 11),
        )
        subtitle_label.pack(pady=(0, 8))

        disclaimer_label = tk.Label(
            self.root,
            text=DISCLAIMER_TEXT,
            font=("Arial", 10, "italic"),
            wraplength=760,
            justify="center",
        )
        disclaimer_label.pack(pady=(0, 12))

    def create_problem_section(self):
        """Create the issue input area."""
        problem_label = tk.Label(
            self.root,
            text="Describe the IT issue:",
            font=("Arial", 12, "bold"),
        )
        problem_label.pack(anchor="w", padx=20)

        self.problem_input = scrolledtext.ScrolledText(
            self.root,
            height=7,
            wrap=tk.WORD,
            font=("Arial", 11),
        )
        self.problem_input.pack(fill="x", padx=20, pady=(5, 10))

    def create_button_section(self):
        """Create the Analyze, Clear, and Save buttons."""
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        self.analyze_button = tk.Button(
            button_frame,
            text="Analyze Issue",
            command=self.handle_analyze,
            font=("Arial", 12, "bold"),
            width=16,
            height=2,
        )
        self.analyze_button.grid(row=0, column=0, padx=5)

        clear_button = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_fields,
            font=("Arial", 12),
            width=16,
            height=2,
        )
        clear_button.grid(row=0, column=1, padx=5)

        save_button = tk.Button(
            button_frame,
            text="Save Analysis",
            command=self.save_analysis,
            font=("Arial", 12),
            width=16,
            height=2,
        )
        save_button.grid(row=0, column=2, padx=5)

    def create_result_section(self):
        """Create the AI analysis output area."""
        result_label = tk.Label(
            self.root,
            text="AI Analysis:",
            font=("Arial", 12, "bold"),
        )
        result_label.pack(anchor="w", padx=20, pady=(10, 0))

        self.result_output = scrolledtext.ScrolledText(
            self.root,
            height=22,
            wrap=tk.WORD,
            font=("Arial", 11),
        )
        self.result_output.pack(fill="both", expand=True, padx=20, pady=(5, 20))

    def handle_analyze(self):
        """Start analysis in a background thread so the GUI stays responsive."""
        problem = self.get_problem_text()

        if not problem:
            messagebox.showwarning(
                "Missing Information",
                "Please describe the IT problem before analyzing.",
            )
            return

        self.set_result_text("Analyzing issue...")
        self.set_analyze_button_state(tk.DISABLED)

        worker = threading.Thread(
            target=self.run_analysis,
            args=(problem,),
            daemon=True,
        )
        worker.start()

    def run_analysis(self, problem):
        """Run the OpenAI request outside the main GUI thread."""
        try:
            if self.client is None:
                self.client = load_client()

            analysis = analyze_problem(self.client, problem)
            self.root.after(0, self.set_result_text, analysis)

        except Exception as error:
            error_message = f"An error occurred:\n\n{error}"
            self.root.after(0, self.set_result_text, error_message)

        finally:
            self.root.after(0, self.set_analyze_button_state, tk.NORMAL)

    def clear_fields(self):
        """Clear both the input and output boxes."""
        self.problem_input.delete("1.0", tk.END)
        self.result_output.delete("1.0", tk.END)

    def save_analysis(self):
        """Save the current issue and AI analysis to a text file."""
        problem = self.get_problem_text()
        analysis = self.get_result_text()

        if not analysis:
            messagebox.showwarning(
                "No Analysis to Save",
                "Please analyze an issue before saving.",
            )
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt"),
                ("All Files", "*.*"),
            ],
            title="Save Analysis",
        )

        if not file_path:
            return

        try:
            self.write_analysis_file(file_path, problem, analysis)
            messagebox.showinfo(
                "Analysis Saved",
                "The analysis was saved successfully.",
            )

        except Exception as error:
            messagebox.showerror(
                "Save Failed",
                f"The analysis could not be saved:\n\n{error}",
            )

    def write_analysis_file(self, file_path, problem, analysis):
        """Write the issue and AI analysis to a text file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(file_path, "w", encoding="utf-8") as file:
            file.write("AI IT Support Assistant Analysis\n")
            file.write("================================\n\n")
            file.write(f"Timestamp: {timestamp}\n\n")
            file.write(f"{DISCLAIMER_TEXT}\n\n")
            file.write("User Issue:\n")
            file.write(problem)
            file.write("\n\nAI Analysis:\n")
            file.write(analysis)

    def get_problem_text(self):
        """Return the text from the problem input box."""
        return self.problem_input.get("1.0", tk.END).strip()

    def get_result_text(self):
        """Return the text from the result output box."""
        return self.result_output.get("1.0", tk.END).strip()

    def set_result_text(self, text):
        """Replace the result output text."""
        self.result_output.delete("1.0", tk.END)
        self.result_output.insert(tk.END, text)

    def set_analyze_button_state(self, state):
        """Enable or disable the Analyze button."""
        self.analyze_button.config(state=state)


def main():
    """Run the desktop application."""
    root = tk.Tk()
    TroubleshootingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
