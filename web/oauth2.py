import requests
import yaml
import os

class OAuth(object):

    with open('web/settings/web_settings.yaml', 'r') as f: settings = yaml.load(f, Loader= yaml.FullLoader)

    CLIENT_ID = settings['CLIENT_ID']
    CLIENT_SECRET = settings['CLIENT_SECRET']
    scope = settings['SCOPE']
    redirect_uri = settings['REDIRECT_URI']
    discord_login_url = f"https://discordapp.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={redirect_uri}&response_type=code&scope={scope}"
    discord_token_url = 'https://discordapp.com/api/oauth2/token'
    discord_api_url = 'https://discordapp.com/api'

    @staticmethod
    def get_access_token(code):
        data = {
            'client_id': OAuth.CLIENT_ID,
            'client_secret': OAuth.CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': OAuth.redirect_uri,
            'scope': OAuth.scope
        }
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        access_token = requests.post(url= OAuth.discord_token_url, data= data, headers= header)
        json = access_token.json()
        return json.get("access_token")

    @staticmethod
    def get_user_info(access_token):
        header = {
            'Authorization': f'Bearer {access_token}'
        }

        user_obj = requests.get(url= f'{OAuth.discord_api_url}//users/@me', headers= header)
        user_json = user_obj.json()
        return user_json

    @staticmethod
    def get_user_guilds(access_token):
        header = {
            'Authorization': f'Bearer {access_token}'
        }

        guilds_obj = requests.get(url= f'{OAuth.discord_api_url}/users/@me/guilds', headers= header)
        guilds_json = guilds_obj.json()
        return guilds_json