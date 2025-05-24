import math
from sklearn import neighbors
import pickle
from PIL import Image
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
from time import monotonic
from .models import Image
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def record_time(function):
    def wrap(*args, **kwargs):
        start_time = monotonic()
        function_return = function(*args, **kwargs)
        print(f"Run time {monotonic() - start_time} seconds")
        return function_return
    return wrap

def train(model_save_path=None,model=Image, n_neighbors=None, knn_algo='ball_tree', verbose=False):
    X = []
    y = []
    counter = 1
    for img in model.objects.all():
        img_path = img.image.path
        print(counter, ": - :", img_path.split("/")[-2])
        image = face_recognition.load_image_file(img_path)
        face_bounding_boxes = face_recognition.face_locations(image, number_of_times_to_upsample=0)
        if (len(face_bounding_boxes)) != 1:
            if verbose:
                print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(face_bounding_boxes) < 1 else "Found more than one face"))
        else:
            X.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
            y.append(img.person_id)
        counter=counter+1        

    # Determine how many neighbors to use for weighting in the KNN classifier
    if n_neighbors is None:
        n_neighbors = int(round(math.sqrt(len(X))))
        if verbose:
            print("Chose n_neighbors automatically:", n_neighbors)

    # Create and train the KNN classifier
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance', n_jobs=3)
    knn_clf.fit(X, y)

    # Save the trained KNN classifier
    if model_save_path is not None:
        # Ensure directory exists
        os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f)
    else:
        with open('knn_model.pkl', 'wb') as f:
            pickle.dump(knn_clf, f)


def predict(file, knn_clf=None, model_path=None, distance_threshold=0.6):
    """
    Recognizes faces in given image using a trained KNN classifier

    :param X_img_path: path to image to be recognized
    :param knn_clf: (optional) a knn classifier object. if not specified, model_save_path must be specified.
    :param model_path: (optional) path to a pickled knn classifier. if not specified, model_save_path must be knn_clf.
    :param distance_threshold: (optional) distance threshold for face classification. the larger it is, the more chance
           of mis-classifying an unknown person as a known one.
    :return: a list of names and face locations for the recognized faces in the image: [(name, bounding box), ...].
        For faces of unrecognized persons, the name 'unknown' will be returned.
    """

    if knn_clf is None and model_path is None:
        raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")

    # Load a trained KNN model (if one was passed in)
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)
    
    knn_clf.set_params(n_jobs=3)

    # Load image file and find face locations
    X_img = face_recognition.load_image_file(file=file)
    X_face_locations = face_recognition.face_locations(X_img, number_of_times_to_upsample=0)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test iamge
    faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_face_locations)

    # Use the KNN model to find the best matches for the test face
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

    # Predict classes and remove classifications that aren't within the threshold
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]

if __name__ == "__main__":
    classifier = train("media/static/uploads/images", model_save_path="media/static/model/trained_knn_model.clf", n_neighbors=1)

