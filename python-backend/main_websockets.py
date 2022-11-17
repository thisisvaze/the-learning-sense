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
import lesson_generator
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
from zed import zed_sensor_connection
import context_handler
from lesson import lesson_helper
import requests
from api import message_extraction
import uvicorn
from fastapi import WebSocket
# Init hololens connection
# connection_manager = hololens_sensor_connection.HololensConnectionManager(
#     show_stream=False)

p1 = None



session_started = False

connection_manager = zed_sensor_connection.ZedConnectionManager(
        show_stream=False)

context_handler_obj = context_handler.context(
    sensor_connection_manager=connection_manager)

app = FastAPI()
sio = SocketManager(app=app)
wit = message_extraction.wit_utilities()

def sendDataToUnity(tag, data):
    sendinthisdata = {CONSTANTS.DATA_TYPE: tag, CONSTANTS.DATA_VALUE: data}
    print(sendinthisdata)
    return sendinthisdata

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(data)
        json_data = json.loads(data)
        if json_data[CONSTANTS.DATA_TYPE] == CONSTANTS.REQUEST_ENV_INFO_UPDATE:
            data = {"Items": context_handler_obj.env_context.getDefaultParameters()}
            await websocket.send_text(f"{sendDataToUnity(CONSTANTS.ENVIRONMENT_OJBECTS_UPDATE, data)}")
            #await asyncio.sleep(0.5)
        elif json_data[CONSTANTS.DATA_TYPE] == CONSTANTS.SPEECH_SENTENCE_SPOKEN and context_handler_obj.session.state == CONSTANTS.SESSION_STATE_LESSON_INITIATED:
            await websocket.send_text(f"{sendDataToUnity(CONSTANTS.SHOW_3D_MODEL,lesson_helper.handle_message(wit.infer_message(data)))}")

        elif json_data[CONSTANTS.DATA_TYPE] == CONSTANTS.INITIATE_LESSON_REQUEST:
            context_handler_obj.session.state = CONSTANTS.SESSION_STATE_INITIATING_LESSON
            await websocket.send_text(f"{sendDataToUnity(CONSTANTS.LESSON_INIT_INFO,lesson_generator.sendLesson(json_data[CONSTANTS.DATA_VALUE]))}")
            context_handler_obj.session.state = CONSTANTS.SESSION_STATE_LESSON_INITIATED
        elif json_data[CONSTANTS.DATA_TYPE] == CONSTANTS.BUTTON_PRESSED:
            print(json_data[CONSTANTS.DATA_TYPE], json_data[CONSTANTS.DATA_VALUE])
        elif json_data[CONSTANTS.DATA_TYPE] == CONSTANTS.SET_USER_PREFERENCES:
            context_handler_obj.user_preferences.
        else:
            pass

# async def manageCommunicationWithDevice():
#     global session_state
#     print("Session state changed to :" + session_state)
#     if session_state == CONSTANTS.SESSION_STATE_EXPLORE:
#         # asyncio.get_event_loop().create_task(env_info_update())
        
#         app.sio.start_background_task(target=send_env_info)
#         #session_started = True

#     if session_state == CONSTANTS.SESSION_STATE_INITIATING_LESSON:
#         await app.sio.emit(CONSTANTS.LESSON_INIT_INFO,
#                            {"Items": lesson_helper.sendLesson()})

#     if session_state == CONSTANTS.SESSION_STATE_LAUNCH:
#         await asyncio.sleep(0.1)

#     if session_state == CONSTANTS.SESSION_STATE_LESSON_INITIATED:

#         await asyncio.sleep(0.1)

#     if session_state == CONSTANTS.SESSION_STATE_DISCONNECTED:
#         await asyncio.sleep(0.1)



# @app.on_event("startup")
# def startup_event():
#     global p1
#     global session_state
#     global shared_data_queue
#     shared_data_queue = Manager().Queue()
#     p1 = Process(target=env_info_update,
#                 args=(shared_data_queue,))
#     p1.start()
# @app.on_event("shutdown")
# def shutdown_event():
#     global p1
#     p1.terminate()

# @app.sio.event
# async def connect(sid, environ, auth):
#     print('connect ', sid)
#     global session_state
#     # thread = Thread(target=env_info_update, args=())
#     # thread.daemon = True
#     # thread.start()
#     session_state = CONSTANTS.SESSION_STATE_EXPLORE
#     await manageCommunicationWithDevice()


# @app.sio.event
# async def disconnect(sid):
#     global session_state
#     global p1
#     print('disconnect ', sid)

#     session_state = CONSTANTS.SESSION_STATE_DISCONNECTED
#     await manageCommunicationWithDevice()


# @app.sio.on(CONSTANTS.INITIATE_LESSON_REQUEST)
# async def root():
#     global session_state
#     session_state = CONSTANTS.SESSION_STATE_INITIATING_LESSON
#     await manageCommunicationWithDevice()


