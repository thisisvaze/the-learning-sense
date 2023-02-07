import base64
import re
import requests
from PIL import Image
import gradio as gr
import json
from api import sketchfab_helper

model_maps = {
    "apple": "588278115f92444fab01aa121da0b244",
    "orange": ""
}

model_maps_local = {
    "apple": "588278115f92444fab01aa121da0b244",
    "orange": ""
}


def from_echo3d(keyword):

    # iparsing request
    API_KEY = "young-hat-4823"
    URL = "https://api.echo3D.co/search?key=young-hat-4823&keywords="+keyword
    response = requests.get(url=URL).json()

    print(response)
    # parsing response
    model_url = ""
    for result in response:
        if result["gltf_url"]:
            model_url = result["gltf_url"]

    return model_url


def from_sketchfab(keyword):
    sk = sketchfab_helper.sketchfab()
    return sk.getBestModelFromKeyword(keyword)


def from_sketchfab_UID_database(keyword):
    UID = model_maps[keyword]
    URL = " https://api.sketchfab.com/v3/models/" + UID + "/download"
    response = requests.get(url=URL).json()
    print(response)
    return response


def from_local_hololens_database(keyword):
    data = []
    data.append({"model_url": keyword})
    return data

