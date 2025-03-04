from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
import uvicorn
import io
import base64
from PIL import Image, ImageDraw
import numpy as np
import onnxruntime as ort
import os

app = FastAPI()

model_path = "/app/yolov5s.onnx"
ort_session = ort.InferenceSession(model_path)

def encode_image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def draw_boxes(image, results_data):
    draw = ImageDraw.Draw(image)
    for obj in results_data:
        top_left = (obj['x'], obj['y'])
        bottom_right = (obj['x'] + obj['width'], obj['y'] + obj['height'])
        draw.rectangle([top_left, bottom_right], outline="blue", width=2)
        draw.text((obj['x'], obj['y']), f"{obj['label']} {obj['confidence']:.2f}", fill="red")
    return image

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

def get_label_name(label_id):
    return LABELS.get(label_id, "Unknown")

def process_model_output(model_output):
    detected_objects = []
    for detection in model_output[0][0]:
        x_center, y_center, width, height, obj_confidence = detection[:5]
        class_probabilities = detection[5:]
        class_id = np.argmax(class_probabilities)
        class_confidence = class_probabilities[class_id]
        label = get_label_name(class_id)

        if obj_confidence > 0.5 and class_confidence > 0.5:
            detected_objects.append({
                "label": label,
                "confidence": float(obj_confidence * class_confidence),
                "x": float(x_center - width / 2),
                "y": float(y_center - height / 2),
                "width": float(width),
                "height": float(height)
            })
    return detected_objects

def non_maximum_suppression(objects, iou_threshold=0.5):
    if len(objects) == 0:
        return objects

    objs = sorted(objects, key=lambda obj: obj['confidence'], reverse=True)
    keep = []
    while objs:
        largest = objs.pop(0)
        keep.append(largest)
        objs = [obj for obj in objs if iou(largest, obj) < iou_threshold]
    return keep

def iou(boxA, boxB):
    # determine the coordinates of the intersection rectangle
    xA = max(boxA['x'], boxB['x'])
    yA = max(boxA['y'], boxB['y'])
    xB = min(boxA['x'] + boxA['width'], boxB['x'] + boxB['width'])
    yB = min(boxA['y'] + boxA['height'], boxB['y'] + boxB['height'])

    # compute the area of intersection
    intersection = max(0, xB - xA) * max(0, yB - yA)

    # compute the area of both bounding boxes
    boxAArea = boxA['width'] * boxA['height']
    boxBArea = boxB['width'] * boxB['height']

    # compute the intersection over union
    iou = intersection / float(boxAArea + boxBArea - intersection)
    return iou

@app.post("/detect/")
async def detect_objects(file: UploadFile = File(...), label: str = Query(default=None)):
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data)).convert("RGB")
    image_resized = image.resize((640, 640))

    image_np = np.array(image_resized).astype(np.float32)
    image_np = image_np / 255.0
    image_np = np.transpose(image_np, (2, 0, 1))
    input_tensor = np.expand_dims(image_np, axis=0)

    ort_inputs = {ort_session.get_inputs()[0].name: input_tensor}
    ort_outs = ort_session.run(None, ort_inputs)

    results_data = process_model_output(ort_outs)
    results_data = non_maximum_suppression(results_data)  # apply NMS


    if label and label.lower() != "all":
        results_data = [obj for obj in results_data if obj["label"].lower() == label.lower()]

    if not results_data:
        raise HTTPException(status_code=404, detail=f"No objects with label '{label}' found")

    image_processed = draw_boxes(image, results_data)
    image_base64 = encode_image_to_base64(image_processed)

    result = {
        "image": image_base64,
        "objects": results_data,
        "count": len(results_data)
    }

    return JSONResponse(content=result)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
