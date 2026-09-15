"""
run_telegram.py — Launcher for Antigravity ATS Resume Scoring Telegram Bot.
- Validates the Telegram Bot Token
- Auto-saves the token to .env if provided interactively
- Starts the Telegram Bot in polling mode (NO tunnels or webhooks required!)
"""
import os
import sys
import logging
from pathlib import Path
import requests
from dotenv import load_dotenv

# Ensure stdout flushes immediately and supports UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

# Load existing .env
env_file = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_file, override=True)

from app.config import settings
from app.adapters.telegram_bot import TelegramBotAdapter

def verify_token(token: str) -> dict:
    """Checks token with Telegram API getMe."""
    try:
        url = f"https://api.telegram.org/bot{token.strip()}/getMe"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("ok"):
                return data.get("result", {})
    except Exception as e:
        print(f"[ERROR] Could not connect to Telegram API: {e}", flush=True)
    return {}

def save_token_to_env(token: str):
    """Saves or updates TELEGRAM_BOT_TOKEN in .env file."""
    token = token.strip()
    lines = []
    found = False
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("TELEGRAM_BOT_TOKEN="):
                    lines.append(f"TELEGRAM_BOT_TOKEN={token}\n")
                    found = True
                else:
                    lines.append(line)
    if not found:
        lines.append(f"\nTELEGRAM_BOT_TOKEN={token}\n")

    with open(env_file, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"[CONFIG] Saved TELEGRAM_BOT_TOKEN to {env_file.name}", flush=True)

def main():
    print("=" * 60, flush=True)
    print("  ANTIGRAVITY ATS RESUME COACH - TELEGRAM BOT", flush=True)
    print("=" * 60, flush=True)

    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip() or settings.TELEGRAM_BOT_TOKEN.strip()

    # If not found in .env, prompt the user
    if not token:
        print("\nNo TELEGRAM_BOT_TOKEN found in .env.", flush=True)
        print("\nHow to get a FREE Telegram Bot Token (takes 30 seconds):", flush=True)
        print("  1. Open Telegram and search for: @BotFather", flush=True)
        print("  2. Send: /newbot", flush=True)
        print("  3. Enter a display name (e.g. ATS Resume Coach)", flush=True)
        print("  4. Enter a username ending in 'bot' (e.g. my_ats_coach_bot)", flush=True)
        print("  5. Copy the HTTP API token BotFather gives you\n", flush=True)

        try:
            token = input("Paste your Telegram Bot Token here: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nAborted.", flush=True)
            sys.exit(0)

        if not token:
            print("[ERROR] No token provided. Exiting.", flush=True)
            sys.exit(1)

    # Clean any accidental spaces from user input
    token = token.replace(" ", "")

    # Verify token
    print(f"\n[TELEGRAM] Verifying bot token with Telegram...", flush=True)
    bot_info = verify_token(token)
    if not bot_info:
        print("[ERROR] Invalid Telegram Bot Token! Please check the token from @BotFather.", flush=True)
        sys.exit(1)

    bot_username = bot_info.get("username", "UnknownBot")
    bot_first_name = bot_info.get("first_name", "Bot")
    print(f"[SUCCESS] Connected to Telegram Bot: {bot_first_name} (@{bot_username})", flush=True)

    # Persist in .env
    save_token_to_env(token)
    settings.TELEGRAM_BOT_TOKEN = token

    print("\n" + "=" * 60, flush=True)
    print(f"  BOT READY! Open Telegram and search for: @{bot_username}", flush=True)
    print("  Send /start to begin analyzing resumes!", flush=True)
    print("=" * 60 + "\n", flush=True)

    # Run bot
    TelegramBotAdapter.run_bot(token)

if __name__ == "__main__":
    main()
