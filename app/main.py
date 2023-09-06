import os
import requests
from bs4 import BeautifulSoup
from typing import Union
from fastapi import FastAPI, Response, UploadFile, status
from PIL import Image
import pytesseract
from transformers import pipeline
# import cv2

os.environ["TESSDATA_PREFIX"] = "/tessdata"

app = FastAPI()

UPLOAD_FOLDER = './app/static/uploads'

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/upload")
async def upload_file(file: UploadFile, response: Response):
    text = pytesseract.image_to_string(Image.open(file.file), lang='por')

    pipe = pipeline("text-generation", model="meta-llama/Llama-2-70b-hf", token="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")
    print(pipe('qual a frase mais famosa usada por programadores no seu primeiro programa?'))

    return {"text": text}


# Not working yet, problem with browser version and rate limit :c
@app.get("/scrapy")
def read_item(url: Union[str, None] = None):
    response = requests.get(url)
    bs = BeautifulSoup(response.text, 'html.parser')
    table = bs.findAll('table')[0]
    rows = table.findAll('tr')

    scrapy = list()

    for row in rows:
        scrapyRow = []

        for cell in row.findAll(['td', 'th']):
            scrapyRow.append(cell.get_text())

        scrapy.append(scrapyRow)

    return {"url": url, "scrapy": scrapy}
