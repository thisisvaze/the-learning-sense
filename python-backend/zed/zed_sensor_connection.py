import Constants.Values as CONSTANTS
import cv2
from threading import Thread
import base64
import time
import sys
import numpy as np
import pyzed.sl as sl
import cv2
import math
from api.norfair_utilities import YOLO, yolo_detections_to_norfair_detections, names
from api.norfair_utilities import Detection, Paths, Tracker, Video
from norfair.distances import frobenius, iou
import Constants
from threading import Thread
import time
import asyncio
import copy
LOG_TAG = "ZED_CONNECTION"
help_string = "[s] Save side by side image [d] Save Depth, [n] Change Depth format, [p] Save Point Cloud, [m] Change Point Cloud format, [q] Quit"
prefix_point_cloud = "Cloud_"
prefix_depth = "Depth_"
path = "./"

count_save = 0
mode_point_cloud = 0
mode_depth = 0
point_cloud_format_ext = ".ply"
depth_format_ext = ".png"


def depth_format_name():
    global mode_depth
    if mode_depth > 2:
        mode_depth = 0
    switcher = {
        0: ".png",
        1: ".pfm",
        2: ".pgm",
    }
    return switcher.get(mode_depth, "nothing")


def save_point_cloud(zed, filename):
    print("Saving Point Cloud...")
    tmp = sl.Mat()
    zed.retrieve_measure(tmp, sl.MEASURE.XYZRGBA)
    saved = (tmp.write(filename + point_cloud_format_ext)
             == sl.ERROR_CODE.SUCCESS)
    if saved:
        print("Done")
    else:
        print("Failed... Please check that you have permissions to write on disk")


def save_depth(zed, filename):
    print("Saving Depth Map...")
    tmp = sl.Mat()
    zed.retrieve_measure(tmp, sl.MEASURE.DEPTH)
    saved = (tmp.write(filename + depth_format_ext) == sl.ERROR_CODE.SUCCESS)
    if saved:
        print("Done")
    else:
        print("Failed... Please check that you have permissions to write on disk")


def save_sbs_image(zed, filename):

    image_sl_left = sl.Mat()
    zed.retrieve_image(image_sl_left, sl.VIEW.LEFT)
    image_cv_left = image_sl_left.get_data()

    image_sl_right = sl.Mat()
    zed.retrieve_image(image_sl_right, sl.VIEW.RIGHT)
    image_cv_right = image_sl_right.get_data()

    sbs_image = np.concatenate((image_cv_left, image_cv_right), axis=1)

    cv2.imwrite(filename, sbs_image)


def process_key_event(zed, key):
    global mode_depth
    global mode_point_cloud
    global count_save
    global depth_format_ext
    global point_cloud_format_ext

    if key == 100 or key == 68:
        save_depth(zed, path + prefix_depth + str(count_save))
        count_save += 1
    elif key == 110 or key == 78:
        mode_depth += 1
        depth_format_ext = depth_format_name()
        print("Depth format: ", depth_format_ext)
    elif key == 112 or key == 80:
        save_point_cloud(zed, path + prefix_point_cloud + str(count_save))
        count_save += 1
    elif key == 109 or key == 77:
        mode_point_cloud += 1
        point_cloud_format_ext = point_cloud_format_name()
        print("Point Cloud format: ", point_cloud_format_ext)
    elif key == 104 or key == 72:
        print(help_string)
    elif key == 115:
        save_sbs_image(zed, "ZED_image" + str(count_save) + ".png")
        count_save += 1
    else:
        a = 0


def print_help():
    print(" Press 's' to save Side by side images")
    print(" Press 'p' to save Point Cloud")
    print(" Press 'd' to save Depth image")
    print(" Press 'm' to switch Point Cloud format")
    print(" Press 'n' to switch Depth format")


class ZedConnectionManager():
    def __init__(self, show_stream):
        self.deviceType = "zed"
        self.videoStream = VideoStream(show_stream, src=0)


