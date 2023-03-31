import Constants.Values as CONSTANTS
from UserPreferences import Preferences
import api.norfair_utilities as norfair_utilities
import cv2
from api.norfair_utilities import Detection, Paths, Tracker, Video
import asyncio
from norfair.distances import frobenius, iou
from api import multiple_object_detection
import api.visual_question_answering as vqa
import base64


class session():
    def __init__(self, state=CONSTANTS.SESSION_STATE_LAUNCH):
        self.state = state


class context():
    def __init__(self, sensor_connection_manager):
        self.session = session()
        self.sensor_connection_manager = sensor_connection_manager
        self.env_context = env_context(
            self.sensor_connection_manager, obj_detection=CONSTANTS.RESNET_LOCAL)
        self.user_preferences = Preferences()
        self.session.state = CONSTANTS.SESSION_STATE_EXPLORE


class env_context():
    def __init__(self, sensor_connection_manager, obj_detection=CONSTANTS.NORFAIR_YOLOV7_LOCAL):
        match obj_detection:
            case CONSTANTS.NORFAIR_YOLOV7_LOCAL:
                self.obj_detection_manager = multiple_object_detection.norfair_yolo_detection()
            case CONSTANTS.FB_RESNET50_HF:
                self.obj_detection_manager = multiple_object_detection.fb_resnet_detection_hf()
            case CONSTANTS.RESNET_LOCAL:
                self.obj_detection_manager = multiple_object_detection.resnet_local()
            case CONSTANTS.GCP_CLOUD:
                self.obj_detection_manager = multiple_object_detection.gcp_cloud()
        self.sensor_connection_manager = sensor_connection_manager

    def getDefaultParameters(self):
        self.coordinateData = self.getCoordinatesOfObjectsInEnvironment()
        return self.coordinateData

    def getCoordinatesOfObjectsInEnvironment(self):
        return self.obj_detection_manager.trackMultipleObjects(
            frame=self.sensor_connection_manager.videoStream.get_current_frame(),
            pointcloud=self.sensor_connection_manager.videoStream.get_current_point_cloud()
        )

    # to be implemented later

    async def getSpecialParameters(self, color=True, material=False):
        return await self.getObjectCharacterstics(color, material)

    async def getObjectCharacterstics(self, color, material):
        data = []
        if color:
            await self.getColorsOfObjectsInEnvironment()
        # if material:
        #     await self.getMaterialsOfObjectsInEnvironment()
        # print(data)

    def getColorsOfObjectsInEnvironment(self):
        base64_encoded_image = self.sensor_connection_manager.videoStream.get_current_frame(
            mode="base64")
        asyncio.run(vqa.getConcurrentMultipleResults(base64_encoded_image, [
            "what is the color of cup?", "where is this place?", "what is the color of shirt?", "how many eyes?",
            "what is the color of cup?", "where is this place?", "what is the color of shirt?", "how many eyes?"]))

    def getMaterialsOfObjectsInEnvironment(self):
        retval, buffer = cv2.imencode(
            '.jpg', self.sensor_connection_manager.videoStream.get_current_frame())
        base64_encoded_image = base64.b64encode(buffer)

        return vqa.getConcurrentMultipleResults(base64_encoded_image, ["what is the color of cup?", "where is this place?", "what is happening in this scene?"])
