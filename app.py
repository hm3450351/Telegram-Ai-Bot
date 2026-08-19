"""
Telegram AI Bot — powered by Groq (free, open-source LLMs like Llama).
Runs as a Vercel serverless function via FastAPI.

Required environment variables:
  TELEGRAM_BOT_TOKEN   - from @BotFather on Telegram
  GROQ_API_KEY         - from console.groq.com (free, no credit card)

Optional:
  GROQ_MODEL           - defaults to "llama-3.3-70b-versatile"
  WEBHOOK_SECRET        - random string to verify requests really come from Telegram
"""

import os
import requests
from fastapi import FastAPI, Request, Response

app = FastAPI()

# --- Configuration ---
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET")  # optional but recommended

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = (
    "أنت مساعد ذكاء اصطناعي مفيد وودود داخل بوت تيليجرام. "
    "جاوب بإيجاز ووضوح، وبنفس لغة رسالة المستخدم."
)


def ask_ai(user_message: str) -> str:
    """Send the user's message to Groq's free API and return the model's reply."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        "temperature": 0.7,
        "max_tokens": 1024,
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=25)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def send_telegram_message(chat_id: int, text: str) -> None:
    """Send a text message back to the user via the Telegram Bot API."""
    max_len = 4000  # stay under Telegram's 4096-character limit
    if len(text) > max_len:
        text = text[:max_len] + "…"
    requests.post(
        f"{TELEGRAM_API_URL}/sendMessage",
        json={"chat_id": chat_id, "text": text},
        timeout=10,
    )


@app.get("/")
def health_check():
    """Visit this in a browser to confirm the deployment is live."""
    return {"status": "ok", "bot": "telegram-ai-bot"}


@app.post("/api/webhook")
async def telegram_webhook(request: Request):
    # Optional: reject requests that don't carry Telegram's secret token
    if WEBHOOK_SECRET:
        secret_header = request.headers.get("x-telegram-bot-api-secret-token")
        if secret_header != WEBHOOK_SECRET:
            return Response(status_code=403)

    update = await request.json()
    message = update.get("message") or update.get("edited_message")

    if not message:
        return {"ok": True}

    chat_id = message["chat"]["id"]
    text = (message.get("text") or "").strip()

    if not text:
        return {"ok": True}  # ignore stickers, photos, etc. for now

    if text in ("/start", "/help"):
        send_telegram_message(
            chat_id,
            "أهلاً 👋 أنا بوت ذكاء اصطناعي. اسألني أي شي وبجاوبك!",
        )
        return {"ok": True}

    try:
        reply = ask_ai(text)
    except Exception:
        reply = "صار خطأ بسيط، جرب ترسل رسالتك مرة ثانية 🙏"

    send_telegram_message(chat_id, reply)
    return {"ok": True}
