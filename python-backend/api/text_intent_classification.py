from wit import Wit
import Constants.Values as CONSTANTS

class wit_utilities:
    def __init__(self):
        self.wit_client = Wit(CONSTANTS.WIT_ACCESS_TOKEN)

    def infer_message(self, message):
        return self.wit_client.message(message)
        