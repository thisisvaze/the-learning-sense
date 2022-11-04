import base64
import requests
from PIL import Image
import gradio as gr
import json
from io import BytesIO
from transformers import ViltProcessor, ViltForQuestionAnswering
import asyncio


def getResultFromHuggingFace(query, base64_encoded_image):
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
