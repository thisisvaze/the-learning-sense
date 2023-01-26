from re import T
import json
from . import depth_estimation
#from google.cloud import vision
import copy
import math
import base64
import requests
from api.norfair_utilities import YOLO, yolo_detections_to_norfair_detections, names
from . import norfair_utilities
import cv2
import Constants.Values as CONSTANTS
from api.norfair_utilities import Detection, Paths, Tracker, Video
from norfair.distances import frobenius, iou
import norfair
import api.translate_text as lang_translator
DISTANCE_THRESHOLD_BBOX: float = 2
DISTANCE_THRESHOLD_CENTROID: int = 30
MAX_DISTANCE: int = 10000


class norfair_yolo_detection(object):
    def __init__(self, track_points="bbox"):
        self.track_points = track_points
        self.model = YOLO(CONSTANTS.YOLO_V7_MODEL_PATH)
        distance_function = iou if track_points == "bbox" else frobenius
        distance_threshold = (
            DISTANCE_THRESHOLD_BBOX
            if track_points == "bbox"
            else DISTANCE_THRESHOLD_CENTROID
        )
        self.tracker = Tracker(
            distance_function=distance_function,
            distance_threshold=distance_threshold
            # hit_counter_max=100
        )

    def trackMultipleObjects(self, frame, sensor, pointcloud=None, language="English", gaze_coordinates="(0,0,0)"):
        #gaze_coordinates = gaze_coordinates.lstrip('(').rstrip(')').split(',')
        try:
            translator_utility = lang_translator.translation()
        except:
            language = "English"

        # (status, frame) = capture.read()
        yolo_detections = self.model(
            frame,
            conf_threshold=0.25,
            iou_threshold=0.45,
            image_size=480,
            # classes=[names.index("cup")]
            # classes=[32]
            # classes=[41]
        )
        detections = yolo_detections_to_norfair_detections(
            yolo_detections, track_points=self.track_points
        )
        # detections[0]
        tracked_objects = self.tracker.update(detections=detections)
        if self.track_points == "centroid":
            norfair.draw_points(frame, detections)
            norfair.draw_tracked_objects(
                frame, tracked_objects, draw_labels=True)
        elif self.track_points == "bbox":
            norfair.draw_boxes(frame, detections)
            norfair.draw_tracked_boxes(
                frame, tracked_objects, draw_labels=True)
        if sensor == "hololens":
            returnString = []
            closestObjectDistance = 100
            for tracked_object in tracked_objects:
                det = tracked_object.last_detection
                print(gaze_coordinates[0])
                print(gaze_coordinates[1])
                factor = 0.8
                d = math.pow((((det.points[0][0]+det.points[1][0])/432)-1)*factor - float(gaze_coordinates[0]), 2) + math.pow(
                    (((det.points[0][1]+det.points[1][1])/240)-1)*factor - float(gaze_coordinates[1]), 2)

                if (d < closestObjectDistance):
                    returnString.clear()
                    if language == "English":
                        returnString.append(
                            {"id": tracked_object.id, "name": det.label, "x": ((det.points[0][0]/216)-1)*factor, "y": (1-(det.points[0][1]/120))*0.5, "visibility": 1})
                    else:
                        returnString.append(
                            {"id": tracked_object.id, "name": translator_utility.thisText(det.label, language), "x": ((det.points[0][0]/216)-1)*factor, "y": (1-(det.points[0][1]/120))*0.5, "visibility": 1})

                # print(det.points)

                # z_index = (500*500)/int((int(det.points[1][0]-det.points[0][0])) *
                #                       (int(det.points[1][1]-det.points[0][1])))
                # cv2.putText(frame, str(int(det.points[0][0]))+", "+str(int(det.points[0][1]))+", "+str(z_index), (50, 50),
                #            cv2.FONT_HERSHEY_SIMPLEX, 2, 255)

                #result = translator.translate_text("Hello, world!", target_lang="FR")
                # print(result.text)  # "Bonjour, le monde !"
            print(det.label, d)

        if sensor == "zed":
            returnString = []
            try:
                for tracked_object in tracked_objects:
                    det = tracked_object.last_detection
                    x1 = int(det.points[0][0])
                    x2 = int(det.points[1][0])
                    y1 = int(det.points[0][1])
                    y2 = int(det.points[1][1])
                    point3D = pointcloud.get_value((x1+x2)/2, (y1+y2)/2)
                    # print(point3D)
                    round_off_param = 2
                    #returnString.append({"name": det.label})
                    if language == "English":
                        returnString.append(
                            {"id": tracked_object.id, "name": det.label, "x": -round(point3D[1][0], round_off_param), "y": -round(point3D[1][1], round_off_param),  "z": -round(point3D[1][2], round_off_param), "visibility": 1})

                    else:
                        returnString.append(
                            {"id": tracked_object.id, "name": det.label, "x": -round(point3D[1][0], round_off_param), "y": -round(point3D[1][1], round_off_param),  "z": -round(point3D[1][2], round_off_param), "visibility": 1})

            except:
                returnString.append(
                    {"name": "lost track"})

        cv2.imshow("Frame", frame)
        #print("multiple_object_detection:" + str(returnString))
        key = cv2.waitKey(1)
        if key == ord('q'):
            cv2.destroyAllWindows()
            exit(1)
        # print(returnString)
        return returnString


def facebook_resnet_localize_objects(base64_encoded_image):
    API_TOKEN = "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"
    API_URL = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    response = requests.request(
        "POST", API_URL, headers=headers, data=base64.b64decode(base64_encoded_image))
    data = []
    print(response)
    for result in json.loads(response.content.decode("utf-8")):
        print(result)
        # for hololens images
        # data.append({"name": result["label"], "x": (
        # result["box"]["xmin"] + result["box"]["xmax"]) / 2560, "y": result["box"]["ymin"]/720})
        data.append({"name": result["label"], "x": (
            result["box"]["xmin"] + result["box"]["xmax"]) / 856, "y": result["box"]["ymin"]/240})

    return data

# def gcp_localize_objects(base64_encoded_image):
#     data = []
#     text = ""
#     client = vision.ImageAnnotatorClient()
#     image_from_vision = vision.Image(content=base64.b64decode(base64_encoded_image) )
#     objects = client.object_localization(
#         image=image_from_vision).localized_object_annotations
#     #getting depthestimation data
#     #depth_image = depth_estimation.depth_value(apple_content)
#     #print(depth_image)
#     print('Number of objects found: {}'.format(len(objects)))
#     i=0
#     for object_ in objects:
#         text = text + " " + object_.name
#         data.append({"name": object_.name, "x": str((object_.bounding_poly.normalized_vertices[0].x + object_.bounding_poly.normalized_vertices[1].x) / 2), "y": str((object_.bounding_poly.normalized_vertices[0].y + object_.bounding_poly.normalized_vertices[2].y) / 2)})
#         i+=1
#         print('\n{} (confidence: {})'.format(object_.name, object_.score))
#         print('Normalized bounding polygon vertices: ')
#         for vertex in object_.bounding_poly.normalized_vertices:
#             print(' - ({}, {})'.format(vertex.x, vertex.y))
#     json_data = json.dumps(data)
#     return data
