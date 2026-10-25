# My AI Chatbot (Gemini + Streamlit)

A small chatbot that remembers the conversation, built for the Verstech AI Automation / GenAI internship.

## Setup

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
```

1. Get a free API key at https://aistudio.google.com/apikey
2. Copy `.env.example` to `.env` and paste your key.
3. Test the connection: `python ai.py`
4. Run the app: `streamlit run app.py`

## Files

| File | Purpose |
|------|---------|
| `ai.py` | All Gemini code: single question, chat with memory, retry/error handling |
| `app.py` | Streamlit chat interface |
| `.env` | Your secret key (never commit it) |
| `.gitignore` | Keeps `.env` out of Git |

## How it works

User types a message -> `app.py` calls `chat_ai_safe()` -> `ai.py` sends it to Gemini with the conversation history -> reply is shown in the chat.