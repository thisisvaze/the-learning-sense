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
code = '5mt4Le5FGaVzdKGfA7Vsl1dOXiJ3pU'

sketchfab_self_creds = {"access_token": "gDjGHGfRO9bdXb5OPQ7premDWvkn4n", "expires_in": 2592000,
                        "token_type": "Bearer", "scope": "read write", "refresh_token": "vQ5AaVLNCwBFeyiRcZC80BjNlkvQgg"}
model_maps = {
    "apple": "588278115f92444fab01aa121da0b244",
    "orange": ""
}
access_token = "gDjGHGfRO9bdXb5OPQ7premDWvkn4n"

polygonCountLimit = 20000


def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'


username = SKETCHFAB_CLIENT_ID
password = SKETCHFAB_CLIENT_SECRET


class sketchfab():
    def __init__(self):
        pass

    def getInitialToken():
        API_URL = "https://sketchfab.com/oauth2/token/"
        headers = {'Authorization': basic_auth(username, password)}
        # print(HTTPBasicAuth(SKETCHFAB_CLIENT_ID, SKETCHFAB_CLIENT_SECRET))
        response = requests.post(API_URL, headers={'Content-type': 'application/x-www-form-urlencoded'},
                                 data="grant_type=authorization_code&code="+code+"&client_id="+client_id+"&client_secret="+client_secret+"&redirect_uri="+redirect_url)
        print(response.text)

        #UID = '5322e7ba8e1848268152e6f82187861d'
    # def getBestModelUUID(keyword):
    #     API_URL = "https://api.sketchfab.com/v3/models/"+UID
    #     headers = {'Authorization': "Bearer hZ7DJc4mIAqFCVGs5fyAXIyRqugd4I"}
    #     response = requests.get(API_URL, headers=headers)
    #     print(response.json()["faceCount"])
    #     self.getBestModelFileURL(UID)

    def getBestModelUUID(self, keyword):
        API_URL = "https://api.sketchfab.com/v3/search?type=models&q="+keyword + \
            "&downloadable=true&max_face_count=50000"
        headers = {'Authorization': "Bearer hZ7DJc4mIAqFCVGs5fyAXIyRqugd4I"}
        response = requests.get(API_URL, headers=headers).json()
        for result in response["results"]:
            if result["archives"]["glb"]["faceCount"] < polygonCountLimit:
                return result["uid"]

        return "no_valid_model_found"

    def getBestModelFileURL(self, UID):
        headers = {'Authorization': "Bearer "+access_token}
        URL = " https://api.sketchfab.com/v3/models/"+UID+"/download"
        response = requests.get(url=URL, headers=headers).json()
        print(response["glb"]["url"])
        return response["glb"]["url"]
        # print(response)
        # parsing response
        model_url = ""

        print(model_url)
        return model_url

    def getBestModelFromKeyword(self, keyword):
        return self.getBestModelFileURL(self.getBestModelUUID(keyword))

def main():
    sk = sketchfab()

    sk.getBestModelFileURL(sk.getBestModelUUID("cup"))


if __name__ == "__main__":
    main()
