# Twitter to Telegram Monitoring Bot

A Python bot that monitors Twitter users and sends relevant tweets to a Telegram chat.

## Features
- Real-time tweet monitoring
- Telegram notifications with text + tweet link
- Keyword filtering
- Multi-user tracking
- Easy deployment on Render or Railway

## Setup

1. Clone this repo.
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Set environment variables:
- `TELEGRAM_BOT_TOKEN`
- `TWITTER_BEARER_TOKEN`
- `TELEGRAM_CHAT_ID`
- `TRACKED_USERS` (comma-separated usernames)
- `KEYWORDS` (comma-separated)

4. Run the bot:
```bash
python bot.py
```

## Deployment

### Render
- Add `render.yaml`
- Deploy and set environment variables

### Railway
- Create new project
- Connect GitHub repo
- Set environment variables in settings

## License
MIT
