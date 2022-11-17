import math
import os
import openai
import json
import requests
import urllib.parse
from . import draw, multiple_object_detection
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

WOLFRAM_API_KEY = "TT3P62-W479LAP7E3"


def openai_text_output(query):

    response = openai.Completion.create(
        model="text-curie-001",
        prompt=query,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text


def fact_generator(topic, object_name):
    print("generating a " + topic + " fact for " + object_name)
    min_distance_x = 1
    min_distance_object_label = ""
    # for object in data:
    #     print(object)
    #     if (abs(object["x"]-0.5) < min_distance_x):
    #         min_distance_object_label = object["name"]
    response = openai.Completion.create(
        model="text-curie-001",
        # prompt="tell me a fact about"+min_distance_object_label +
        #"that teaches me " + topic,
        prompt="tell me a" + topic + " concept which is about a "+object_name,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return "A " + topic + " fact for "+min_distance_object_label+":"+response.choices[0].text


def wolram_results(query):
    URL_ENCODED_INPUT = urllib.parse.quote_plus(query)
    API_URL = "http://api.wolframalpha.com/v1/result?appid={WOLFRAM_API_KEY}&i={URL_ENCODED_INPUT}"
    response = requests.request("GET", API_URL)
    print(response.text)
    return response.text


async def get_wolfram_results_async(session, query):
    URL_ENCODED_INPUT = urllib.parse.quote_plus(query)
    API_URL = "http://api.wolframalpha.com/v1/result?appid={WOLFRAM_API_KEY}&i={URL_ENCODED_INPUT}"
    async with session.get(API_URL) as response:
        return await response.text()


def wolram_spoken_results(query):
    URL_ENCODED_INPUT = urllib.parse.quote_plus(query)
    API_URL = "http://api.wolframalpha.com/v1/result?appid={WOLFRAM_API_KEY}&i={URL_ENCODED_INPUT}"
    response = requests.request("GET", API_URL)
    print(response.text)
    return response.text
