from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
import uvicorn
import io
import base64
from PIL import Image

app = FastAPI()

model_path = os.path.join("Macintosh HD", os.sep, "Users", "beng", "Desktop", "case", "yolov5s.onnx")
ort_session = ort.InferenceSession(model_path)

def encode_image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

