import cv2
from threading import Thread
import base64
import time
import numpy as np
import pyzed.sl as sl
import cv2
from threading import Thread
import time
import sys


import pykinect_azure as pykinect
from pykinect_azure import K4A_CALIBRATION_TYPE_COLOR, K4A_CALIBRATION_TYPE_DEPTH, k4a_float2_t


class KinectConnectionManager():
    def __init__(self):
        self.deviceType = "kinect"
        self.videoStream = VideoStream()


class VideoStream():

    class pcclass():
        def __init__(self, device):
            self.device = device
            pass

        def update_capture(self, capture):
            self.capture = capture

        def get_value(self, x, y):

            ret_depth, transformed_depth_image = self.capture.get_transformed_depth_image()
            rgb_depth = transformed_depth_image[y, x]
            pixels = k4a_float2_t((x, y))
            # pos3d_color = device.calibration.convert_2d_to_3d(
            #     pixels, rgb_depth, K4A_CALIBRATION_TYPE_COLOR, K4A_CALIBRATION_TYPE_COLOR)
            pos3d_depth = self.device.calibration.convert_2d_to_3d(
                pixels, rgb_depth, K4A_CALIBRATION_TYPE_COLOR, K4A_CALIBRATION_TYPE_COLOR)

            return pos3d_depth

    def __init__(self):

       # Initialize the library, if the library is not found, add the library path as argument
        pykinect.initialize_libraries()

        # Modify camera configuration
        device_config = pykinect.default_configuration
        device_config.color_format = pykinect.K4A_IMAGE_FORMAT_COLOR_BGRA32
        device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_720P
        device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED
        # print(device_config)

        # Start device
        self.device = pykinect.start_device(config=device_config)
        self.pointcloud = self.pcclass(self.device)
        capture = self.device.update()
        self.pointcloud.update_capture(capture)
        ret_color, self.frame = capture.get_color_image()
        # asyncio.get_event_loop().create_task(self.update())
       # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            # Get capture
            capture = self.device.update()
            self.pointcloud.update_capture(capture)
            # Get the color image from the capture
            ret_color, self.frame = capture.get_color_image()

            # # Get the colored depth
            # ret_depth, transformed_depth_image = capture.get_transformed_depth_image()

            # if not ret_color or not ret_depth:
            #     continue

            # pix_x = self.frame.shape[1] // 2
            # pix_y = self.frame.shape[0] // 2
            # rgb_depth = transformed_depth_image[pix_y, pix_x]

            # pixels = k4a_float2_t((pix_x, pix_y))

            # # pos3d_color = device.calibration.convert_2d_to_3d(
            # #     pixels, rgb_depth, K4A_CALIBRATION_TYPE_COLOR, K4A_CALIBRATION_TYPE_COLOR)
            # pos3d_depth = self.device.calibration.convert_2d_to_3d(
            #     pixels, rgb_depth, K4A_CALIBRATION_TYPE_COLOR, K4A_CALIBRATION_TYPE_DEPTH)

            # print(pos3d_depth)
            # print(
            #     f"RGB depth: {rgb_depth}, RGB pos3D: {pos3d_color}, Depth pos3D: {pos3d_depth}")

            # Overlay body segmentation on depth image
            cv2.imshow('Transformed Color Image', self.frame)
            # err = self.zed.grab(self.runtime)
            # if err == sl.ERROR_CODE.SUCCESS:
            #     # Retrieve the left image, depth image in the half-resolution
            #     self.zed.retrieve_image(
            #         self.image_zed, sl.VIEW.LEFT, sl.MEM.CPU, self.image_size)
            #     self.zed.retrieve_measure(
            #         self.point_cloud, sl.MEASURE.XYZRGBA, sl.MEM.CPU, self.image_size)
            #     self.frame = self.image_zed.get_data()
            #     #self.last_updated_point_cloud = self.point_cloud.copy()
            #     #self.last_updated_point_cloud = copy.deepcopy(self.point_cloud)
            #     #print("zed_sensor_connection:" + str(self.point_cloud))
            #     # self.show_frame()
            time.sleep(1)

    def get_current_frame(self, mode="opencv"):
        if mode == "opencv":
            return self.frame
        elif mode == "base64":
            retval, buffer = cv2.imencode('.jpg', self.frame)
            jpg_as_text = base64.b64encode(buffer)
            print(jpg_as_text[:80])
            return jpg_as_text

    def get_current_point_cloud(self):
        return self.pointcloud

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


if __name__ == "__main__":
    ZedConnectionManager(show_stream=0)
