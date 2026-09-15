import subprocess
import time
import re
import threading
from app.config import settings

def run_ssh_tunnel():
    print("==================================================")
    print("[TUNNEL] CREATING FREE PUBLIC HTTPS TUNNEL VIA SSH...")
    print("==================================================")
    
    cmd = ["ssh", "-o", "StrictHostKeyChecking=no", "-R", "80:localhost:8000", "nokey@localhost.run"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    tunnel_url = None
    for line in proc.stdout:
        print(line, end="")
        match = re.search(r"https://[a-zA-Z0-9-]+\.lhrtunnel\.link|https://[a-zA-Z0-9-]+\.lhr\.life", line)
        if match:
            tunnel_url = match.group(0)
            print("\n" + "="*50)
            print(f" SUCCESS! YOUR LIVE PUBLIC WHATSAPP WEBHOOK URL IS:")
            print(f"\n    {tunnel_url}/api/webhook/whatsapp\n")
            print("="*50)
            print("Copy this URL into Twilio Console:")
            print("Messaging -> Settings -> WhatsApp Sandbox Settings -> 'WHEN A MESSAGE COMES IN'")
            print("="*50 + "\n")

if __name__ == "__main__":
    t = threading.Thread(target=run_ssh_tunnel, daemon=True)
    t.start()
    
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=False)
