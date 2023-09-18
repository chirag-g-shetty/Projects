import cv2 as cv
from deepface import DeepFace
def is_same_person(model_name="Facenet", distance_metric="euclidean_l2"):
    try:
        result = DeepFace.verify('Image.jpg', 'Present.jpg', model_name=model_name, distance_metric=distance_metric)
        return result["verified"]
    except: pass
    return False

def cap_N_save():
    cc=0
    cap = cv.VideoCapture(0,cv.CAP_DSHOW)
    while True:
        _,img = cap.read()
        if _:
            cc+=1
            if cc>60:
                cv.imwrite('Image.jpg',img)
                break
    cap.release()
    cv.destroyAllWindows()

def verify():
    cap = cv.VideoCapture(0,cv.CAP_DSHOW)
    if not cap.isOpened():
        print("Error: Couldn't open the camera.")
    else:
        c=0
        while True:
            ret, frame = cap.read()
            if ret:
                c+=1
                if c>60:
                    cv.imwrite('Present.jpg', frame)
                    return is_same_person()
        cap.release()
        cv.destroyAllWindows()

