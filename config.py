import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("GROQ_API_KEY")
MODEL = "llama-3.1-8b-instant"

if not API_KEY:
    raise ValueError(
        "GROQ_API_KEY not set. Add it to your .env file or run: export GROQ_API_KEY='your_key'"
    )