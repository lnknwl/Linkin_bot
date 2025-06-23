import requests
import os
from dotenv import load_dotenv, set_key

load_dotenv()

def refresh_access_token(client_id, client_secret, refresh_token):
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret,
    }

    response = requests.post(url, data=params)
    data = response.json()

    if 'access_token' in data:
        new_access_token = data['access_token']
        new_refresh_token = data['refresh_token']

        update_env_variable("ACCESS_TOKEN", new_access_token)
        update_env_variable("REFRESH_TOKEN", new_refresh_token)

        print("Access token успешно обновлён")
        return new_access_token, new_refresh_token
    else:
        print('Ошибка обновления токена:', data)
        return None, None

def update_env_variable(key, value, filename=".env"):
    set_key(filename, key, value)