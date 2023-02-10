import base64
import requests
from PIL import Image
import gradio as gr
import json

async def return_sentiment_async(session, query,random):
    url = 'https://hf.space/embed/srini047/text-based-sentiment-analyzer/+/api/predict'
    async with session.post(url, json={"data": [query]}) as response:
        # print(response)
        return await response.text()
        # return str(response)
