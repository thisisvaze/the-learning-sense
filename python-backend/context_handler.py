import Constants.Values as CONSTANTS
from UserPreferences import Preferences
import api.norfair_utilities as norfair_utilities
import cv2
from api.norfair_utilities import Detection, Paths, Tracker, Video

from norfair.distances import frobenius, iou
from api import multiple_object_detection
import api.visual_question_answering as vqa

import base64


class session():
    def __init__(self, state=CONSTANTS.SESSION_STATE_LAUNCH):
        self.state = state

    def transition_to_state(self, session_state):
        self.state = session_state


class context():
    def __init__(self, sensor_connection_manager):
        self.session = session()
        self.sensor_connection_manager = sensor_connection_manager
        self.env_context = env_context(self.sensor_connection_manager)
        self.user_preferences = Preferences()
        self.session.state = CONSTANTS.SESSION_STATE_EXPLORE


class env_context():
    def __init__(self, sensor_connection_manager):
        self.user_preferences = Preferences()
        self.obj_detection_manager = multiple_object_detection.norfair_yolo_detection()
        self.sensor_connection_manager = sensor_connection_manager

    def getDefaultParameters(self):
        self.coordinateData = self.getCoordinatesOfObjectsInEnvironment()
        return self.coordinateData

    def getSpecialParameters(self, color=True, material=False):
        return self.getObjectCharactersics(self, color, material)

    def getCoordinatesOfObjectsInEnvironment(self):
        return self.obj_detection_manager.trackMultipleObjects(
            frame=self.sensor_connection_manager.videoStream.get_current_frame(),
            pointcloud=self.sensor_connection_manager.videoStream.get_current_point_cloud(),
            sensor="zed"
        )

    def getObjectCharacterstics(self, color, material):
        data = []
        if color:
            self.getColorsOfObjectsInEnvironment()
        if material:
            self.getMaterialsOfObjectsInEnvironment()
        # print(data)

    def getColorsOfObjectsInEnvironment(self):
        retval, buffer = cv2.imencode(
            '.jpg', self.sensor_connection_manager.videoStream.get_current_frame())
        base64_encoded_image = base64.b64encode(buffer)
        return vqa.getConcurrentMultipleResults(base64_encoded_image, ["what is the color of cup?", "where is this place?", "what is happening in this scene?"])

    def getMaterialsOfObjectsInEnvironment(self):
        retval, buffer = cv2.imencode(
            '.jpg', self.sensor_connection_manager.videoStream.get_current_frame())
        base64_encoded_image = base64.b64encode(buffer)

        return vqa.getConcurrentMultipleResults(base64_encoded_image, ["what is the color of cup?", "where is this place?", "what is happening in this scene?"])
