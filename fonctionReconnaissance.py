import cv2
import numpy as np
import tensorflow as tf

def find_faces(img, model):
    """
    Find the faces in an image
    
    Parameters
    ----------
    img : np.uint8
        Image to find faces from
    model : dnn_Net
        Face detection model

    Returns
    -------
    faces : list
        List of coordinates of the faces detected in the image

    """
    h, w = img.shape[:2] #Recuperation hauteur et largeur de l'image

    blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    model.setInput(blob)
    res = model.forward()
    faces = []
    for i in range(res.shape[2]):
        confidence = res[0, 0, i, 2]
        if confidence > 0.5:
            box = res[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x, y, x1, y1) = box.astype("int")
            faces.append([x, y, x1, y1])

    return faces

def move_box(box, offset):
    """Move the box to direction specified by vector offset"""
    left_x = box[0] + offset[0]
    top_y = box[1] + offset[1]
    right_x = box[2] + offset[0]
    bottom_y = box[3] + offset[1]
    return [left_x, top_y, right_x, bottom_y]

def get_square_box(box):
    """Get a square box out of the given box, by expanding it."""
    left_x = box[0]
    top_y = box[1]
    right_x = box[2]
    bottom_y = box[3]

    box_width = right_x - left_x
    box_height = bottom_y - top_y

    # Check if box is already a square. If not, make it a square.
    diff = box_height - box_width
    delta = int(abs(diff) / 2)

    if diff == 0:                   # Already a square.
        return box
    elif diff > 0:                  # Height > width, a slim box.
        left_x -= delta
        right_x += delta
        if diff % 2 == 1:
            right_x += 1
    else:                           # Width > height, a short box.
        top_y -= delta
        bottom_y += delta
        if diff % 2 == 1:
            bottom_y += 1

    # Make sure box is always square.
    assert ((right_x - left_x) == (bottom_y - top_y)), 'Box is not square.'

    return [left_x, top_y, right_x, bottom_y]


def detect_marks(img, model, face):
    """
    Find the facial landmarks in an image from the faces

    Parameters
    ----------
    img : np.uint8
        The image in which landmarks are to be found
    model : Tensorflow model
        Loaded facial landmark model
    face : list
        Face coordinates (x, y, x1, y1) in which the landmarks are to be found

    Returns
    -------
    marks : numpy array
        facial landmark points

    """

    offset_y = int(abs((face[3] - face[1]) * 0.1))
    box_moved = move_box(face, [0, offset_y])
    facebox = get_square_box(box_moved)
    
    h, w = img.shape[:2]
    if facebox[0] < 0:
        facebox[0] = 0
    if facebox[1] < 0:
        facebox[1] = 0
    if facebox[2] > w:
        facebox[2] = w
    if facebox[3] > h:
        facebox[3] = h
    
    face_img = img[facebox[1]: facebox[3],
                     facebox[0]: facebox[2]]
    face_img = cv2.resize(face_img, (128, 128))
    face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
    
    # # Actual detection.
    predictions = model.signatures["predict"](
        tf.constant([face_img], dtype=tf.uint8))

    # Convert predictions to landmarks.
    marks = np.array(predictions['output']).flatten()[:136]
    marks = np.reshape(marks, (-1, 2))
    
    marks *= (facebox[2] - facebox[0])
    marks[:, 0] += facebox[0]
    marks[:, 1] += facebox[1]
    marks = marks.astype(np.uint)

    return marks


def getTabPointsFace(marks):
    return np.array([
                    marks[27], # Nose haut
                    marks[30], # Nose bas
                    marks[8],  # Menton
                    marks[36], # Eye Gauche G
                    marks[39], # Eye Gauche D
                    marks[42], # Eye Droite G
                    marks[45]  # Eye Droite D
                ], dtype="double")

def getModelFile():
    return "models/opencv_face_detector_uint8.pb"

def getConfigFile():
    return "models/opencv_face_detector.pbtxt"

def getFaceModel():
    return cv2.dnn.readNetFromTensorflow("models/opencv_face_detector_uint8.pb", "models/opencv_face_detector.pbtxt")

def getLandmark_model():
    return tf.saved_model.load("models/pose_model")

def main():
    modelFile = getModelFile()
    configFile = getConfigFile()
    face_model = getFaceModel()
    landmark_model = getLandmark_model()

    cap = cv2.VideoCapture(2)
    ret, img = cap.read()

    while True:
        ret, img = cap.read()
        if ret == True:
            faces = find_faces(img, face_model)
            for face in faces:
                marks = detect_marks(img, landmark_model, face)

                image_points = np.array([
                                            marks[31],     # Nose tip
                                            marks[8],     # Chin
                                            marks[36],     # Left eye left corner
                                            marks[45],     # Right eye right corne
                                            marks[48],     # Left Mouth corner
                                            marks[54]      # Right mouth corner
                                        ], dtype="double")
                
                image_points = getTabPointsFace(marks)
                
                for p in image_points:
                    cv2.circle(img, (int(p[0]), int(p[1])), 4, (0,0,255), -1)
                

                (x,y,w,h) = face
                eye_center = ((x + w)//2, (y + h)//2)
                radius = int(round(((w-x) + (h-y))*0.5))
                #cv2.circle(img, eye_center, radius, (255, 0, 0 ), 4)
                cv2.ellipse(img, eye_center, ((w-x+50)//2, (h-y+50)//2), 0, 0, 360, (255, 0, 255), 4)
                
            
            cv2.imshow('img', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
   main()