from re import T
import json
import depth_estimation
#from google.cloud import vision
import copy
import base64
import requests


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
