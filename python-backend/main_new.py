from hololens import hololens_sensor_connection, hololens_utilities
import Constants.Values as CONSTANTS
from asyncio import constants
from pickle import GLOBAL
from fastapi_socketio import SocketManager
from email.mime import image
from fastapi import FastAPI, UploadFile, WebSocket, File
from sympy import Q
import api.ocr_recognition as ocr_recognition
from api import descriptive_answering, plant_recognition, multiple_object_detection, depth_estimation, get_3d_model, sketch_recognition, visual_question_answering, sentiment_analysis
from api.norfair_utilities import YOLO, yolo_detections_to_norfair_detections, names
from fastapi.responses import PlainTextResponse
import os
import asyncio
import aiohttp
import os
import urllib.parse
import openai
from threading import Thread
import cv2
import time
import base64
import argparse
import os
from re import T
from typing import List, Optional, Union
import numpy as np
import torch
import torchvision.ops.boxes as bops
import api.norfair_utilities as norfair_utilities
import cv2
from api.norfair_utilities import Detection, Paths, Tracker, Video
from norfair.distances import frobenius, iou
import Constants.Values
from zed import zed_sensor_connection
import context_handler


# Init hololens connection
# hololens_connection_manager = hololens_sensor_connection.HololensConnectionManager(
#  show_stream=False)
# Init Zed Connection
zed_connection_manager = zed_sensor_connection.ZedConnectionManager(
    show_stream=False)
context_handler_obj = context_handler.context(
    sensor_connection_manager=zed_connection_manager)

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # video_stream_widget.trackMultipleObjects()
        # topic = await websocket.receive_text()
        # print(data)
        # match data:

        #     case "context":
        #         multipleObjectDetection(hololens2_utilities.getPhoto())
        #         await asyncio.sleep(1)
        #data = multipleObjectDetection(hololens2_utilities.getPhoto())

        # showSurfaceAreaDummyLesson
        #data = generate_lesson.initiate_curiousityAndSendToHeadset()

        # Generate Facts
        #data = descriptive_answering.fact_generator(topic, hololens2_utilites.getPhoto())
        #data = "asda"
        # Track objects real timeh
        data = {"Items": context_handler_obj.env_context.getData()}
        #data = returnCurrentImageFromCamera()
        time.sleep(0.01)
        #data = multipleObjectDetection(returnCurrentImageFromCamera())
        #data = multipleObjectDetection(hololens2_utilities.getPhoto())
        await websocket.send_text(f"{data}")


# if __name__ == "__main__":
#     main()
