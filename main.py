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

LABELS = {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck',
          8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench',
          14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear',
          22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase',
          29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat',
          35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass',
          41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich',
          49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair',
          57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop',
          64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster',
          71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear',
          78: 'hair drier', 79: 'toothbrush'}

def process_model_output(model_output):
    detected_objects = []
    for detection in model_output[0][0]:
        x_center, y_center, width, height, obj_confidence = detection[:5]
        detected_objects.append({
            "x_center": x_center, "y_center": y_center,
            "width": width, "height": height, "confidence": obj_confidence
        })

        if obj_confidence > 0.5:
            detected_objects.append({
                "label": label,
                "confidence": float(obj_confidence),
                "x": float(x_center - width / 2),
                "y": float(y_center - height / 2),
                "width": float(width),
                "height": float(height)
            })
    return detected_objects

@app.post("/detect/")
async def detect_objects():



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
