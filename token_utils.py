import requests
import os
from dotenv import load_dotenv

load_dotenv()

def refresh_access_token(client_id, client_secret, refresh_token):
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret,
    }

    response = requests.post(url, params=params)
    data = response.json()

    if 'access_token' in data:
        new_access_token = data['access_token']
        new_refresh_token = data['refresh_token']

        update_env_variable("REFRESH_TOKEN", new_refresh_token)

        return new_access_token, new_refresh_token
    else:
        print('Ошибка обновления токена:', data)
        return None, None

def update_env_variable(key, value, filename=".env"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
    else:
        lines = []

    found = False
    for i in range(len(lines)):
        if lines[i].startswith(f"{key}="):
            lines[i] = f"{key} = {value}\n"
            found = True
            break

    if not found:
        lines.append(f"{key}={value}\n")

    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(lines)