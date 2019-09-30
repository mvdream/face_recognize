import math, pandas as pd,numpy as np,json
from sklearn import neighbors
import os
import os.path
import pickle
from PIL import Image, ImageDraw
import face_recognition
import cv2
from face_recognition.face_recognition_cli import image_files_in_folder
from faceapp.models import Datasets,People

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def get_encoding(image, verbose=False):
    face_bounding_boxes = face_recognition.face_locations(image)
    if len(face_bounding_boxes) != 1:
        if verbose:
            print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(face_bounding_boxes) < 1 else "Found more than one face"))
        return []
    else:
        return face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0]

def numpy_to_list(numpy_ar):
    return list(numpy_ar)

def train(X,y, model_save_path=None, n_neighbors=None, knn_algo='ball_tree', verbose=False):
    if n_neighbors is None:
        n_neighbors = int(round(math.sqrt(len(X))))
        if verbose:
            print("Chose n_neighbors automatically:", n_neighbors)

    # Create and train the KNN classifier
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    knn_clf.fit(X, y)

    # Save the trained KNN classifier
    if model_save_path is not None:
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f)

def str_to_numpy(array_str):
    return np.array(json.loads(array_str))

def add_new(name, image):
    encoding = get_encoding(image)
    # print(encoding)
    if len(encoding)==0:
        return "There is no face detect in image"
    if not Datasets.objects.all():
        X,y = [],[]
    else:
        X = [str_to_numpy(encoding[0]) for encoding in Datasets.objects.all().values_list("encoding")]
        y = [label[0] for label in Datasets.objects.all().values_list("label")]
    id = People.objects.latest("label_id").label_id + 1 if People.objects.all() else 1
    if len(encoding)!=0:
        X.append(encoding)
        y.append(id)

    train(X,y, model_save_path="model.clf", n_neighbors=2)

    Datasets(encoding=numpy_to_list(encoding),label=id).save()
    people_obj = People(label_id=id,name=name).save()

    return "Successfully add new student"
