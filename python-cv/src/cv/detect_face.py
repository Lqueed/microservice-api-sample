import cv2
import os
from src.helpers.logger import get_logger

logger = get_logger(__name__)

face_cascade_db = cv2.CascadeClassifier(
    cv2.data.haarcascades+"haarcascade_frontalface_default.xml")

def detect_face(filepath):
    try:
        img = cv2.imread(filepath)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade_db.detectMultiScale(img_gray, 1.1, 19)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        logger.info(f'detected {len(faces)} faces')
        filepath_new = f'{filepath}_detected.jpg'
        cv2.imwrite(filepath_new, img)
        return filepath_new
    except Exception:
        logger.error('error processing image', exc_info=True)