# @app.sio.on(CONSTANTS.SPEECH_SENTENCE_SPOKEN)
# async def root(sid, data):
#     global session_state
#     if session_state == CONSTANTS.SESSION_STATE_LESSON_INITIATED:
#         lesson_helper.handle_message(str(wit.infer_message(data)))
#     else:
#         print(CONSTANTS.SPEECH_SENTENCE_SPOKEN + data)

# @app.sio.on(CONSTANTS.BUTTON_PRESSED)
# async def root(sid, data):
#     print(data)


# @app.post("/sendData")
# async def root():
#     while True:
#         if context_handler_obj.session.state == CONSTANTS.SESSION_STATE_EXPLORE:
#             data = {"Items": context_handler_obj.env_context.getDefaultParameters()}
#             print(data)
#             await app.sio.emit(CONSTANTS.ENVIRONMENT_OJBECTS_UPDATE, data)
#             time.sleep(1)

#         if context_handler_obj.session.state == CONSTANTS.SESSION_STATE_LAUNCH:
#             pass

#         if context_handler_obj.session.state == CONSTANTS.SESSION_STATE_ONGOING_LESSON:
#             await app.sio.emit(CONSTANTS.LESSON_INIT_INFO,
#                                {"Items": context_handler_obj.env_context.getDefaultParameters()})
#             time.sleep(0.1)

#         if context_handler_obj.session.state == CONSTANTS.SESSION_DISCONNECTED:
#             break


# @app.post("/sendData")
# async def root():
#     await app.sio.emit("env_update",
#                        {"Items": context_handler_obj.env_context.getDefaultParameters()})


# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         global sendDataToHololensBoolean
#         # video_stream_widget.trackMultipleObjects()
#         # topic = await websocket.receive_text()
#         # print(data)
#         # match data:
#         data = sendDataToHololens()
#         #     case "context":
#         #         multipleObjectDetection(hololens2_utilities.getPhoto())
#         #         await asyncio.sleep(1)
#         #data = multipleObjectDetection(hololens2_utilities.getPhoto())

#         # showSurfaceAreaDummyLesson
#         #data = generate_lesson.initiate_curiousityAndSendToHeadset()

#         # Generate Facts
#         #data = descriptive_answering.fact_generator(topic, hololens2_utilites.getPhoto())
#         #data = "asda"
#         # Track objects real timeh
#         #data = returnCurrentImageFromCamera()
#         print("data sent to hololens", str(data))
#         time.sleep(0.01)
#         #data = multipleObjectDetection(returnCurrentImageFromCamera())
#         #data = multipleObjectDetection(hololens2_utilities.getPhoto())

#         await websocket.send_text(f"{data}")
#         sendDataToHololensBoolean = False

# if __name__ == "__main__":
#     main()

# @app.sio.on('join')
# async def handle_join(sid, *args, **kwargs):
#     await app.sio.emit('lobby', 'User joined')


# @app.sio.on('eventName')
# def on_message(data):
#     print('I received a message!', data)
# @app.sio.event
# def connect():
#     print("Connected!!!")
# async def getConcurrentMultipleResults(*args):
#     async with aiohttp.ClientSession() as session:
#         tasks = []
#         for arg in args:
#             tasks.append(arg[0](session, arg[1], arg[2]))
#         result = await asyncio.gather(*tasks)
#     await asyncio.gather()
#     return result


# @app.post("/testMultipleQueries")
# async def root(image: UploadFile):
#     base64_encoded_image = base64.b64encode(image.file.read()).decode('utf-8')
#     return {"data": await getConcurrentMultipleResults(
#         [visual_question_answering.getResultFromHuggingFace,
#             base64_encoded_image, "where is this?"],
#         [visual_question_answering.getResultFromHuggingFace,
#             base64_encoded_image, "what is the activity?"],
#         [visual_question_answering.getResultFromHuggingFace,
#             base64_encoded_image,  "how many people are there?"],
#         [visual_question_answering.getResultFromHuggingFace,
#             base64_encoded_image, "what is the color of the cup"],
#         [visual_question_answering.getResultFromHuggingFace,
#             base64_encoded_image, "where is this?"],
#         [visual_question_answering.getResultFromHuggingFace,
#             base64_encoded_image, "what is the activity?"],
#         [visual_question_answering.getResultFromHuggingFace,
#             base64_encoded_image,  "how many people are there?"],
#         [visual_question_answering.getResultFromHuggingFace,
#             base64_encoded_image, "what is the color of the cup"]

#     )
#     }

def main():
    # while True:
    #     print("Socket thread",shared_data_queue.get())
    #     time.sleep(1)
    # global env_data
    # env_data = shared_data_queue
    #print("this is the shared data", shared_data_queue.get())
    uvicorn.run("main_websockets:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
if __name__ == "__main__":
    main()
    