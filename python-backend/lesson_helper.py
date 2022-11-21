import json
import Constants.Values as CONSTANTS
from api import descriptive_answering


def initiate_curiousityAndSendToHeadset():
    with open("sample_context.json") as json_file:
        baseContext = json.load(json_file)
    print(baseContext)
    # return lesson content
    with open("concepts/surface_area.json") as lesson_content:
        lesson_object = json.load(lesson_content)
        return json.dumps(lesson_object)


def sendLesson(object):
    print(object)
    match object:
        case "cup":
            return {"text": "What is Pi?",
                    "image_url": "https://i0.wp.com/team-cartwright.com/wp-content/uploads/2021/02/definition-of-pi-1.png",
                    "3d_model": "circle"}
        case "potted plant":
            return {"text": "Plant Cell",
                    "image_url": "https://ez002.k12.sd.us/labs/plant.jpg",
                    "3d_model": "plantcell"}
        case "chair":
            return {"text": "Mars",
                    "image_url": "https://osr.org/wp-content/uploads/2021/01/11-01Instagram-Post-Infographic-1.jpg",
                    "3d_model": "mars"}

    return {"text": "What is Pi?",
                    "image_url": "https://i0.wp.com/team-cartwright.com/wp-content/uploads/2021/02/definition-of-pi-1.png",
                    "3d_model": "circle"}


def handle_speech_message(message, context):
    print(message)
    try:
        match message['intents'][0]['name']:
            case CONSTANTS.load_3d_model:
                return {CONSTANTS.DATA_TYPE: "SHOW_3D_MODEL", CONSTANTS.DATA_VALUE: message['entities']['3d_model:3d_model'][0]['body']}

            case CONSTANTS.modify_user_preferences:
                match message['traits']['subject'][0]['value']:
                    case "language":
                        context.user_preferences.set(
                            {"subject": message['traits']['subject'][0]['value'], "topic_of_interest": message['entities']['topic_of_interest:topic_of_interest'][0]['body']})
                    case "science":
                        context.user_preferences.set(
                            {"subject": message['traits']['subject'][0]['value'], "topic_of_interest": "plants"})
                    case "mathematics":
                        context.user_preferences.set(
                            {"subject": message['traits']['subject'][0]['value'], "topic_of_interest": "volume"})

                return {CONSTANTS.DATA_TYPE: "SPEECH_HANDLED_IN_SERVER", CONSTANTS.DATA_VALUE: str(context.user_preferences.data)}

            case CONSTANTS.descriptive_query:
                return {CONSTANTS.DATA_TYPE: "SPEECH_HANDLED_IN_SERVER", CONSTANTS.DATA_VALUE: "DESCRIPTIVE QUERY"}
            case CONSTANTS.fact_query:
                data = descriptive_answering.wolram_results(
                    message['text'])
                return {CONSTANTS.DATA_TYPE: "SHOW_FACT", CONSTANTS.DATA_VALUE: data}
    except:
        return "This case is not handled"
    # wit_response_message = json.loads(message)
    # print(wit_response_message)

# # def choose_lesson():
# #     with open("sample_context.json") as json_file:
# #         baseContext = json.load(json_file)
# #     print(baseContext)


# def generate_final_send_to_headset():
