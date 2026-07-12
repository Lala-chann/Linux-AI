import json
import os
from config import HISTORY_FILE

def save_entry(question, answer):
    """Append one Q&A pair to the history file as a Json line"""
    entry = {
        "question": question,
        "answer": answer,
    }
    with open(HISTORY_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

def load_entries():
    """Read all history entires. Return an empty list if the file does not exist yet."""
    if not os.path.exists(HISTORY_FILE):
        return []
    
    entries = []
    with open(HISTORY_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries

def print_history():
    entries = load_entries()
    if not entries:
        print("No history yet.")
        return
    
    for i, entry in enumerate(entries, start=1):
        print(f"{i}. Q: [{entry['question']}]")
        print(f"   A: [{entry['answer']}]")
        print("=" * 70)


