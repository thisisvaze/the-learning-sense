from hololens import hololens_connection, hololens_utilities
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


def main():
    hololens_connection_manager = hololens_connection.HololensConnectionManager(
        show_stream=False)
    obj_detection_manager = multiple_object_detection.norfair_yolo_detection()
    print(hololens_connection_manager.ip_address)
    while True:
        # hololens_connection_manager.videoStream.show_frame()
        current_frame = hololens_connection_manager.videoStream.get_current_frame(
            mode="opencv")
        obj_detection_manager.trackMultipleObjects(current_frame)
        # multiple_object_detection.trackMultipleObjects(current_frame)


if __name__ == "__main__":
    main()
