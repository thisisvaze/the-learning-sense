import json


def initiate_curiousityAndSendToHeadset():
    with open("sample_context.json") as json_file:
        baseContext = json.load(json_file)
    print(baseContext)
    # return lesson content
    with open("concepts/surface_area.json") as lesson_content:
        lesson_object = json.load(lesson_content)
        return json.dumps(lesson_object)

# # def choose_lesson():
# #     with open("sample_context.json") as json_file:
# #         baseContext = json.load(json_file)
# #     print(baseContext)


# def generate_final_send_to_headset():
