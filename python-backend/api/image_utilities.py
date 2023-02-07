from google_images_search import GoogleImagesSearch
#import Constants.Values as CONSTANTS

GCP_API_KEY = "AIzaSyAJP4ZwYnV14DJ4MiQIbFzz0VtP1fw5iZM"
CX = "f1cf9c8faf3b24e9f"


def getMatchingImageUrl(query):
    gis = GoogleImagesSearch(GCP_API_KEY, CX)
    _search_params = {
        'q': query,
        'num': 1,
        'fileType': 'jpg'
    }

    # this will only search for images:
    gis.search(search_params=_search_params)
    for image in gis.results():
        return image.url


def main():
    print(getMatchingImageUrl("Plant cell wall"))


if __name__ == "__main__":
    main()