class VideoStream():

    def __init__(self, show_stream, src=0):

        # Create a ZED camera object
        self.zed = sl.Camera()

        # Set configuration parameters
        # if len(sys.argv) >= 2:
        #     input_type.set_from_svo_file(sys.argv[1])
        init = sl.InitParameters()
        init.camera_resolution = sl.RESOLUTION.HD720
        init.depth_mode = sl.DEPTH_MODE.PERFORMANCE
        init.coordinate_units = sl.UNIT.METER
        init.depth_stabilization = False

        # Open the camera
        err = self.zed.open(init)
        if err != sl.ERROR_CODE.SUCCESS:
            print(repr(err))
            self.zed.close()
            exit(1)

        # Display help in console
        # print_help()

        # Set runtime parameters after opening the camera
        self.runtime = sl.RuntimeParameters()
        self.runtime.sensing_mode = sl.SENSING_MODE.STANDARD

        # Prepare new image size to retrieve half-resolution images
        self.image_size = self.zed.get_camera_information().camera_resolution
        self.image_size.width = self.image_size.width / 2
        self.image_size.height = self.image_size.height / 2
        # Declare your sl.Mat matrices
        self.image_zed = sl.Mat(
            self.image_size.width, self.image_size.height, sl.MAT_TYPE.U8_C4)

        # self.depth_image_zed = sl.Mat(
        #     self.image_size.width, self.image_size.height, sl.MAT_TYPE.U8_C4)
        self.point_cloud = sl.Mat(
            self.image_size.width, self.image_size.height, sl.MAT_TYPE.F32_C4)
        self.last_updated_point_cloud = sl.Mat(
            self.image_size.width, self.image_size.height, sl.MAT_TYPE.F32_C4)
        self.frame = self.image_zed.get_data()
        # asyncio.get_event_loop().create_task(self.update())
       # Start the thread to read frames from the video stream
        #self.thread = Thread(target=self.update, args=())
        #self.thread.daemon = True
        #self.thread.start()

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            err = self.zed.grab(self.runtime)
            if err == sl.ERROR_CODE.SUCCESS:
                # Retrieve the left image, depth image in the half-resolution
                self.zed.retrieve_image(
                    self.image_zed, sl.VIEW.LEFT, sl.MEM.CPU, self.image_size)
                self.zed.retrieve_measure(
                    self.point_cloud, sl.MEASURE.XYZRGBA, sl.MEM.CPU, self.image_size)
                #self.frame = self.image_zed.get_data()
                #self.last_updated_point_cloud = self.point_cloud.copy()
                #self.last_updated_point_cloud = copy.deepcopy(self.point_cloud)
                print("zed_sensor_connection:" + str(self.point_cloud))
                time.sleep(0.5)

    def get_current_frame(self, mode="opencv"):
        err = self.zed.grab(self.runtime)
        if err == sl.ERROR_CODE.SUCCESS:
            self.zed.retrieve_image(
                self.image_zed, sl.VIEW.LEFT, sl.MEM.CPU, self.image_size)
        if mode == "opencv":
            return self.image_zed.get_data()
        elif mode == "base64":
            retval, buffer = cv2.imencode('.jpg', self.frame)
            jpg_as_text = base64.b64encode(buffer)
            print(jpg_as_text[:80])
            return jpg_as_text

    def get_current_point_cloud(self):
        err = self.zed.grab(self.runtime)
        if err == sl.ERROR_CODE.SUCCESS:
            self.zed.retrieve_measure(
                    self.point_cloud, sl.MEASURE.XYZRGBA, sl.MEM.CPU, self.image_size)
        # return None
        return self.point_cloud

    def show_frame(self):
        image_ocv = self.frame
        # print(depth_image_zed.get_data())
        #depth_image_ocv = self.depth_image_zed.get_data()
        cv2.imshow("Image", image_ocv)
        #cv2.imshow("Depth", depth_image_ocv)
        key = cv2.waitKey(1)
        # process_key_event(key)
        if key == ord('q'):
            cv2.destroyAllWindows()
            self.zed.close()
            exit(1)
