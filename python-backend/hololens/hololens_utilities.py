import requests
import numpy as np
import cv2
import json
import base64
from PIL import Image
from io import BytesIO
#from bs4 import BeautifulSoup

MIXED_REALITY_DEVICE_PORTAL_USERNAME = "acelab"
MIXED_REALITY_DEVICE_PORTAL_PASSWORD = "ace1ace!"
HOLOLENS_IP_ADDR = "http://"+MIXED_REALITY_DEVICE_PORTAL_USERNAME + \
    ":"+MIXED_REALITY_DEVICE_PORTAL_PASSWORD+"@"+"192.168.0.114"

photo_file_list = []


def getPhoto():
    response = requests.post(url=HOLOLENS_IP_ADDR +
                             '/api/holographic/mrc/photo?holo=false&pv=true')
    encoded_file_name = str(base64.b64encode(
        (json.loads(response.text)["PhotoFileName"]).encode('ascii')).decode('ascii'))
    photo_file_list.append(encoded_file_name)
    # print(encoded_file_name)
    response_image = requests.get(
        url=HOLOLENS_IP_ADDR + '/api/holographic/mrc/file?filename=' + encoded_file_name)
    base64_encoded_image = base64.b64encode(response_image.content)
    #open("instagram.png", "wb").write(response_image.content)
    # return response
    #im = Image.open(BytesIO(base64.b64decode(response_image)))
    # print(response_image)
    # im.show()
    return base64_encoded_image


def getMrcSettings():
    response = requests.get(url=HOLOLENS_IP_ADDR +
                            '/api/holographic/mrc/settings')
    print(response.text)
    return response.text

# need to check, doesn't work yet


def setMrcSettings():
    response = requests.post(url=HOLOLENS_IP_ADDR + '/api/holographic/mrc/settings', data=[
                             {"Setting": "PhotoCaptureHeight", "Value": 720}, {"Setting": "PhotoCaptureWidth", "Value": 1280}])
    print(response.text)
    return response.text


def deleteAllPhotos():
    for encoded_file_name in photo_file_list:
        requests.delete(url=HOLOLENS_IP_ADDR +
                        '/api/holographic/mrc/file?filename=' + encoded_file_name)


def streamVideo():
    url = HOLOLENS_IP_ADDR + \
        '/api/holographic/stream/live.mp4?holo=false&pv=true&mic=false&loopback=false&vstab=false&vstabbuffer=0'
    #r = requests.get(url, stream=True)
    vcap = cv2.VideoCapture(url)
    #vcap = cv2.VideoCapture(url)
    while 1:
        # Capture frame-by-frame
        ret, frame = vcap.read()
        # print cap.isOpened(), ret
        if frame is not None:
            # Display the resulting frame
            cv2.imshow('frame', frame)
            # Press q to close the video windows before it ends if you want
            if cv2.waitKey(22) & 0xFF == ord('q'):
                break
        else:
            print("Frame is None")
            break
    # When everything done, release the capture
    vcap.release()
    cv2.destroyAllWindows()
    print("Video stop")
    return "apple"
