import json
import Constants.Values as CONSTANTS
from api import descriptive_answering, text_to_speech, image_utilities, get_3d_model, text_translate

import nltk
from nltk.corpus import wordnet


class lesson_helper_object:
    def __init__(self):
        with open("lessons.json") as lessons:
            self.lessons = json.load(lessons)
        self.translation_utility = text_translate.translation()

    def add_lesson(self, json_data):
        self.lessons.append(json_data)
        with open("lessons.json", "w") as file:
            json.dump(self.lessons, file)
        return json.dumps(self.lessons)

    def selectSemanticLessonforEnvObject(self, recognized_object_name, user_pref):
        relevant_lessons = []
        for lesson in self.lessons:
            for lesson_initiation_object in lesson["objects"]:
                if lesson_initiation_object == recognized_object_name:
                    relevant_lessons.append(lesson)
        most_relevant_lesson = self.get_lesson_with_highest_semantic_score(
            user_pref["topic"], relevant_lessons)
        return most_relevant_lesson["lesson"]

        # for lesson in self.lessons:
        #     ["relevant_subjects"]["topic"])
        #     for subjects_of_interest in lesson["relevant_subjects"]:
        #         if subjects_of_interest["subject"] == user_pref["subject"]:
        #             for topic_of_interest in subjects_of_interest["topic"]:
        #                 if user_pref["topic"] == topic_of_interest:
        #                     lesson_interest_relevancy = True
        #     for lesson_initiation_object in lesson["objects"]:
        #         if lesson_initiation_object == recognized_object_name and lesson_interest_relevancy:
        #             return lesson["lesson"]
        return "None"

    def selectLessonforEnvObject(self, recognized_object_name, user_pref):
        lesson_interest_relevancy = False
        for lesson in self.lessons:
            for subjects_of_interest in lesson["relevant_subjects"]:
                if subjects_of_interest["subject"] == user_pref["subject"]:
                    for topic_of_interest in subjects_of_interest["topic"]:
                        if user_pref["topic"] == topic_of_interest:
                            lesson_interest_relevancy = True
            for lesson_initiation_object in lesson["objects"]:
                if lesson_initiation_object == recognized_object_name and lesson_interest_relevancy:
                    return lesson["lesson"]
        return "None"

    def sendEnvUpdateWithCuriosity(self, user_pref, data):
        # if user_pref['topic'] == 'language':
        #     for recognized_object in data:
        #         recognized_object["lesson_curiosity_text"] = self.translation_utility.thisText(
        #             recognized_object["name"], user_pref['topic_of_interest'])
        # else:
        for recognized_object in data:
            d = self.selectSemanticLessonforEnvObject(
                recognized_object["name"], user_pref)
            if d != "None":
                recognized_object["lesson_curiosity_text"] = d["lesson_curiosity_text"]
            else:
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

    def sendAIGeneratedLesson(self, title, model):
        panel_title = title
        panel_description = descriptive_answering.openai_text_output(title)
        panel_image = image_utilities.getMatchingImageUrl(title)
        # model = {"model_url": get_3d_model.from_sketchfab(
        #     model), "model_name": model}
        return {"template": "TITLE_DESCRIPTION_IMAGE_MODEL",
                "lesson_id": "100",
                "lesson_curiosity_text": panel_title,
                "title": panel_title,
                "description": panel_description,
                "image_url": panel_image,
                "3d_model": model}

    def handle_speech_message(self, message, context):
        print(message)
        try:
            match message['intents'][0]['name']:
                case CONSTANTS.load_3d_model:
                    return {CONSTANTS.DATA_TYPE: CONSTANTS.SHOW_3D_MODEL, CONSTANTS.DATA_VALUE: message['entities']['3d_model:3d_model'][0]['body']}
                case CONSTANTS.load_ai_generated_lesson:
                    return {CONSTANTS.DATA_TYPE: CONSTANTS.LESSON_INIT_INFO, CONSTANTS.DATA_VALUE: self.sendAIGeneratedLesson(message['entities']['lesson_title:lesson_title'][0]['body'], message['entities']['lesson_title:lesson_title'][0]['entities'][0]['body'])}
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
                    data = descriptive_answering.openai_text_output(
                        message['text'])
                    # sendSpeechToUnity(message['text'])
                    return {CONSTANTS.DATA_TYPE: "SHOW_FACT", CONSTANTS.DATA_VALUE: data}
                    # data = descriptive_answering.wolram_results(
                    #     message['text'])
                    # return {CONSTANTS.DATA_TYPE: "SHOW_FACT", CONSTANTS.DATA_VALUE: data}
                case CONSTANTS.end_lesson:
                    return {CONSTANTS.DATA_TYPE: "MODIFY_LESSON_STATE",  CONSTANTS.DATA_VALUE: "END_LESSON"}
        except:
            return "This case is not handled"

    def get_lesson_with_highest_semantic_score(self, tags, lessons):
        max_score = -1
        best_lesson = None

        # Calculate the semantic score for each lesson
        for lesson in lessons:
            score = 0
            for tag in tags:
                # get the first synset for the tag
                tag_synset = wordnet.synsets(tag)[0]
                # get the synsets for each word in the lesson
                lesson_synsets = [wordnet.synsets(
                    word) for word in lesson["tags"]]
                # flatten the list of synsets
                lesson_synsets = [
                    synset for synsets in lesson_synsets for synset in synsets]
                # Calculate the similarity between the tag and each word in the lesson
                similarities = [tag_synset.path_similarity(
                    lesson_synset) for lesson_synset in lesson_synsets]
                # get the highest similarity, or 0 if no similarities were found
                max_similarity = max(similarities) if any(similarities) else 0
                #score += max_similarity
                if score < max_similarity:
                    score = max_similarity
            # Update the best lesson if this one has a higher score
            if score > max_score:
                max_score = score
                best_lesson = lesson
        print(best_lesson)
        return best_lesson


def main():
    env_dummy_data = [{"lesson_curiosity_text": "What is a plant cell?",
                      "name": "potted plant", "x": 1, "y": 1, "z": 0.1, "visibility": 1}]
    obj = lesson_helper_object()
    # obj.get_lesson_with_highest_semantic_score({"cylinder"})
    obj.sendEnvUpdateWithCuriosity({"topic": "science"}, env_dummy_data)
    #obj.sendSpeechToUnity("how far is earth from sun?")


if __name__ == "__main__":
    main()
