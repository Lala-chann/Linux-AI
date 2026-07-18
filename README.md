# AI-Powered Linux CLI Assistant
 
A command-line tool that answers Linux/CLI questions using an LLM (via the [Groq API](https://groq.com)). Ask a question in plain English, get back the exact command and a short explanation — no execution, just answers.
 
```bash
$ ask "what is the CLI for deleting a file"
The CLI command for deleting a file is:
rm filename
Explanation: The rm command removes a file from the system, where filename is the name of the file you want to delete.
```
 
**Note:** this tool only explains commands. It never executes anything on your system — you decide what to run.
 
---
 
## Requirements
 
- Python 3.10+
- A [Groq API key](https://console.groq.com) (free tier available)
- Linux (developed and tested on Ubuntu)
---

 
## Project Structure
 
```
ai-cli/
├── ask.py                     # Main script — entry point. Parses the question,
│                               # calls the Groq API, prints the answer, and
│                               # routes `ask history` to the history viewer.
├── config.py                  # Loads GROQ_API_KEY and model name from .env
│                               # via python-dotenv. Also defines HISTORY_FILE.
│                               # Fails loudly if the API key is missing.
├── history.py                  # Saves and loads question/answer history
│                               # (history/history.jsonl).
├── history/
│   ├── history.jsonl            # Actual history log. Gitignored — local only.
│   └── history_example.txt       # Sample format, safe to commit, no real data.
├── requirements.txt             # Pinned dependency versions (groq, python-dotenv, etc.)
├── .gitignore                    # Excludes .env, venv/, __pycache__/,
│                               # history/history.jsonl, and other
│                               # machine-specific or secret files from git.
├── .env                          # Your actual API key. Never committed — gitignored.
├── .env.example                   # Template showing what .env should contain.
└── README.md
```

---
 
## How it works (brief)
 
1. `ask.py` joins your CLI arguments into a single question string.
2. If that argument is exactly `history`, it prints your saved question/answer log instead of calling the API.
3. By default, every command and its explanation is automatically recorded in history. Over time, this can make the history cluttered and hard to read. Use `ask history clean` to clear your history whenever you no longer need it.
4. The model's text response is printed to the terminal and appended to `history/history.jsonl`.
No conversation state is fed back into future questions — each question is still answered independently (see "Upcoming Features").
 
---
 
## History
 
Every question and answer is automatically logged. To view your past conversations:
 
```bash
ask history
```
 
Output looks like:
```
1. Q: how do I list files
   A: Use ls -l to list files with details.
   
----------------------------------------
2. Q: how can I use chmod with numbers
   A: chmod 755 file sets owner to read/write/execute, group and others to read/execute.

----------------------------------------
```
 
**Note:** Detailed information about history is available in `history/history.txt`.

## Upcoming Features
 
- [ ] **Conversation memory** — feed previous exchanges back to the model as context so follow-up questions like "now undo that" work correctly. (Distinct from the History feature above, which only logs and displays — it doesn't influence future answers.)
- [ ] **Consistent response format** — enforce single best-answer output by default, with an optional flag (e.g. `--options`) for multiple alternatives.
- [ ] **Plain-text output enforcement** — instruct the model to avoid markdown syntax so output renders cleanly in a terminal.
- [ ] **Error handling** — graceful messages for no internet connection, API rate limits, and invalid API keys instead of raw stack traces.
- [ ] **Optional safe-execution mode** — with an explicit `y/n` confirmation prompt and a blocklist for destructive patterns (`rm -rf /`, `dd`, `mkfs`, etc.) before ever running a suggested command. Off by default.
- [ ] **Config file support** — let users choose model, temperature, and max tokens without editing source code.
- [ ] **History size limit** — cap or rotate `history.jsonl` so it doesn't grow unbounded.
- [ ] **Packaging** — proper installable package (`pip install .`) instead of manual symlinking.
---
 
## License
 
Not yet specified.