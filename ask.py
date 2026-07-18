#!/home/lalachan/linuxProject/ai-cli/venv/bin/python3
import os
import sys
import json 
import subprocess

script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, script_dir)


from groq import Groq
from config import API_KEY, MODEL
from history import save_entry, print_history, clear_history
from safety import confirm_and_run


def main():
    if len(sys.argv) < 2: 
        print("Usage: ask \"your question\"")
        sys.exit(1)

    if len(sys.argv) >= 2 and sys.argv[1] == "history":
        if len(sys.argv) == 2:
            print_history()
            return 

        elif len(sys.argv) == 3 and sys.argv[2] == "clear":
            clear_history()
            return

    question = " ".join(sys.argv[1:])
    client = Groq(api_key=API_KEY)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content":(
                "You are a Linux CLI expert. Respond ONLy a JSON object, no other text, "
                "in this exat format: "
                '{"command": "<the exact shell command>", "explanation": "<Two or three comprehensible sentences of explanation.>"}. '
                "Do not include markdown, backticks, or any text outside the JSOn object. "
                "If the question doesn't map to a single command, put your best single command anyway "
                "Do not give me extra suggested command"
            
            )},
            {"role": "user", "content": question}
        ],
        response_format = {"type": "json_object"}
    )


    raw = response.choices[0].message.content
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        parsed = json.loads(cleaned)
    
    command = parsed["command"]
    explanation = parsed["explanation"]

    save_entry(question, f"{command} - {explanation}")
    confirm_and_run(command, explanation)

if __name__ == "__main__":
    main()

