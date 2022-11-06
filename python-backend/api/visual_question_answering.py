import base64
import requests
from PIL import Image
import gradio as gr
import json
from io import BytesIO
from transformers import ViltProcessor, ViltForQuestionAnswering
import asyncio
import aiohttp


async def get_results_async(query, base64_encoded_image) -> dict:
    return getResultFromHuggingFace(query, base64_encoded_image)


async def getConcurrentMultipleResults(base64_encoded_image, queries):
    data: dict = {}
    # await asyncio.gather(*[get_results_async(query, base64_encoded_image) for query in queries])
    data = await asyncio.gather(get_results_async("where is this?", base64_encoded_image),
                                get_results_async(
        "how many people are there?", base64_encoded_image),
        get_results_async("what is the activity?", base64_encoded_image))
    print(data)
    return data


# async def getConcurrentMultipleResults(*args):
#     async with aiohttp.ClientSession() as session:
#         tasks = []
#         for arg in args:
#             tasks.append(arg[0](session, arg[1]))
#         result = await asyncio.gather(*tasks)
#     await asyncio.gather()
#     return result


async def getResultFromHuggingFace(session, base64_encoded_image, query):
    # print(images)
    url='https://thisisvaze-visual-question-answering.hf.space/api/predict'
    data =  [query, "data:image/png;base64," + str(base64_encoded_image)]
    async with session.post(url, json={"data": data}) as response:
        # print(response)
        return await response.text()
    # return response["data"][0]


def getResult(query, base64_encoded_image):
    # prepare image + question
    image = Image.open(BytesIO(base64.b64decode(base64_encoded_image)))
    text = query

    processor = ViltProcessor.from_pretrained(
        "dandelin/vilt-b32-finetuned-vqa")
    model = ViltForQuestionAnswering.from_pretrained(
        "dandelin/vilt-b32-finetuned-vqa")

    # prepare inputs
    encoding = processor(image, text, return_tensors="pt")

    # forward pass
    outputs = model(**encoding)
    logits = outputs.logits
    idx = logits.argmax(-1).item()
    print("Predicted answer:", model.config.id2label[idx])
    return model.config.id2label[idx]
