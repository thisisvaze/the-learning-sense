import argparse
import os
from re import T
from typing import List, Optional, Union
import numpy as np
import torch
import torchvision.ops.boxes as bops
import cv2
from norfair import Detection, Paths, Tracker, Video
from norfair.distances import frobenius, iou


names = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
         'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
         'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
         'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
         'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
         'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
         'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
         'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
         'hair drier', 'toothbrush']

DISTANCE_THRESHOLD_BBOX: float = 0.7
DISTANCE_THRESHOLD_CENTROID: int = 30
MAX_DISTANCE: int = 10000
MIXED_REALITY_DEVICE_PORTAL_USERNAME = "acelab"
MIXED_REALITY_DEVICE_PORTAL_PASSWORD = "ace1ace!"
HOLOLENS_IP_ADDR = "http://"+MIXED_REALITY_DEVICE_PORTAL_USERNAME + \
    ":"+MIXED_REALITY_DEVICE_PORTAL_PASSWORD+"@"+"192.168.0.114"
url = HOLOLENS_IP_ADDR + \
    '/api/holographic/stream/live_low.mp4?holo=false&pv=true&mic=false&loopback=true&vstab=false&vstabbuffer=0'


class YOLO:
    def __init__(self, model_path: str, device: Optional[str] = None):
        if device is not None and "cuda" in device and not torch.cuda.is_available():
            raise Exception(
                "Selected device='cuda', but cuda is not available to Pytorch."
            )
        # automatically set device if its None
        elif device is None:
            device = "cuda:0" if torch.cuda.is_available() else "cpu"

         # load model
        try:
            self.model = torch.hub.load(
                "WongKinYiu/yolov7", "custom", model_path)
        except:
            raise Exception("Failed to load model from {}".format(model_path))

    def __call__(
        self,
        img: Union[str, np.ndarray],
        conf_threshold: float = 0.25,
        iou_threshold: float = 0.45,
        image_size: int = 720,
        classes: Optional[List[int]] = None,
    ) -> torch.tensor:

        self.model.conf = conf_threshold
        self.model.iou = iou_threshold
        if classes is not None:
            self.model.classes = classes
        detections = self.model(img, size=image_size)
        return detections


def center(points):
    return [np.mean(np.array(points), axis=0)]


def yolo_detections_to_norfair_detections(
    yolo_detections: torch.tensor, track_points: str = "centroid"  # bbox or centroid
) -> List[Detection]:
    """convert detections_as_xywh to norfair detections"""
    norfair_detections: List[Detection] = []

    if track_points == "centroid":
        detections_as_xywh = yolo_detections.xywh[0]
        for detection_as_xywh in detections_as_xywh:
            centroid = np.array(
                [detection_as_xywh[0].item(), detection_as_xywh[1].item()]
            )
            scores = np.array([detection_as_xywh[4].item()])
            norfair_detections.append(
                Detection(
                    points=centroid,
                    scores=scores,
                    label=names[int(detection_as_xywh[-1].item())],
                )
            )
    elif track_points == "bbox":
        detections_as_xyxy = yolo_detections.xyxy[0]
        for detection_as_xyxy in detections_as_xyxy:
            bbox = np.array(
                [
                    [detection_as_xyxy[0].item(), detection_as_xyxy[1].item()],
                    [detection_as_xyxy[2].item(), detection_as_xyxy[3].item()],
                ]
            )
            scores = np.array(
                [detection_as_xyxy[4].item(), detection_as_xyxy[4].item()]
            )
            norfair_detections.append(
                Detection(
                    points=bbox, scores=scores, label=names[int(
                        detection_as_xyxy[-1].item())]
                )
            )

    return norfair_detections


# parser = argparse.ArgumentParser(description="Track objects in a video.")
# parser.add_argument(
#     "--detector-path", type=str, default="/custom_models/yolov7-tiny.pt", help="YOLOv7 model path"
# )
# parser.add_argument(
#     "--img-size", type=int, default="240", help="YOLOv7 inference size (pixels)"
# )
# parser.add_argument(
#     "--conf-threshold",
#     type=float,
#     default="0.25",
#     help="YOLOv7 object confidence threshold",
# )
# parser.add_argument(
#     "--iou-threshold", type=float, default="0.45", help="YOLOv7 IOU threshold for NMS"
# )
# parser.add_argument(
#     "--classes",
#     nargs="+",
#     type=int,
#     # default=[33],
#     help="Filter by class: --classes 0, or --classes 0 2 3",
# )
# parser.add_argument(
#     "--device", type=str, default="cuda:0", help="Inference device: 'cpu' or 'cuda'"
# )
# parser.add_argument(
#     "--track-points",
#     type=str,
#     default="centroid",
#     help="Track points: 'centroid' or 'bbox'",
# )
# args = parser.parse_args()


def trackImageData(model, frame, track_points):
   # (status, frame) = capture.read()
    yolo_detections = model(
        frame,
        conf_threshold=0.25,
        iou_threshold=0.45,
        image_size=240,
        classes=[41]
    )
    detections = yolo_detections_to_norfair_detections(
        yolo_detections, track_points=track_points
    )
    # detections[0]
    tracked_objects = tracker.update(detections=detections)
    if args.track_points == "centroid":
        norfair.draw_points(frame, detections)
        norfair.draw_tracked_objects(frame, tracked_objects, draw_labels=True)
    elif args.track_points == "bbox":
        norfair.draw_boxes(frame, detections)
        norfair.draw_tracked_boxes(frame, tracked_objects, draw_labels=True)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        cv2.destroyAllWindows()
        exit(1)
