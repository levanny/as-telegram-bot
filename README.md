# TokosJarvis Bot

A simple Telegram bot that answers basic car service questions.

---

## How to Run

1. Make sure you have Python 3.12+ installed.

2. Clone the project and go to the folder:
```bash
git clone https://github.com/levanny/as-telegram-bot
cd as-telegram-bot

Create a .env & .env.docker files in the project root and add your bot token, database url, password, username:
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN

Install dependencies:
uv sync

Run the bot:
uv run python bot.py
