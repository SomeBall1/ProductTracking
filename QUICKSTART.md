# Quick Start Guide - 5 Minutes to Running 🚀

## Step 1: Install Dependencies (2 minutes)

Open Command Prompt in the project folder:

```bash
cd C:\Users\D\Downloads\CODING\ProductTracking
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

## Step 2: Set Up Telegram Bot (2 minutes)

### Get Bot Token:
1. Open Telegram → Search `@BotFather`
2. Send: `/newbot`
3. Follow prompts, copy the token

### Get Your Chat ID:
1. Search `@userinfobot` on Telegram
2. Start chat, copy your chat ID

## Step 3: Configure (30 seconds)

Create `.env` file:
```bash
copy .env.example .env
notepad .env
```

Add your credentials:
```
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
CHECK_INTERVAL_MINUTES=5
```

## Step 4: Get All Locations (30 seconds)

```bash
python fetch_locations.py
```

Copy the output and paste it into `config.py` (replace the `LOCATIONS` list).

## Step 5: Run! (10 seconds)

```bash
python main.py
```

You should get a Telegram message saying "Product Monitor Started" 🎉

## That's It!

The monitor is now running. Keep the window open, or set it up to run at startup (see README.md).

You'll get a Telegram notification whenever your salmon becomes available at any Fisherija location!

## Quick Test

To test notifications are working, you can temporarily modify `scraper.py` to always return `available: True` and run a check cycle.

## Need Help?

See the full README.md for:
- Running 24/7 in the background
- Troubleshooting
- Detailed configuration options
