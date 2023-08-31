from typing import Union
from fastapi import FastAPI, UploadFile
from PIL import Image
import pytesseract

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/upload")
async def upload_file(file: UploadFile):
    text = pytesseract.image_to_string(Image.open(file.file))
    return {"text": text}
