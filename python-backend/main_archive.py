

# archive api methods and endpoints


# @app.post("/getDepthFromImage")
# def returnThis(image: UploadFile):
#     return getDepthMapFromImage(image)

# def getDepthMapFromImage(image):
#     return {"depth value": depth_estimation.depth_value(image.file)}

# def get3DModelFromEcho3D(query):
#     return {"gltf_url": get_3d_model.from_echo3d(query)}

# def cropPageFromImageVer2(image):
#     return crop.getSketchFromPage(image)


# @app.get("/")
# def hello():
#     return {"message": "Hello TutLinks.com"}


# @app.post("/testMultipleQueries")
# async def root():
#     return {"data": await getConcurrentMultipleResults(
#         [sentiment_analysis.return_sentiment_async, "population of china"],
#         [sentiment_analysis.return_sentiment_async, "how are you?"],
#         [sentiment_analysis.return_sentiment_async, "how are you?"],
#         [sentiment_analysis.return_sentiment_async, "how are you?"],
#         [sentiment_analysis.return_sentiment_async, "how are you?"])
#     }


# @app.get("/getContextualResultAsync")
# async def get_results_async(query, base64_encoded_image) -> dict:
#     return visual_question_answering.getResult(query, base64_encoded_image)


# @app.post("/getBaseContext")
# async def getConcurrentMultipleResults():
#     data: dict = {}
#     base64_encoded_image = hololens2_utilities.getPhoto()
#     await asyncio.gather(get_results_async("where is this?", base64_encoded_image),
#                          get_results_async(
#                              "how many people are there?", base64_encoded_image),
#                          get_results_async("what is the activity?", base64_encoded_image))
#     return data


# @app.post("/getMultipleAnswers")
# async def getConcurrentMultipleResults(*args):
#     async with aiohttp.ClientSession() as session:
#         tasks = []
#         for arg in args:
#             tasks.append(arg[0](session, arg[1]))
#         result = await asyncio.gather(*tasks)
#     await asyncio.gather()
#     return result
