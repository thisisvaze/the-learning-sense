from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import requests
from PIL import Image


def get_text_from_image(image):

    processor = TrOCRProcessor.from_pretrained(
        "microsoft/trocr-base-handwritten")
    model = VisionEncoderDecoderModel.from_pretrained(
        "microsoft/trocr-base-handwritten")

    #image = Image.open(image).convert("RGB")
    # load image from the IAM database
    url = 'https://fki.tic.heia-fr.ch/static/img/a01-122-02-00.jpg'
    image = Image.open(requests.get(url, stream=True).raw).convert("RGB")

    pixel_values = processor(image, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)

    generated_text = processor.batch_decode(
        generated_ids, skip_special_tokens=True)[0]
    print(generated_text)
    return generated_text
#     reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory
#     result = reader.readtext(Image.open(image), detail = 0)
#     return ' '.join(result)

# export GOOGLE_APPLICATION_CREDENTIALS="/Users/vaze/desktop/thesis-server-code/keys/thesis-gcp-api-97828526cbc3.json"
