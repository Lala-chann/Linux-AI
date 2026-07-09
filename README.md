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
├── ask.py              # Main script — entry point. Parses the question,
│                        # calls the Groq API, prints the answer.
├── config.py            # Loads GROQ_API_KEY and model name from .env
│                        # via python-dotenv. Fails loudly if the key is missing.
├── requirements.txt      # Pinned dependency versions (groq, python-dotenv, etc.)
├── .gitignore            # Excludes .env, venv/, __pycache__/, and other
│                        # machine-specific or secret files from git.
├── .env                  # Your actual API key. Never committed — gitignored.
├── .env.example           # Template showing what .env should contain.
└── README.md
```

**Why the split between `ask.py` and `config.py`:** keeping API-key/config loading separate from the main logic means the key-handling code (and its failure behavior) is isolated and easy to audit on its own, rather than mixed into the request logic.

---

## How it works (brief)

1. `ask.py` joins your CLI arguments into a single question string.
2. It sends that question to Groq's chat completion endpoint, with a system prompt instructing the model to act as a Linux CLI expert and explain commands rather than execute them.
3. The model's text response is printed directly to the terminal.

No conversation state is kept between runs — each question is currently independent (see Upcoming Features).

---

## Known Limitations (current version)

- No conversation memory — can't currently ask a follow-up like "now undo that" and have it retain context.
- Response format is inconsistent — sometimes returns one command, sometimes a list of several options, depending on how the model interprets the question.
- Markdown formatting (`**bold**`) from the model isn't stripped, so raw asterisks may appear in terminal output.
- No handling yet for network failures, rate limiting, or invalid/expired API keys — the script will just raise whatever error the underlying library throws.
- Not currently packaged for `pip install`; setup is manual (see Setup above).

---

## Upcoming Features

- [ ] **Conversation history** — remember previous questions/answers in a session so follow-up questions work (e.g., "now undo that").
- [ ] **Consistent response format** — enforce single best-answer output by default, with an optional flag (e.g. `--options`) for multiple alternatives.
- [ ] **Plain-text output enforcement** — instruct the model to avoid markdown syntax so output renders cleanly in a terminal.
- [ ] **Error handling** — graceful messages for no internet connection, API rate limits, and invalid API keys instead of raw stack traces.
- [ ] **Optional safe-execution mode** — with an explicit `y/n` confirmation prompt and a blocklist for destructive patterns (`rm -rf /`, `dd`, `mkfs`, etc.) before ever running a suggested command. Off by default.
- [ ] **Config file support** — let users choose model, temperature, and max tokens without editing source code.
- [ ] **Logging** — optional local log of questions and answers for reference.
- [ ] **Packaging** — proper installable package (`pip install .`) instead of manual symlinking.

---

## Contributing / Notes for future self

If you're picking this project back up later: check `.gitignore` staging state and confirm `.env` never appears in `git status` before any commit or push — this project has previously hit issues where staged files were stale after mid-development fixes.

## License

Not yet specified.