#!/home/lalachan/linuxProject/ai-cli/venv/bin/python3
import os
import sys

script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, script_dir)

from groq import Groq
from config import API_KEY, MODEL
from history import save_entry, print_history

def main():
    if len(sys.argv) < 2:
        print("Usage: ask \"your question\"")
        sys.exit(1)

    if len(sys.argv) == 2 and sys.argv[1] == "history":
        print_history()
        return

    question = " ".join(sys.argv[1:])
    client = Groq(api_key=API_KEY)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a Linux CLI expert. Give the exact command and a one-line explanation. Do not execute anything, only explain."},
            {"role": "user", "content": question}
        ]
    )
    answer = response.choices[0].message.content
    print(answer)
    save_entry(question,answer)

if __name__ == "__main__":
    main()