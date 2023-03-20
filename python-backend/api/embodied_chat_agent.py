import openai
import requests
import urllib.parse
import json
# short lesson learning content
# target short attention span


OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY


class emobodied_object_helper():
    def __init__(self):
        self.conversation = []

    def setObject(self, object_name):
        self.conversation = [
            {"role": "system", "content": "Act as a " + object_name + " and answer any further questions I ask in short in the voice of a " + object_name}]

    def chat_response(self, query):
        self.conversation.append(
            {"role": "user", "content": query})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.conversation
        )
        msg = response["choices"][0]["message"]
        self.conversation.append(msg)
        print(msg["content"])
        return msg["content"]


def main():
    eoh = emobodied_object_helper("couch")
    eoh.chat_response("Who are you?")
    eoh.chat_response("What are you made up of?")


if __name__ == "__main__":
    main()
