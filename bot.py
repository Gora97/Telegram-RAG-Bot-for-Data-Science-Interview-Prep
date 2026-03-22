# bot.py

import os
import logging
from collections import defaultdict, deque

from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    filters,
)

from openai import OpenAI
from assist import ask_question


# ================================
# 🔹 LOGGER SETUP
# ================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# ================================
# 🔹 OPENAI CLIENT
# ================================
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ================================
# 🔹 MEMORY STORAGE
# ================================

# For RAG conversation (last 3 interactions)
user_history = defaultdict(lambda: deque(maxlen=3))

# For summarization (store both user + bot messages)
last_user_messages = defaultdict(lambda: deque(maxlen=6))


# ================================
# 🔹 SUMMARIZATION FUNCTION
# ================================
def summarize_text(text: str) -> str:
    logger.info("Summarizing conversation...")

    prompt = f"""
Summarize the following conversation into bullet points for data science interview revision.

Conversation:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()


# ================================
# 🔹 BOT HANDLERS
# ================================
def create_bot_app(token):

    # -------- START COMMAND --------
    async def start(update, context):
        await update.message.reply_text("Hello! Ask me anything 🤖")

    # -------- MESSAGE HANDLER --------
    async def handle_message(update, context):
        user_id = update.effective_user.id
        user_text = update.message.text

        logger.info(f"User {user_id}: {user_text}")

        # Store for RAG memory
        user_history[user_id].append({
            "role": "user",
            "content": user_text
        })

        # Get response from RAG
        response = ask_question(
            user_text,
            history=list(user_history[user_id])
        )

        # Store bot response in RAG memory
        user_history[user_id].append({
            "role": "assistant",
            "content": response
        })

        # Store for summarization (text format)
        last_user_messages[user_id].append(f"User: {user_text}")
        last_user_messages[user_id].append(f"Bot: {response}")

        await update.message.reply_text(response)

    # -------- SUMMARIZE COMMAND --------
    async def summarize(update, context):
        user_id = update.effective_user.id

        messages = last_user_messages[user_id]

        if not messages:
            await update.message.reply_text("No messages to summarize.")
            return

        text = "\n".join(messages)

        summary = summarize_text(text)

        await update.message.reply_text("🧠 Summary:\n" + summary)

    # ================================
    # 🔹 BUILD APP
    # ================================
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("summarize", summarize))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot initialized successfully")

    return app