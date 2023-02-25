import base64
import requests
from PIL import Image
import gradio as gr
import json
from io import BytesIO
from transformers import ViltProcessor, ViltForQuestionAnswering
import asyncio
import aiohttp


async def getResultFromHuggingFace(session, base64_encoded_image, query):
    # print(images)
    url = 'https://thisisvaze-visual-question-answering.hf.space/api/predict'
    data = {"data": [query, "data:image/png;base64," + base64_encoded_image]}
    # print(data)
    async with session.post(url, json=data) as response:
        return await response.text()


async def getConcurrentMultipleResults(b64_image, queries):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for query in queries:
            tasks.append(getResultFromHuggingFace(session, b64_image, query))
        result = await asyncio.gather(*tasks)
        print(result)
        return result


# def getResult(query, base64_encoded_image):
#     # prepare image + question
#     image = Image.open(BytesIO(base64.b64decode(base64_encoded_image)))
#     text = query

#     processor = ViltProcessor.from_pretrained(
#         "dandelin/vilt-b32-finetuned-vqa")
#     model = ViltForQuestionAnswering.from_pretrained(
#         "dandelin/vilt-b32-finetuned-vqa")

#     # prepare inputs
#     encoding = processor(image, text, return_tensors="pt")

#     # forward pass
#     outputs = model(**encoding)
#     logits = outputs.logits
#     idx = logits.argmax(-1).item()
#     print("Predicted answer:", model.config.id2label[idx])
#     return model.config.id2label[idx]
