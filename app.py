# app.py

import os
from dotenv import load_dotenv
from bot import create_bot_app


def main():
    load_dotenv()

    TOKEN = os.getenv("TELEGRAM_TOKEN")

    if not TOKEN:
        raise ValueError("❌ TELEGRAM_TOKEN not found in environment")

    app = create_bot_app(TOKEN)

    print("🚀 Starting Telegram bot...")
    app.run_polling()


if __name__ == "__main__":
    main()