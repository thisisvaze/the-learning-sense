import base64
import requests
from PIL import Image

def get_plant_name_2(image):

    API_KEY = "2b10k7dF1DJuRhGmzOigudIze"	# Your API_KEY here
    api_endpoint = f"https://my-api.plantnet.org/v2/identify/all?api-key={API_KEY}"
    # encode images to base64
    """images = Image.open(image)"""
    images = [base64.b64encode(image.read()).decode("ascii")]
    response = requests.post(
        api_endpoint,
        files = [
	('images', (open(image, 'rb')))]
        ).json()
    print(response)
    for result in response["results"]:
        print(result["species"]["genus"]["scientificNameWithoutAuthor"]) 
       # Taraxacum officinale
    return result["species"]["genus"]["scientificNameWithoutAuthor"]

def get_plant_name(image):

    # encode images to base64
    images = [base64.b64encode(image.read()).decode("ascii")]

    response = requests.post(
        "https://api.plant.id/v2/identify",
        json={
            "images": images,
            "modifiers": ["similar_images"],
            "plant_details": ["common_names", "url"],
        },
        headers={
            "Content-Type": "application/json",
            "Api-Key": "ZLIolJj7rS2eFztToaEJU1plgMAwPlyGFM2Iif0zJ5megApDdi",
        }).json()

    for suggestion in response["suggestions"]:
        print(suggestion["plant_name"])    # Taraxacum officinale
        print(suggestion["plant_details"]["common_names"])    # ["Dandelion"]
        print(suggestion["plant_details"]["url"])    # https://en.wikipedia.org/wiki/Taraxacum_officinale

        return suggestion["plant_details"]["common_names"][0]
