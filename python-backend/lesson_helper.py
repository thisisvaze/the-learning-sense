import json
import Constants.Values as CONSTANTS
from api import descriptive_answering, text_to_speech


class lesson_helper_object:
    def __init__(self):
        with open("lessons.json") as lessons:
            self.lessons = json.load(lessons)

    def initiate_curiousityAndSendToHeadset():
        with open("sample_context.json") as json_file:
            baseContext = json.load(json_file)
        print(baseContext)
        # return lesson content
        with open("concepts/surface_area.json") as lesson_content:
            lesson_object = json.load(lesson_content)
            return json.dumps(lesson_object)

    def selectLessonforEnvObject(self, recognized_object_name):
        for lesson in self.lessons:
            for lesson_initiation_object in lesson["objects"]:
                if lesson_initiation_object == recognized_object_name:
                    return lesson["lesson"]
        return "None"

    def sendEnvUpdateWithCuriosity(self, user_pref, data):
        if user_pref['subject'] == 'language':
            return data
        else:
            for recognized_object in data:
                d = self.selectLessonforEnvObject(recognized_object["name"])
                if d != "None":
                    recognized_object["lesson_curiosity_text"] = d["lesson_curiosity_text"]
                else:
                    # need to change it to 0
                    recognized_object["visibility"] = 0
        return data

    def sendSpeechToUnity(query):
        spoken_results = descriptive_answering.wolram_spoken_results(query)
        tts = text_to_speech.tts_fairseq()
        tts.predict(spoken_results)

    def sendLesson(self, lesson_curiosity_text):

        for lesson in self.lessons:
            if lesson_curiosity_text == lesson["lesson"]["lesson_curiosity_text"]:
                return lesson["lesson"]

    def handle_speech_message(self, message, context):
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
                    data = descriptive_answering.openai_text_output(
                        message['text'])
                    # sendSpeechToUnity(message['text'])
                    return {CONSTANTS.DATA_TYPE: "SHOW_FACT", CONSTANTS.DATA_VALUE: data}
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


def main():
    obj = lesson_helper_object()
    obj.sendSpeechToUnity("how far is earth from sun?")


if __name__ == "__main__":
    main()
