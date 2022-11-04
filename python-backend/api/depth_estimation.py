import base64
import requests
from PIL import Image
import gradio as gr
import json


def depth_value(apple_content):

    #img = gr.processing_utils.encode_url_or_file_to_base64(image.read())
    images = base64.b64encode(apple_content).decode('utf-8')
    response = requests.post(url='https://hf.space/embed/pytorch/MiDaS/+/api/predict/',
                             json={"data": ["data:image/png;base64," + str(images)]}).json()
    # base64.b64decode(response["data"][1])
    appheader, encoded = (str(response["data"][0])).split(",", 1)
    decoded = base64.b64decode(encoded)
    print(encoded)
    encoded
    return str(encoded)
