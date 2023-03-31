from hololens import hololens_sensor_connection, hololens_utilities
import Constants.Values as CONSTANTS
from asyncio import constants
from pickle import GLOBAL
from fastapi_socketio import SocketManager
from email.mime import image
from fastapi import FastAPI, UploadFile, WebSocket, File, Request
from sympy import Q
import api.ocr_recognition as ocr_recognition
from api import get_3d_model, embodied_chat_agent
# from api.norfair_utilities import YOLO, yolo_detections_to_norfair_detections, names
from fastapi.responses import PlainTextResponse
import os
from multiprocessing import Process, Manager
import asyncio
import aiohttp
import os
import urllib.parse
import openai
from threading import Thread, Lock
import multiprocessing
import cv2
import time
import base64
import argparse
import os
import json
import copy
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
from fastapi.middleware.cors import CORSMiddleware


from zed import zed_sensor_connection
from kinect import kinect_sensor_connection
import lesson_helper
import context_handler
import lesson_helper
import requests
from api import text_intent_classification
import uvicorn
from fastapi import WebSocket


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# sio = SocketManager(app=app)
wit = text_intent_classification.wit_utilities()


# Init hololens connection
# connection_manager = hololens_sensor_connection.HololensConnectionManager(
#     show_stream=False)
connection_manager = zed_sensor_connection.ZedConnectionManager()

# KNECT connection manager
#connection_manager = kinect_sensor_connection.KinectConnectionManager()

context_handler_obj = context_handler.context(
    sensor_connection_manager=connection_manager)

lesson_manager = lesson_helper.lesson_helper_object()

chat_agent = embodied_chat_agent.emobodied_object_helper()


def sendDataToUnity(tag, data):
    sendinthisdata = {CONSTANTS.DATA_TYPE: tag, CONSTANTS.DATA_VALUE: data}
    print(sendinthisdata)
    return sendinthisdata


@ app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(data)
        json_data = json.loads(data)
        if json_data[CONSTANTS.DATA_TYPE] == CONSTANTS.INITIATE_LESSON_REQUEST:
            context_handler_obj.session.state = CONSTANTS.SESSION_STATE_INITIATING_LESSON
            await websocket.send_text(f"{sendDataToUnity(CONSTANTS.LESSON_INIT_INFO,lesson_manager.sendLesson(json_data[CONSTANTS.DATA_VALUE], context_handler_obj.user_preferences.data))}")
            context_handler_obj.session.state = CONSTANTS.SESSION_STATE_LESSON_INITIATED

        elif json_data[CONSTANTS.DATA_TYPE] == CONSTANTS.SPEECH_SENTENCE_SPOKEN:
            # if context_handler_obj.session.state == CONSTANTS.SESSION_EMBODIED_CHAT:
            #     if str(json_data[CONSTANTS.DATA_VALUE]).lower() == "bye":
            #         context_handler_obj.session.state = CONSTANTS.SESSION_STATE_EXPLORE
            #         data = "Bye"
            #         await websocket.send_text(f"{sendDataToUnity(CONSTANTS.END_EMBODIED_CHAT,data)}")

            #     data = chat_agent.chat_response(
            #         json_data[CONSTANTS.DATA_VALUE])
            #     await websocket.send_text(f"{sendDataToUnity(CONSTANTS.EMBODIED_CHAT_DATA_UPDATE,data)}")
            # else:
            # and context_handler_obj.session.state == CONSTANTS.SESSION_STATE_LESSON_INITIATED:

            data = lesson_manager.handle_speech_message_with_gpt(
                json_data[CONSTANTS.DATA_VALUE], context_handler_obj)

            # data = lesson_manager.handle_speech_message(
            #     wit.infer_message(json_data[CONSTANTS.DATA_VALUE]), context_handler_obj)

            await websocket.send_text(f"{data}")

        elif json_data[CONSTANTS.DATA_TYPE] == CONSTANTS.REQUEST_ENV_INFO_UPDATE:
            data = {"Items": lesson_manager.sendEnvUpdateWithCuriosity(context_handler_obj.user_preferences.data,
                                                                       context_handler_obj.env_context.getDefaultParameters())}
            await websocket.send_text(f"{sendDataToUnity(CONSTANTS.ENVIRONMENT_OJBECTS_UPDATE, data)}")

        # elif json_data[CONSTANTS.DATA_TYPE] == CONSTANTS.GAZE_INPUT:
        #     context_handler_obj.gaze_position = json_data[CONSTANTS.DATA_VALUE]

        elif json_data[CONSTANTS.DATA_TYPE] == CONSTANTS.REQUEST_MODEL_URL:
            data = {"model_url": get_3d_model.from_sketchfab(
                json_data[CONSTANTS.DATA_VALUE]), "model_name": json_data[CONSTANTS.DATA_VALUE]}
            await websocket.send_text(f"{sendDataToUnity(CONSTANTS.DOWNLOAD_AND_SHOW_3D_MODEL,data)}")

        elif json_data[CONSTANTS.DATA_TYPE] == CONSTANTS.INITIATE_EMBOIDIED_CHAT:
            context_handler_obj.session.state = CONSTANTS.SESSION_EMBODIED_CHAT
            chat_agent.setObject(json_data[CONSTANTS.DATA_VALUE])
            data = chat_agent.chat_response("Hey there! Introduce Yourself.")
            await websocket.send_text(f"{sendDataToUnity(CONSTANTS.EMBODIED_CHAT_DATA_UPDATE,data)}")

        elif json_data[CONSTANTS.DATA_TYPE] == CONSTANTS.SET_USER_PREFERENCES:
            context_handler_obj.user_preferences.set(
                json_data[CONSTANTS.DATA_VALUE])
        else:
            pass


