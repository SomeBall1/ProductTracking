# Wolt Product Availability Monitor 🔔

Automatically monitors Wolt for product availability and sends instant push notifications to your phone via Telegram when the product becomes available.

## Features

- 🔍 Monitors multiple Wolt locations simultaneously
- 📱 Instant Telegram push notifications
- 💾 SQLite database tracking availability history
- ⏰ Configurable check intervals
- 🚀 Easy setup and configuration
- 📊 Detailed logging

## Prerequisites

- Python 3.8 or higher
- Windows PC (running 24/7)
- Telegram account

## Setup Instructions

### 1. Install Python Dependencies

Open Command Prompt or PowerShell and navigate to the project directory:

```bash
cd C:\Users\D\Downloads\CODING\ProductTracking
```

Create a virtual environment (recommended):

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright browsers:

```bash
playwright install chromium
```

### 2. Set Up Telegram Bot

#### Create a Telegram Bot:

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow the prompts to create your bot
4. Copy the bot token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

#### Get Your Chat ID:

1. Search for `@userinfobot` on Telegram
2. Start a chat with it
3. It will reply with your chat ID (a number like: `123456789`)

### 3. Configure the Application

Copy the example environment file:

```bash
copy .env.example .env
```

Edit `.env` file and add your credentials:

```
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
CHECK_INTERVAL_MINUTES=5
PRODUCT_NAME=Divlji crveni losos fileti s kožom MSC 150g
```

### 4. Fetch All Fisherija Locations

Run the location fetcher to get all 11 locations:

```bash
python fetch_locations.py
```

This will output a configuration block. Copy it and update the `LOCATIONS` list in `config.py`.

### 5. Test the Setup

Test that everything works:

```bash
python main.py
```

You should receive a startup message on Telegram, and the script will start monitoring.

Press `Ctrl+C` to stop.

## Running 24/7

### Option 1: Keep Terminal Open

Simply run:

```bash
python main.py
```

Keep the terminal window open. The script will run continuously.

### Option 2: Run as Background Service (Windows)

Create a batch file `start_monitor.bat`:

```batch
@echo off
cd C:\Users\D\Downloads\CODING\ProductTracking
call venv\Scripts\activate
python main.py
```

Then:
1. Press `Win + R`
2. Type `shell:startup`
3. Create a shortcut to `start_monitor.bat` in this folder
4. The monitor will start automatically when Windows boots

### Option 3: Use Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: "At startup"
4. Action: Start a program
5. Program: `C:\Users\D\Downloads\CODING\ProductTracking\venv\Scripts\python.exe`
6. Arguments: `main.py`
7. Start in: `C:\Users\D\Downloads\CODING\ProductTracking`

## Configuration

Edit `config.py` to customize:

- `CHECK_INTERVAL_MINUTES`: How often to check (default: 5 minutes)
- `LOCATIONS`: List of Wolt locations to monitor
- `PRODUCT_NAME`: Name of the product to track

## How It Works

1. **Scheduler**: Checks all locations every X minutes
2. **Scraper**: Uses Playwright to load Wolt pages and check availability
3. **Database**: Tracks availability history to detect changes
4. **Notifier**: Sends Telegram notification when product becomes available

## Notifications

You'll receive notifications when:
- ✅ Monitor starts up
- 🎉 Product becomes available at any location
- ❌ Errors occur (optional)

## Logs

All activity is logged to:
- Console output
- `product_monitor.log` file

## Troubleshooting

### "TELEGRAM_BOT_TOKEN is required"
Make sure you created the `.env` file and added your bot token.

### "Failed to connect to Telegram"
- Check your bot token is correct
- Check your internet connection
- Make sure bot isn't blocked

### "Timeout loading page"
- Check your internet connection
- Increase timeout in `scraper.py`
- Try running with `headless=False` to see what's happening

### Product availability not detected correctly
- The Wolt page structure might have changed
- Check the scraper logic in `scraper.py`
- Run with `headless=False` to debug

## Files Overview

- `main.py` - Main monitoring loop
- `scraper.py` - Web scraping logic for Wolt
- `notifier.py` - Telegram notification handler
- `database.py` - SQLite database models
- `config.py` - Configuration settings
- `fetch_locations.py` - Utility to fetch all locations
- `requirements.txt` - Python dependencies
- `.env` - Your secret configuration (not committed to git)

## Security Notes

- Never commit your `.env` file to git
- Keep your bot token secret
- The `.gitignore` file protects sensitive files

## Support

If you encounter issues:
1. Check the logs in `product_monitor.log`
2. Verify your Telegram credentials
3. Test internet connectivity
4. Make sure Python and all dependencies are installed correctly

## License

This project is for personal use to monitor product availability on Wolt.

---

**Happy monitoring! 🎣**
