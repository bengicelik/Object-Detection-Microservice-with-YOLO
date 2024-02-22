# Object Detection Microservice

## Features
* Object Detection: Leverages a YOLO model to identify objects in any uploaded image.
* Bounding Boxes: Provides coordinates for bounding boxes around detected objects.
* REST API: API for uploading images and receiving detailed detection information.
* Docker Support: Dockerized for easy deployment and scaling.

## Get Start
Follow instructions to get the project up and running on your local machine.

## Prerequisites
* Python 3.8 or newer
* Docker and Docker Compose 
* Git

## Installation DÜZELTTTT
* Clone repo: \
`git clone https://github.com/bengiscelik/object-detection-microservice.git `\
`cd object-detection-microservice`
* Install requirements: \
`pip install -r requirements.txt`

## Running the App
 * With Docker:\
`docker-compose up --build`

* Without Docker:\
`uvicorn main:app --reload`

The application will accessible at http://localhost:8000.

# Using API 
- Send a POST request to /detect/ with an image file.
- Receive a JSON response containing detected objects, their bounding boxes, and confidence scores.
### Example Request
Using Postman :
* Set request type to POST.
* If you want to detect all object enter this url:\
[http://localhost:8000/detect/](http://127.0.0.1:8000/detect/)
* or if you want to detect specific object type:\
http://127.0.0.1:8000/detect/?label=dog


## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details 
