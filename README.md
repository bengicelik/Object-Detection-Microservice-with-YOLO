# Object Detection Microservice

## Features
* Object Detection: Leverages a YOLO model to identify objects in any uploaded image.
* Bounding Boxes: Provides coordinates for bounding boxes around detected objects.
* REST API: API for uploading images and receiving detailed detection information.
* Docker Support: Dockerized for easy deployment and scaling.
  
## Project Structure
Overview of main components:
* `main.py`: main file of microservice where FastAPI app is runs.
* `Dockerfile and docker-compose.yml`: for dockerizing the app.
* `requirements.txt`: List of all libraries needed in project.
  
## Get Start
Follow instructions to get the project up and running on your local machine.

## Prerequisites
* Python 3.8 or newer
* Docker and Docker Compose 
* Git

## Installation
* Clone repo: 
```
https://github.com/bengicelik/Object-Detection-Microservice-with-YOLO.git

cd Object-Detection-Microservice-with-YOLO
```
* Install requirements:
```
pip install -r requirements.txt
```

## Running the App
 * With Docker:\
```
docker-compose up --build
```

* Without Docker:
```
uvicorn main:app --reload
```

The application will accessible at http://127.0.0.1:8000.
## Accesing the Documentation
* When server is running visit: http://127.0.0.1:8000/docs in browser to see the automatic API documentation provided by FastAPI.

# Using API
- Send a POST request to /detect/ with an image file.
- Receive a JSON response containing detected objects, their bounding boxes, and confidence scores.
### Example Request
Using Postman :
* Set request type to POST.
* If you want to detect all object enter this url:\
http://127.0.0.1:8000/detect/
* or if you want to detect specific object type:\
http://127.0.0.1:8000/detect/?label=dog

For uploading image on postman:
* In body part, select the form-data and add key with named 'file' change text to file at the right and upload an image from your local machine.

After that when you send the request the example response format is like this: 
```
{
  "image": "base64_encoded_image",
  "objects": [
    {
      "label": "person",
      "confidence": 0.99,
      "x": 220,
      "y": 34,
      "width": 50,
      "height": 72
    }
  ],
  "count": 1
}
```
## Converting YOLOv5 model to ONNX Format
* Clone yolov5 repo:
```
git clone https://github.com/ultralytics/yolov5
cd yolov5
```
* Install requirements:
```
pip install -r requirements.txt
``` 
* export model to onnx
```
python export.py --weights yolov5s.pt --include onnx
```
## How to Test
1. Start the Microservice : `docker-compose up`
2. Preparing the Request: Use a tool like Postman or cURL to send requests to your microservice. (explained in the `Using API` part above)
3. You can find test image from test_images folder in project repository.
4. Analyzing the Response: The microservice returns a JSON response containing:image,objects and count.
5. Output image: The output image is form of base64 in the response. For visualizing you can use the tools like `base64 to image` converters on internet to get the visual by pasting the base64 code of output image.


## License
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/bengicelik/Object-Detection-Microservice-with-YOLO/blob/develop/LICENCES.md)

