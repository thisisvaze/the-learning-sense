from asyncio import constants
from pickle import GLOBAL
from fastapi_socketio import SocketManager
from email.mime import image
from fastapi import FastAPI, UploadFile, WebSocket, File
from matplotlib.pyplot import get
from sympy import Q
import api.ocr_recognition as ocr_recognition
import descriptive_answering
import plant_recognition
import multiple_object_detection
import depth_estimation
import get_3d_model
import sketch_recognition
import hololens2_utilities
import visual_question_answering
import generate_lesson
import sentiment_analysis
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


DISTANCE_THRESHOLD_BBOX: float = 2
DISTANCE_THRESHOLD_CENTROID: int = 30
MAX_DISTANCE: int = 10000


OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.legacy.TrackerCSRT_create,
    "kcf": cv2.legacy.TrackerKCF_create,
    "boosting": cv2.legacy.TrackerBoosting_create,
    "mil": cv2.legacy.TrackerMIL_create,
    "tld": cv2.legacy.TrackerTLD_create,
    "medianflow": cv2.legacy.TrackerMedianFlow_create,
    "mosse": cv2.legacy.TrackerMOSSE_create
}


class VideoStreamWidget(object):
    def __init__(self, src=1, track_points="bbox"):
        self.track_points = track_points
        self.model = YOLO("custom_models/yolov7.pt")
        distance_function = iou if track_points == "bbox" else frobenius
        distance_threshold = (
            DISTANCE_THRESHOLD_BBOX
            if track_points == "bbox"
            else DISTANCE_THRESHOLD_CENTROID
        )
        self.tracker = Tracker(
            distance_function=distance_function,
            distance_threshold=distance_threshold,
            hit_counter_max=100
        )

        url = Constants.Values.HOLOLENS_IP_ADDR + \
            '/api/holographic/stream/live_low.mp4?holo=false&pv=true&mic=true&loopback=true&vstab=false&vstabbuffer=0'
        # r = requests.get(url, stream=True)
        self.capture = cv2.VideoCapture(url)
        #self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
        #self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
        width = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(width, height)
        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def trackMultipleObjects(self):
        # (status, frame) = capture.read()
        yolo_detections = self.model(
            self.frame,
            conf_threshold=0.25,
            iou_threshold=0.45,
            image_size=480,
            classes=[names.index("potted plant")]
            # classes=[32]
            # classes=[41]
        )
        detections = yolo_detections_to_norfair_detections(
            yolo_detections, track_points=self.track_points
        )
        # detections[0]
        tracked_objects = self.tracker.update(detections=detections)
        if self.track_points == "centroid":
            norfair_utilities.draw_points(self.frame, detections)
            norfair_utilities.draw_tracked_objects(
                self.frame, tracked_objects, draw_labels=True)
        elif self.track_points == "bbox":
            norfair_utilities.draw_boxes(self.frame, detections)
            norfair_utilities.draw_tracked_boxes(
                self.frame, tracked_objects, draw_labels=True)

        returnString = []
        for det in detections:
            # print(det.points)
            factor = 0.8
            z_index = (500*500)/int((int(det.points[1][0]-det.points[0][0])) *
                                    (int(det.points[1][1]-det.points[0][1])))
            cv2.putText(self.frame, str(int(det.points[0][0]))+", "+str(int(det.points[0][1]))+", "+str(z_index), (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, 255)

            returnString.append(
                {"name": det.label, "x": ((det.points[0][0]/216)-1)*factor, "y": (1-(det.points[0][1]/120))*0.5})
        cv2.imshow("Frame", self.frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            cv2.destroyAllWindows()
            exit(1)
        print(returnString)
        return returnString

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
            # time.sleep(.01)

    def show_frame(self):
        # Display frames in main program
        cv2.imshow('frame', self.frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            self.capture.release()
            cv2.destroyAllWindows()
            exit(1)

    def base64_encoded_current_image_from_camera(self):
        # Display frames in main program
        # cv2.imshow('frame', self.frame)
        retval, buffer = cv2.imencode('.jpg', self.frame)
        jpg_as_text = base64.b64encode(buffer)
        print(jpg_as_text[:80])
        return jpg_as_text


def returnCurrentImageFromCamera():
    return {"Items": video_stream_widget.trackMultipleObjects()}


video_stream_widget = VideoStreamWidget()
# time.sleep(2)
# returnCurrentImageFromCamera()


app = FastAPI()

time.sleep(3)
# web socket
# while True:
#     returnCurrentImageFromCamera()


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

        # Track objects real time
        data = {"Items": video_stream_widget.trackMultipleObjects()}
        #data = returnCurrentImageFromCamera()
        # time.sleep(0.01)
        #data = multipleObjectDetection(returnCurrentImageFromCamera())
        #data = multipleObjectDetection(hololens2_utilities.getPhoto())
        await websocket.send_text(f"{data}")


@app.post("/getFactForObject")
def getFactForObject(topic: str):
    # return {"answer": descriptive_answering.openai_text_output(query)}
    return descriptive_answering.fact_generator(topic)

# socket_manager = SocketManager(app=app)


# @app.sio.on('join')
# async def handle_join(sid, *args, **kwargs):
#     await app.sio.emit('lobby', 'User joined')


# @app.sio.on('message')
# async def print_message(sid, message):
#     # When we receive a new event of type
#     # 'message' through a socket.io connection
#     # we print the socket ID and the message
#     print("Socket ID: ", sid)
#     print(message)


# @app.sio.emit('sendlesson', {'data': generate_lesson.initiate_curiousityAndSendToHeadset()})

@app.post("/getLesson")
def root():
    # return {"answer": descriptive_answering.openai_text_output(query)}
    return generate_lesson.initiate_curiousityAndSendToHeadset()


@app.post("/recognizeText")
def root(image: UploadFile):
    return ocr_recognition.get_text_from_image(image.file)


@app.post("/getContextualResult")
def root(query: str, image: str):
    # return {"answer": descriptive_answering.openai_text_output(query)}
    return {"updated": visual_question_answering.getResult(query, hololens2_utilities.getPhoto())}


# @app.post("/shakalakaboomboom")
# def root():
#     return get3DModelFromLocalDatabase(preditObjectFromSketch(cropPageFromImage(hololens2_utilities.getPhoto())))


@app.get("/captureImage")
def root():
    return {"base64_encoded_image": hololens2_utilities.getPhoto()}


@app.get("/getTextAnswer")
def root(query: str):
    # return {"answer": descriptive_answering.openai_text_output(query)}
    return {"answer": descriptive_answering.wolram_results(query)}


@app.websocket("/speechRecognition")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        speechData = await websocket.receive_text()
        print(speechData)


@app.post("/translateText")
def root(query: str, language: str):
    return "null"


@app.get("/deletePhotos")
def root():
    return hololens2_utilities.deleteAllPhotos()


@app.get("/testApis")
def root():
    hololens2_utilities.setMrcSettings()
    return {"getting it": hololens2_utilities.getMrcSettings()}


@app.get("/livePreview")
def streamVideoFromHololens():
    return {"getting it": hololens2_utilities.streamVideo()}


@app.post("/objectDetectionCamera")
def root():
    return multipleObjectDetection(returnCurrentImageFromCamera())


@app.post("/objectDetection")
def root():
    return multipleObjectDetection(hololens2_utilities.getPhoto())


@app.post("/receiveContext")
def read_item(image: UploadFile):
    return multipleObjectDetection(image)


@app.post("/get3DModel")
def returnThis(query: str):
    return get3DModelFromLocalDatabase(query)


@app.post("/predictObjectFromSketch")
def read_item(image: UploadFile):
    return preditObjectFromSketch(image)


# helper functions


def multipleObjectDetection(base64_encoded_image):
    return {"Items": multiple_object_detection.facebook_resnet_localize_objects(base64_encoded_image)}
    # return { "Items": multiple_object_detection.gcp_localize_objects(base64_encoded_image)}


def getPlantName(image):
    return {"plant_name": plant_recognition.get_plant_name(image.file)}


def getPlantNameNew(image):
    return {"plant_name": plant_recognition.get_plant_name_2(image.file)}


def getTextFromImage(image):
    return {"text": ocr_recognition.get_text_from_image(image.file)}


def get3DModelFromLocalDatabase(query):
    return {"Items": get_3d_model.from_local_hololens_database(query)}


def preditObjectFromSketch(image):
    return sketch_recognition.sketch_predicted_object(image)
