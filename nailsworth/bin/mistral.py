import os
from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()


api_key = os.environ["API_KEY"]
client = Mistral(api_key=api_key)

ocr_response = client.ocr.process(
    model="mistral-ocr-latest",
    document={
        "type": "document_url",
        "document_url": "https://arxiv.org/pdf/2201.04234",
    },
    include_image_base64=True,
)
