import json


class Preferences():
    def __init__(self):
        with open("user_pref.json") as user_pref:
            self.data = json.load(user_pref)

    def set(self, data):
        self.data = data
        with open("user_pref.json", "w") as user_pref:
            json.dump(self.data, user_pref)
        return json.dumps(self.data)

def main():
    pref = Preferences(1)
    print(pref.data["subject"])


if __name__ == "__main__":
    main()
