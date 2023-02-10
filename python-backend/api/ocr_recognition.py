from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import requests
from PIL import Image


class microsoft_tocr:
    def __init__(self):
        self.processor = TrOCRProcessor.from_pretrained(
            "microsoft/trocr-base-handwritten")
        self.model = VisionEncoderDecoderModel.from_pretrained(
            "microsoft/trocr-base-handwritten")

    def get_text_from_image(self):

        #image = Image.open(image).convert("RGB")
        # load image from the IAM database
        url = 'https://fki.tic.heia-fr.ch/static/img/a01-122-02-00.jpg'
        image = Image.open(requests.get(url, stream=True).raw).convert("RGB")

        pixel_values = self.processor(image, return_tensors="pt").pixel_values
        generated_ids = self.model.generate(pixel_values)

        generated_text = self.processor.batch_decode(
            generated_ids, skip_special_tokens=True)[0]
        print(generated_text)
        return generated_text
    #     reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory
    #     result = reader.readtext(Image.open(image), detail = 0)
    #     return ' '.join(result)

# export GOOGLE_APPLICATION_CREDENTIALS="/Users/vaze/desktop/thesis-server-code/keys/thesis-gcp-api-97828526cbc3.json"


def main():
    m = microsoft_tocr()
    m.get_text_from_image()


if __name__ == "__main__":
    main()
