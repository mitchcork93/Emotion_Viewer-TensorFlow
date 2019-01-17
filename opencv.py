import cv2
import dlib
import json
import requests
import mat

cnn_face_detector = dlib.cnn_face_detection_model_v1("cascades/mmod_human_face_detector.dat")
predictor = dlib.shape_predictor("cascades/shape_predictor_68_face_landmarks.dat")


def get_rects(img, scale, all=True):

    global cnn_face_detector
    dets = cnn_face_detector(img, scale)

    return dets


def detect_face(img, scale):

    """
        Method takes in an image and returns the image with a box drawn around every face in the image.
        commented code below is for use on non CUDA pcs, the other code is for CUDA ONLY
        :param img: image to detect faces in
        :param scale: how large to scale image
        :return img with overlay:
    """

    """
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    """

    dets = get_rects(img, scale)

    for i, d in enumerate(dets):
        cv2.rectangle(img, (d.rect.left(), d.rect.top()), (d.rect.right(), d.rect.bottom()), (255, 0, 255), 2)

    return img


def detect_emotion(img):

    """
    :param img:
    :return:
    """

    global predictor

    dets = get_rects(img, 0)
    for k, d in enumerate(dets):
        shape = predictor(img, d.rect)

        landmarks = dict()
        points = dict()

        index = 0
        for x in range(0, 68):

            landmark = shape.part(x)
            points[str(index)] = {'x': landmark.x, 'y': landmark.y}
            index = index + 1

        landmarks['landmarks'] = points
        return mat.predict(points)


def send_request(landmarks):

    """
        Method sends captured landmarks (in JSON format) to MAT C++ server for processing and predicting emotion.
         ****************************** METHOD NOT CURRENTLY IN USE *********************************************
        :param landmarks:
        :return emotion:
    """

    # Local MAT server
    url = 'http://localhost:9000/test'
    headers = {'content-type': 'application/json'}

    response = requests.post(url, data=json.dumps(landmarks), headers=headers)
    return response.json()