@ app.post("/add_lessons")
async def updateLessons(new_lesson_data: Request):
    data = await new_lesson_data.json()
    return lesson_manager.add_lesson(data)


@ app.post("/update_user_preferences")
async def updateLessons(new_user_pref_data: Request):
    data = await new_user_pref_data.json()
    return context_handler_obj.user_preferences.set(data)


@ app.get("/get_special_parametere")
def main():
    return context_handler_obj.env_context.getColorsOfObjectsInEnvironment()


@ app.get("/get_lessons")
async def main():
    return lesson_manager.lessons


@ app.get("/get_user_preferences")
async def main():
    return context_handler_obj.user_preferences.data


@ app.get("/get_system_preferences")
async def main():
    return lesson_manager.cxr_preferences


@ app.post("/modify_mode")
async def main(new_mode_data: Request):
    data = await new_mode_data.json()
    return lesson_manager.modify_cxr_pref(data)


@ app.post("/send_env_context")
def main():
    # data = await env_data.json()
    ret_data = {"Items": lesson_manager.sendEnvUpdateWithCuriosity(context_handler_obj.user_preferences.data,
                                                                   [{"lesson_curiosity_text": "potted plant",
                                                                    "name": "potted plant", "x": 1, "y": 1, "z": 0.1, "visibility": 1},
                                                                    {"lesson_curiosity_text": "mug",
                                                                    "name": "mug", "x": 1, "y": 1, "z": 0.1, "visibility": 1},
                                                                    {"lesson_curiosity_text": "table",
                                                                    "name": "table", "x": 1, "y": 1, "z": 0.1, "visibility": 1},
                                                                    {"lesson_curiosity_text": "chair",
                                                                    "name": "chair", "x": 1, "y": 1, "z": 0.1, "visibility": 1},
                                                                    {"lesson_curiosity_text": "laptop",
                                                                    "name": "laptop", "x": 1, "y": 1, "z": 0.1, "visibility": 1},
                                                                    {"lesson_curiosity_text": "mouse",
                                                                    "name": "mouse", "x": 1, "y": 1, "z": 0.1, "visibility": 1}])}
    return ret_data


def main():
    uvicorn.run("main:app", host="0.0.0.0",
                port=8000, log_level="info", reload=True)


if __name__ == "__main__":
    main()
