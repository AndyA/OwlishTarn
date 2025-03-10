import glob
import json
import os
import time
import urllib.parse
from typing import Any
from dotenv import load_dotenv
from mistralai import (
    Mistral,
    OCRImageObject,
    OCRPageDimensions,
    OCRPageObject,
    OCRResponse,
    SDKError,
)

load_dotenv()


def save_json(file: str, data: Any) -> None:
    os.makedirs(os.path.dirname(file), exist_ok=True)
    tmp = file + ".tmp"
    with open(tmp, "w") as f:
        f.write(json.dumps(data, indent=2))
    os.rename(tmp, file)


def load_json(file: str) -> Any:
    with open(file) as f:
        return json.load(f)


def image_json(image: OCRImageObject) -> dict:
    return {
        "id": image.id,
        "top_left_x": image.top_left_x,
        "top_left_y": image.top_left_y,
        "bottom_right_x": image.bottom_right_x,
        "bottom_right_y": image.bottom_right_y,
    }


def dimensions_json(dimensions: OCRPageDimensions) -> dict:
    return {
        "dpi": dimensions.dpi,
        "height": dimensions.height,
        "width": dimensions.width,
    }


def page_json(page: OCRPageObject) -> dict:
    return {
        "index": page.index,
        "markdown": page.markdown,
        "images": [image_json(image) for image in page.images or []],
        "dimensions": dimensions_json(page.dimensions),
    }


def ocr_json(ocr: OCRResponse) -> dict:
    return {
        "pages": [page_json(page) for page in ocr.pages],
    }


def image_url(image: str) -> str:
    pass


def public_url(img: str) -> str:
    return BASE_URL + "/" + urllib.parse.quote(img, safe="/()")


def scan_image(img_url: str) -> dict:
    backoff = 1
    while True:
        try:
            return client.ocr.process(
                model="mistral-ocr-latest",
                document={"type": "image_url", "image_url": img_url},
            )
        except SDKError as e:
            if e.status_code != 429:
                raise
        print(f"Rate limited, backing off for {backoff} seconds")
        time.sleep(backoff)
        backoff *= 2


IMAGE_DIR = "images"
REPO = "OwlishTarn"
BASE_URL = (
    f"https://raw.githubusercontent.com/AndyA/{REPO}/refs/heads/main/nailsworth/images"
)
STATE = "tmp/ocr-state.json"

api_key = os.environ["API_KEY"]
client = Mistral(api_key=api_key)

try:
    state = load_json(STATE)
except FileNotFoundError:
    state = {}

for img in glob.glob(os.path.join(IMAGE_DIR, "**", "*.jpeg"), recursive=True):
    img_rel = os.path.relpath(img, IMAGE_DIR)
    if img_rel in state:
        continue

    resp = scan_image(public_url(img_rel))
    rep = ocr_json(resp)
    print(json.dumps(rep, indent=2))
    state[img_rel] = rep
    save_json(STATE, state)
