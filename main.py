from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
import uvicorn
import io

app = FastAPI()

model_path = os.path.join("Macintosh HD", os.sep, "Users", "beng", "Desktop", "case", "yolov5s.onnx")
ort_session = ort.InferenceSession(model_path)
