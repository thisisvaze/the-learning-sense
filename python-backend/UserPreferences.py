import json


class Preferences():
    def __init__(self, user_id=0):
        self.user_id = 0
        with open("users/user_"+str(user_id)+"_pref.json") as user_pref:
            self.data = json.load(user_pref)
    