"""ai.py - ALL provider-specific (Gemini) code lives in this file.

If you ever switch to another AI provider, only this file changes.
"""
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()  # reads GEMINI_API_KEY from the .env file

# Model names change over time: check https://ai.google.dev for the current one.
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

SYSTEM_PROMPT = (
    "You are a friendly, helpful assistant inside a small chatbot app. "
    "Keep answers clear and concise, and ask a short question if the "
    "user's request is unclear."
)

_client = None


def get_client():
    """Create the Gemini client once (it reads GEMINI_API_KEY automatically)."""
    global _client
    if _client is None:
        if not os.getenv("GEMINI_API_KEY"):
            raise RuntimeError(
                "GEMINI_API_KEY not found. Add it to your .env file."
            )
        _client = genai.Client()
    return _client


# ---------- Single question (no memory) ----------
def ask_ai(prompt):
    response = get_client().models.generate_content(model=MODEL, contents=prompt)
    return response.text


# ---------- Chatbot (remembers the conversation) ----------
def new_chat():
    """Start a new conversation. The chat object stores the history for you."""
    return get_client().chats.create(
        model=MODEL,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    )


def chat_ai(chat, message):
    response = chat.send_message(message)
    return response.text


# ---------- Error handling with retries ----------
def ask_ai_safe(prompt, retries=3):
    for attempt in range(retries):
        try:
            return ask_ai(prompt)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2 ** attempt)  # wait 1s, 2s, 4s
    return "Sorry, the AI service is not available right now."


def chat_ai_safe(chat, message, retries=3):
    for attempt in range(retries):
        try:
            return chat_ai(chat, message)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2 ** attempt)
    return "Sorry, the AI service is not available right now."


if __name__ == "__main__":
    # Quick test: run `python ai.py`
    print(ask_ai_safe("Explain what an API is in two simple sentences."))
