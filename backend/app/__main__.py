import os
import sys
from pathlib import Path

import uvicorn

from app.config import get_settings
from app.src.middleware.push_notifications import generate_vapid_keys

# Change dir to project root (three levels up from this file)
os.chdir(Path(__file__).parents[2])

# Get arguments from command
args = sys.argv[1:]
settings = get_settings()

if "-vapid" in args:
    generate_vapid_keys()
    exit(0)

if __name__ == "__main__":
    uvicorn.run(
        "app.src.app:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        ssl_keyfile="/etc/ssl/key.pem",
        ssl_certfile="/etc/ssl/cert.pem",
        use_colors=True,
        proxy_headers=True,
        forwarded_allow_ips="*",
    )
