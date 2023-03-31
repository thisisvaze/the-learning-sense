import math
import os
import openai
import json
import requests
import urllib.parse

OPENAI_API_KEY_OLD = "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"
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

WOLFRAM_API_KEY = "TT3P62-W479LAP7E3"


def openai_text_output(query):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful teacher."},
                  {"role": "user", "content": query + ". Provide an answer under 140 characters"}]
    )
    return response["choices"][0]["message"]["content"].replace('\"', '').replace('\'', '').replace('\n', '')


def openai_end_to_end_gpt(query):
    try:
        system_query = " You are CuriosityXR, an educational XR App's API. Do not return in plain text. Always Return in JSON only. The JSON response based on the following conditions.\r\n1. If the user wants to clear the space or delete everything, return {\"intent_name\": \"CLEAR_SPACE\"}.\r\n2. If the user says precisely that they are curious about a topic x, return {\"intent_name\": \"MODIFY_USER_PREFERENCES\", \"topic\": x}.\r\n4. If the user has a learning query, return {\"intent_name\": \"INTERACTIVE_QUERY_RESPONSE\", \"info\": {\"learning_content_answer\": [short_answer], \"sketchfab_model_object_name\": [object_name], \"image_name\": [image_name] if [image_name] else None}}. Always have a model whenever user asks to see it or whenever its possible to help user visualize. If no model is needed, return  sketchfab_model_object_name as null. If no image is needed, set \"image_name\" to null. Replace underscores with spaces in all values. learning_content_answer must be strictly less than 140 characters."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_query},
                      {"role": "user", "content": query}]
        )
        res = response["choices"][0]["message"]["content"].replace('\'', '')
        print(res)
        json_response = json.loads(res)
        return json_response
    except:
        return "no gpt response"


def openai_direct_lesson_generation(object_name, preference_topic):
    query = "Return only a JSON. Teach me an interesting short lesson that teaches me something about " + preference_topic + " related to " + object_name + \
        ". Return 4 parameters, lesson_question_title, learning_content (strictly < 140 characters), sketchfab_model_name (to add concept support visualization related to " + \
        preference_topic + \
            ", and image_name (without extensions). Replace underscore by space for sketchfab_model_name. Do not add explanatory text. Don't include hashtags."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": query}]
    )
    res = response["choices"][0]["message"]["content"]
    json_response = json.loads(res)
    json_response["description"] = json_response.pop("learning_content")
    json_response["title"] = json_response.pop("lesson_question_title")
    json_response["3d_model"] = json_response.pop("sketchfab_model_name")
    return json_response


def fact_generator(topic, object_name):
    print("generating a " + topic + " fact for " + object_name)
    min_distance_x = 1
    min_distance_object_label = ""
    # for object in data:
    #     print(object)
    #     if (abs(object["x"]-0.5) < min_distance_x):
    #         min_distance_object_label = object["name"]
    response = openai.Completion.create(
        model="text-curie-001",
        # prompt="tell me a fact about"+min_distance_object_label +
        #"that teaches me " + topic,
        prompt="tell me a" + topic + " concept which is about a "+object_name,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return "A " + topic + " fact for "+min_distance_object_label+":"+response.choices[0].text


def wolram_results(query):
    URL_ENCODED_INPUT = urllib.parse.quote_plus(query)
    API_URL = "https://api.wolframalpha.com/v1/result?appid=" + \
        WOLFRAM_API_KEY+"&i="+URL_ENCODED_INPUT
    print("sending this request,"+API_URL)
    response = requests.request("GET", API_URL)
    print(response.text)
    return response.text


async def get_wolfram_results_async(session, query):
    URL_ENCODED_INPUT = urllib.parse.quote_plus(query)
    API_URL = "https://api.wolframalpha.com/v1/result?appid=" + \
        WOLFRAM_API_KEY+"&i="+URL_ENCODED_INPUT
    async with session.get(API_URL) as response:
        return await response.text()


def wolram_spoken_results(query):
    URL_ENCODED_INPUT = urllib.parse.quote_plus(query)
    API_URL = "https://api.wolframalpha.com/v1/result?appid=" + \
        WOLFRAM_API_KEY+"&i="+URL_ENCODED_INPUT
    response = requests.request("GET", API_URL)
    print(response.text)
    return response.text


def wolfram_summary_boxes(query):
    URL_ENCODED_INPUT = urllib.parse.quote_plus(query)
    API_URL = "http://www.wolframalpha.com/queryrecognizer/query.jsp?appid=DEMO" + \
        "&mode=Default"+"&i="+URL_ENCODED_INPUT+"&output=json"
    # WOLFRAM_API_KEY+

    response = requests.request("GET", API_URL)
    res = response.json()["query"][0]["summarybox"]["path"]
    print(res)
    API_URL = "http://www.wolframalpha.com/summaryboxes/v1/query?appid=" + \
        WOLFRAM_API_KEY + "&path="+res
    # WOLFRAM_API_KEY+

    response2 = requests.request("GET", API_URL)

    print(response2.text)
    return response2.text


def main():
    # test
    #  wolfram if it works

    print(openai_end_to_end_gpt("I am curious to learn physics"))


if __name__ == "__main__":
    main()
