import Constants.Values as CONSTANTS
from UserPreferences import Preferences
import api.norfair_utilities as norfair_utilities
import cv2
from api.norfair_utilities import Detection, Paths, Tracker, Video
from norfair.distances import frobenius, iou
from api import multiple_object_detection


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


class env_context():
    def __init__(self, sensor_connection_manager):
        self.user_preferences = Preferences()
        self.obj_detection_manager = multiple_object_detection.norfair_yolo_detection()
        self.sensor_connection_manager = sensor_connection_manager

    def getData(self):
        return self.obj_detection_manager.trackMultipleObjects(
            frame = self.sensor_connection_manager.videoStream.get_current_frame(), 
            pointcloud = self.sensor_connection_manager.videoStream.get_current_point_cloud(),
            sensor="zed"
            )
