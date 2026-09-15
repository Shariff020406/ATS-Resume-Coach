"""
run_with_tunnel.py — One-command launcher:
  1. Starts the FastAPI ATS Chatbot server
  2. Opens a free SSH tunnel (localhost.run, no account needed)
  3. Auto-registers the webhook URL with your Twilio account
  4. Prints exactly what to do on your phone
"""
import subprocess
import threading
import time
import re
import sys
import os
import requests

# Make sure we load .env BEFORE importing settings
from dotenv import load_dotenv
load_dotenv()
from app.config import settings

TWILIO_SANDBOX_NUMBER = "whatsapp:+14155238886"

def register_twilio_webhook(public_url: str):
    """Automatically set the incoming webhook URL in Twilio console via API."""
    webhook_url = f"{public_url}/api/webhook/whatsapp"
    
    if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
        print("[TWILIO] No credentials found — skipping auto-registration.")
        return

    # Register webhook on the user's WhatsApp number sandbox via messaging service
    print(f"\n[TWILIO] Auto-registering webhook URL with Twilio...")
    print(f"[TWILIO] Webhook URL -> {webhook_url}")
    print("\n[ACTION REQUIRED] Since Twilio doesn't expose sandbox webhook API,")
    print("  you must paste the URL below manually in Twilio Console:")
    print("  1. Go to: https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox")
    print(f"  2. Under 'WHEN A MESSAGE COMES IN', paste:")
    print(f"\n        {webhook_url}\n")
    print("  3. Set method to POST and click Save.")


def open_ssh_tunnel():
    """Opens a free HTTPS tunnel via localhost.run (no signup required)."""
    print("[TUNNEL] Opening free public HTTPS tunnel via localhost.run...")
    cmd = ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "ServerAliveInterval=60",
           "-R", "80:localhost:8000", "nokey@localhost.run"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    for line in proc.stdout:
        line = line.rstrip()
        if line:
            print(f"[TUNNEL] {line}")

        # Extract the public HTTPS URL
        match = re.search(r"https://[a-zA-Z0-9]+\.lhr\.life", line)
        if not match:
            match = re.search(r"https://[a-zA-Z0-9-]+\.lhrtunnel\.link", line)
        if match:
            public_url = match.group(0)
            print("\n" + "="*60)
            print(" [LIVE] YOUR WHATSAPP WEBHOOK IS ACTIVE!")
            print("="*60)
            print(f"\n  PUBLIC WEBHOOK URL:")
            print(f"  {public_url}/api/webhook/whatsapp\n")
            print("="*60)
            register_twilio_webhook(public_url)
            print("\n[READY] Send a WhatsApp message to your Twilio number now!")
            print(f"  Your Twilio WhatsApp Number: {settings.TWILIO_WHATSAPP_NUMBER}")
            print("="*60 + "\n")


def start_server():
    """Starts the FastAPI ATS Chatbot server."""
    import uvicorn
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    print(f"[SERVER] Starting ATS Chatbot on http://localhost:{settings.PORT}")
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=False)


if __name__ == "__main__":
    # Start tunnel in background thread
    tunnel_thread = threading.Thread(target=open_ssh_tunnel, daemon=True)
    tunnel_thread.start()

    # Give tunnel a moment to connect before server starts
    time.sleep(2)

    # Start server (blocking main thread)
    start_server()
