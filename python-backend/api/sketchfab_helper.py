import requests
from base64 import b64encode
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
SKETCHFAB_CLIENT_ID = 'asl5ceWqUHzbhzq7zrAM7crH7dnGA366QuB3ut4G'
SKETCHFAB_CLIENT_SECRET = '61OyozD26MK1CgYXRqjKGdL2jk8WSsEbuhqijW1hXBOxjt0GjIv9l0YzeUDSpoQeN6l69uzEhqXIBP0oGGKmROB1UrUpJ4Yq22fuEWFJjUcQ5CeLz1zyNh6ZLbpcWd0I'

client_id = 'asl5ceWqUHzbhzq7zrAM7crH7dnGA366QuB3ut4G'
client_secret = '61OyozD26MK1CgYXRqjKGdL2jk8WSsEbuhqijW1hXBOxjt0GjIv9l0YzeUDSpoQeN6l69uzEhqXIBP0oGGKmROB1UrUpJ4Yq22fuEWFJjUcQ5CeLz1zyNh6ZLbpcWd0I'
authorization_base_url = '"https://sketchfab.com/oauth2/token/'
token_url = 'https://github.com/login/oauth/access_token'
redirect_url = 'http://localhost'
code = '3LJgs2JW1To209XsImywjbS0rRgDl6'

sketchfab_self_creds = {'access_token': 'hZ7DJc4mIAqFCVGs5fyAXIyRqugd4I', 'expires_in': 2592000,
                        'token_type': 'Bearer', 'scope': 'read write', 'refresh_token': 'dl2VXEm35zVCSvw2FIbL2pnHcYfQON'}


def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'


username = SKETCHFAB_CLIENT_ID
password = SKETCHFAB_CLIENT_SECRET


class sketchfab():
    def __init__(self):
        # API_URL = "https://sketchfab.com/oauth2/token/"
        # headers = {'Authorization': basic_auth(username, password)}
        # # print(HTTPBasicAuth(SKETCHFAB_CLIENT_ID, SKETCHFAB_CLIENT_SECRET))
        # response = requests.post(API_URL, headers={'Content-type': 'application/x-www-form-urlencoded'},
        #                          data="grant_type=authorization_code&code=3LJgs2JW1To209XsImywjbS0rRgDl6&client_id=asl5ceWqUHzbhzq7zrAM7crH7dnGA366QuB3ut4G&client_secret=61OyozD26MK1CgYXRqjKGdL2jk8WSsEbuhqijW1hXBOxjt0GjIv9l0YzeUDSpoQeN6l69uzEhqXIBP0oGGKmROB1UrUpJ4Yq22fuEWFJjUcQ5CeLz1zyNh6ZLbpcWd0I&redirect_uri=http://localhost")
        #

        UID = '5322e7ba8e1848268152e6f82187861d'
        API_URL = "https://api.sketchfab.com/v3/models/"+UID
        headers = {'Authorization': "Bearer hZ7DJc4mIAqFCVGs5fyAXIyRqugd4I"}
        response = requests.get(API_URL, headers=headers)
        print(response.json()["faceCount"])


def main():
    sk = sketchfab()


if __name__ == "__main__":
    main()
