import Constants.Values as CONSTANTS
import cv2
from threading import Thread
import base64
import time

LOG_TAG = "HOLOLENS_CONNECTION"


class HololensConnectionManager():
    def __init__(self, show_stream):
        self.deviceType = "hololens"
        self.ip_address = CONSTANTS.HOLOLENS_IP_ADDRESS
        self.videoStream = VideoStream(show_stream, src=0)
        print(LOG_TAG, "Connected to Hololens at: " + self.ip_address)


class VideoStream():

    def __init__(self, show_stream, src=0):
        url = CONSTANTS.HOLOLENS_URL + \
            '/api/holographic/stream/live_low.mp4?holo=false&pv=true&mic=true&loopback=true&vstab=false&vstabbuffer=0'
        # r = requests.get(url, stream=True)

        # Using Hololens 2 camera
        #self.capture = cv2.VideoCapture(url)

        # Test with laptop's internal came
        # ra
        self.capture = cv2.VideoCapture(0)

        #self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
        #self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
        width = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(width, height)
        (self.status, self.frame) = self.capture.read()
        # Start the thread to read frames from the video stream
        # self.thread = Thread(target=self.update, args=())
        # self.thread.daemon = True
        # self.thread.start()
        if (show_stream):
            while True:
                if self.capture.isOpened():
                    (self.status, self.frame) = self.capture.read()
                    self.show_stream()
                    break

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
            time.sleep(.01)

    def show_frame(self):
        # Display frames in main program
        cv2.imshow('frame', self.frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            self.capture.release()
            cv2.destroyAllWindows()
            exit(1)

    def show_stream(self):
        while True:
            if self.capture.isOpened():
                self.show_frame()

    def get_current_frame(self, mode="opencv"):
        if mode == "opencv":
            return self.frame
        elif mode == "base64":
            retval, buffer = cv2.imencode('.jpg', self.frame)
            jpg_as_text = base64.b64encode(buffer)
            print(jpg_as_text[:80])
            return jpg_as_text

    def get_current_point_cloud(self):
        return None
