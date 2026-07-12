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
 
## Setup
 
1. Clone the repo:
```bash
   git clone https://github.com/yourusername/ai-cli.git
   cd ai-cli
```
 
2. Create and activate a virtual environment:
```bash
   python3 -m venv venv
   source venv/bin/activate
```
 
3. Install dependencies:
```bash
   pip install -r requirements.txt
```
 
4. Set up your API key:
```bash
   cp .env.example .env
```
   Then open `.env` and add your key:
```
   GROQ_API_KEY=your_key_here
```
 
5. Run it:
```bash
   python3 ask.py "how do I list files"
```
 
### Optional: make it a global command
So you can run `ask "..."` from any directory, not just inside the project folder:
 
```bash
sudo ln -s "$(pwd)/ask.py" /usr/local/bin/ask
```
 
**Important:** this only works if `ask.py`'s shebang line points to your venv's actual Python interpreter (not system Python), since the venv is what has `groq` and `python-dotenv` installed. Edit the first line of `ask.py` to match your own path:
```
#!/absolute/path/to/ai-cli/venv/bin/python3
```
 
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
 
**Why the split between `ask.py` and `config.py`:** keeping API-key/config loading separate from the main logic means the key-handling code (and its failure behavior) is isolated and easy to audit on its own, rather than mixed into the request logic.
 
---
 
## How it works (brief)
 
1. `ask.py` joins your CLI arguments into a single question string.
2. If that argument is exactly `history`, it prints your saved question/answer log instead of calling the API.
3. Otherwise, it sends the question to Groq's chat completion endpoint, with a system prompt instructing the model to act as a Linux CLI expert and explain commands rather than execute them.
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
1. [2026-07-12T10:15:00]
   Q: how do I list files
   A: Use ls -l to list files with details.
----------------------------------------
2. [2026-07-12T10:16:30]
   Q: how can I use chmod with numbers
   A: chmod 755 file sets owner to read/write/execute, group and others to read/execute.
----------------------------------------
```
 
### Where history is stored
 
History is saved to `history/history.jsonl` inside the project folder, one JSON entry per line. This file is excluded from git (see `.gitignore`) — it stays local to your machine and is never pushed to GitHub.
 
**Note:** because history lives inside the project folder rather than your home directory, it will not carry over if you move or re-clone the project onto another machine. This is a deliberate tradeoff for this project, not an oversight.
 
### Format reference
 
See `history/history_example.txt` in this repo for a sample of what a `history.jsonl` entry looks like, without needing to run the tool first.
 
### Limitation
 
`ask history` only *displays* past questions and answers — it does not feed that context back into future questions. Asking a follow-up like "now undo that" will not currently work, since each `ask` call is still independent. True conversational memory is a separate planned feature (see below).
 
---
 
## Known Limitations (current version)
 
- No conversation memory — can't currently ask a follow-up like "now undo that" and have it retain context from prior questions.
- Response format is inconsistent — sometimes returns one command, sometimes a list of several options, depending on how the model interprets the question.
- Markdown formatting (`**bold**`) from the model isn't stripped, so raw asterisks may appear in terminal output.
- No handling yet for network failures, rate limiting, or invalid/expired API keys — the script will just raise whatever error the underlying library throws.
- `history/history.jsonl` grows indefinitely with no size limit or trimming.
- Not currently packaged for `pip install`; setup is manual (see Setup above).
---
 
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