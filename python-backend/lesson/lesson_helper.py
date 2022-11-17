import json


def initiate_curiousityAndSendToHeadset():
    with open("sample_context.json") as json_file:
        baseContext = json.load(json_file)
    print(baseContext)
    # return lesson content
    with open("concepts/surface_area.json") as lesson_content:
        lesson_object = json.load(lesson_content)
        return json.dumps(lesson_object)


def handle_message(message):
    print(message)
    try:
        for entity in message['entities']['3d_model:3d_model']:
            return entity['body']
    except:
        print("none found")
    return message
    #wit_response_message = json.loads(message)
    # print(wit_response_message)

# # def choose_lesson():
# #     with open("sample_context.json") as json_file:
# #         baseContext = json.load(json_file)
# #     print(baseContext)


# def generate_final_send_to_headset():
