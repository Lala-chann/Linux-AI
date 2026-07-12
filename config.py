import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("GROQ_API_KEY")
MODEL = "llama-3.1-8b-instant"

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
HISTORY_FILE = os.path.join(PROJECT_ROOT, "history", "history.jsonl")

if not API_KEY:
    raise ValueError(
        "GROQ_API_KEY not set. Add it to your .env file or run: export GROQ_API_KEY='your_key'"
    )