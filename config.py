import os
from dotenv import load_dotenv
from token_utils import refresh_access_token

load_dotenv()

def get_bot_config():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    refresh_token = os.getenv("REFRESH_TOKEN")

    access_token, _ = refresh_access_token(client_id, client_secret, refresh_token)

    return {
        "access_token": access_token,
        "prefix": os.getenv("PREFIX"),
        "channel": os.getenv("TARGET_CHANNEL"),
        "bot_name": os.getenv("BOT_NAME")
    }
