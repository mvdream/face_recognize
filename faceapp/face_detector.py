from sklearn import neighbors
import os, pickle, math, face_recognition, base64 , numpy as np ,pandas as pd
from PIL import Image, ImageDraw
from face_recognition.face_recognition_cli import image_files_in_folder
from io import BytesIO,StringIO
from faceapp.models import Datasets,People
def get_student_name(id):
    return  People.objects.filter(label_id=id).get().name

def predict(img,distance_threshold=0.5):
    output_data = {'students':[],'status':'Successfully recognize students','error':False}
    if People.objects.all().count()<=1:
        output_data['error'] = True
        output_data['status'] = "Add atleast two students"
        return output_data
    with open("model.clf", 'rb') as f:
        knn_clf = pickle.load(f)

    X_face_locations = face_recognition.face_locations(img)

    if len(X_face_locations) == 0:
        output_data['error'] = True
        output_data['status'] = "There is no face in picture"
        return output_data

    faces_encodings = face_recognition.face_encodings(img, known_face_locations=X_face_locations)

    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

    output_data['students'] = [(get_student_name(pred), loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]

    return output_data


def show_prediction_labels_on_image(img, predictions):
    pil_image = Image.open(BytesIO(base64.b64decode(img)))
    draw = ImageDraw.Draw(pil_image)

    for name, (top, right, bottom, left) in predictions:
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

        name = name.encode("UTF-8")

        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

    del draw

    return base64.b64encode(pil_image.tobytes())