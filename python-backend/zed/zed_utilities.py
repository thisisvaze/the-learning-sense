import sys
import numpy as np
import pyzed.sl as sl
import cv2
import math
from api.norfaird_demo_3 import YOLO, yolo_detections_to_norfair_detections, names
from api.norfaird_demo_3 import Detection, Paths, Tracker, Video
from norfair.distances import frobenius, iou
import Constants
from threading import Thread
import time
help_string = "[s] Save side by side image [d] Save Depth, [n] Change Depth format, [p] Save Point Cloud, [m] Change Point Cloud format, [q] Quit"
prefix_point_cloud = "Cloud_"
prefix_depth = "Depth_"
path = "./"

count_save = 0
mode_point_cloud = 0
mode_depth = 0
point_cloud_format_ext = ".ply"
depth_format_ext = ".png"


DISTANCE_THRESHOLD_BBOX: float = 2
DISTANCE_THRESHOLD_CENTROID: int = 30
MAX_DISTANCE: int = 10000


def point_cloud_format_name():
    global mode_point_cloud
    if mode_point_cloud > 3:
        mode_point_cloud = 0
    switcher = {
        0: ".xyz",
        1: ".pcd",
        2: ".ply",
        3: ".vtk",
    }
    return switcher.get(mode_point_cloud, "nothing")


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


class VideoStreamWidget(object):
    def __init__(self, track_points="bbox"):
        # Create a ZED camera object
        self.zed = sl.Camera()

        # Set configuration parameters
        input_type = sl.InputType()
        if len(sys.argv) >= 2:
            input_type.set_from_svo_file(sys.argv[1])
        init = sl.InitParameters(input_t=input_type)
        init.camera_resolution = sl.RESOLUTION.HD1080
        init.depth_mode = sl.DEPTH_MODE.PERFORMANCE
        init.coordinate_units = sl.UNIT.MILLIMETER

        # Open the camera
        err = self.zed.open(init)
        if err != sl.ERROR_CODE.SUCCESS:
            print(repr(err))
            self.zed.close()
            exit(1)

        # Display help in console
        print_help()

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
        self.depth_image_zed = sl.Mat(
            self.image_size.width, self.image_size.height, sl.MAT_TYPE.U8_C4)
        self.point_cloud = sl.Mat()

        key = ' '
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
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            err = self.zed.grab(self.runtime)
            if err == sl.ERROR_CODE.SUCCESS:
                # Retrieve the left image, depth image in the half-resolution
                self.zed.retrieve_image(
                    self.image_zed, sl.VIEW.LEFT, sl.MEM.CPU, self.image_size)
                self.zed.retrieve_image(self.depth_image_zed, sl.VIEW.DEPTH,
                                        sl.MEM.CPU, self.image_size)
                # Retrieve the RGBA point cloud in half resolution
                self.zed.retrieve_measure(
                    self.point_cloud, sl.MEASURE.XYZRGBA, sl.MEM.CPU, self.image_size)
                time.sleep(.01)

    def trackMultipleObjects(self):
        # (status, frame) = capture.read()
        yolo_detections = self.model(
            self.image_zed.get_data(),
            conf_threshold=0.25,
            iou_threshold=0.45,
            image_size=480,
            #classes=[names.index("potted plant")]
            # classes=[32]
            # classes=[41]
        )
        detections = yolo_detections_to_norfair_detections(
            yolo_detections, track_points=self.track_points
        )
        # detections[0]
        tracked_objects = self.tracker.update(detections=detections)
        if self.track_points == "centroid":
            norfaird_demo_3.draw_points(self.frame, detections)
            norfaird_demo_3.draw_tracked_objects(
                self.frame, tracked_objects, draw_labels=True)
        elif self.track_points == "bbox":
            norfaird_demo_3.draw_boxes(self.frame, detections)
            norfaird_demo_3.draw_tracked_boxes(
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

    def show_frame(self):
        # To recover data from sl.Mat to use it with opencv, use the get_data() method
        # It returns a numpy array that can be used as a matrix with opencv
        image_ocv = self.image_zed.get_data()
        # print(depth_image_zed.get_data())
        depth_image_ocv = self.depth_image_zed.get_data()
        # x1 = 200
        # x2 = 600
        # y1 = 100
        # y2 = 400
        # avg_depth = 0
        # for x in range(x1,x2):
        #     for y in range(y1,y2):
        #         err, depth_value = depth_image_zed.get_value(x, y)
        #         avg_depth+=depth_value[0]
        #         y+=50
        #     x+=50
        # avg_depth = avg_depth/round(((x2-x1)/10)*((y2-y1)/10))

        #print(avg_depth, end="\r")
# Get and print distance value in mm at the center of the image
# We measure the distance camera - object using Euclidean distance

        # x = round(self.image_zed.get_width() / 2)
        # y = round(self.image_zed.get_height() / 2)
        # err, point_cloud_value = self.point_cloud.get_value(x, y)
        # distance = math.sqrt(point_cloud_value[0] * point_cloud_value[0] +
        #                      point_cloud_value[1] * point_cloud_value[1] +
        #                      point_cloud_value[2] * point_cloud_value[2])
        # print("Distance to Camera at ({0}, {1}): {2} mm".format(
        #     x, y, distance), end="\r")

        # x = round(image_zed.get_width() / 2)
        # y = round(image_zed.get_height() / 2)
        # err, depth_value = depth_image_zed.get_value(x, y)
        # print(x,y,depth_value[0], end="\r")
        #print("Distance to Camera at ({0}, {1}): {2} mm".format(x, y, depth_value), end="\r")
        # Get the 3D point cloud values for pixel (i,j)
        #point3D = point_cloud.get_value(200,200)
        #x = point3D[0]
        #y = point3D[1]
        #z = point3D[2]
        #color = point3D[3]
        # print(str(point3D))
        cv2.imshow("Image", image_ocv)
        cv2.imshow("Depth", depth_image_ocv)

        key = cv2.waitKey(1)
        # process_key_event(key)
        if key == ord('q'):
            cv2.destroyAllWindows()
            self.zed.close()
            exit(1)


if __name__ == "__main__":
    video_stream_widget = VideoStreamWidget()
    while True:
        video_stream_widget.show_frame()
