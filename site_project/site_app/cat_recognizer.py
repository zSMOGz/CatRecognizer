import cv2
from PIL import Image
from numpy import array


def detect_cat_face(upload_image,
                    haar_cascade,
                    haar_name):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + haar_cascade)

    if face_cascade.empty():
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalcatface_extended.xml')

    image = cv2.imread(upload_image.path)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    image_original = array(Image.open(upload_image.path))

    faces, _, confidences = face_cascade.detectMultiScale3(gray_image,
                                                           scaleFactor=1.02,
                                                           minNeighbors=1,
                                                           minSize=(50, 50),
                                                           flags=cv2.CASCADE_SCALE_IMAGE,
                                                           outputRejectLevels=True)

    if (len(faces) == 0
            or face_cascade.empty()):
        return Image.fromarray(image_original)
    else:
        face_index = 0
        for (x, y, w, h) in faces:
            if (confidences is not None
                    and confidences[face_index] > 0.9):
                cv2.rectangle(image_original,
                              (x, y),
                              (x + w, y + h),
                              (0, 0, 255))

                cv2.putText(image_original,
                            f'{haar_name[1]} {str(round(confidences[face_index]/5*100, 2))}',
                            (x, y - 5),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (0, 0, 255),
                            2)
            face_index += 1

        return Image.fromarray(image_original)
