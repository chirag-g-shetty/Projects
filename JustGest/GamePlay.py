import _thread as td,cv2 as cv,mediapipe as mp,pyautogui as pag
from pynput.keyboard import Controller, Key
keyboard = Controller()
cap = cv.VideoCapture(0, cv.CAP_DSHOW)
mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
face_mesh = mpFaceMesh.FaceMesh(min_detection_confidence=0.75)
enabled = True
allow_count = True
sec_count = 0

def speak(text):
    import pyttsx3
    ts = pyttsx3.init()
    ts.setProperty('rate', 120)
    ts.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
    ts.say(text)
    ts.runAndWait()
def enabler():
    global enabled
    import time
    time.sleep(.75)
    enabled = True

def timer():
    global allow_count, sec_count
    sec_count += 1
    pag.sleep(1)
    allow_count = True
def doer():
    import _thread
    global enabled
    d = {196: 0, 197: 0, 50: 0, 132: 0, 352: 0, 323: 0, 212: 0, 214: 0}
    success, img = cap.read()
    img = cv.flip(img, 1)
    # cv.imshow('GamePlay',img)
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = face_mesh.process(imgRGB)

    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACEMESH_CONTOURS,
                                  mpDraw.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                                  )

            for id, lm in enumerate(faceLms.landmark):
                ih, iw, ic = img.shape
                x, y = int(lm.x * iw), int(lm.y * ih)
                if id in (196, 197, 50, 132, 323, 352):
                    d[id] = x
                elif id in (212, 214):
                    d[id] = y
            if enabled and d[214] - d[212] >= 3:
                keyboard.press(Key.up)
                enabled = False
                keyboard.release(Key.up)
                _thread.start_new_thread(enabler, ())
                pass
            elif enabled and d[214] - d[212] in (-1, -2):
                keyboard.press(Key.down)
                enabled = False
                keyboard.release(Key.down)
                _thread.start_new_thread(enabler, ())
                pass
            elif enabled and d[50] - d[132] in range(4, -11, -1):
                keyboard.press(Key.left)
                enabled = False
                keyboard.release(Key.left)
                _thread.start_new_thread(enabler, ())
                pass
            elif enabled and d[50] - d[132] >= 23:
                keyboard.press(Key.right)
                enabled = False
                keyboard.release(Key.right)
                _thread.start_new_thread(enabler, ())
                pass

    return img

try:
    while sec_count <= 45:

        img = doer()
        if allow_count:
            allow_count = False
            td.start_new_thread(timer, ())
        if cv.waitKey(1) == ord('q'):
            break

except:speak('Oops!There was a glitch, please try again')
finally:
    cap.release()
    cv.destroyAllWindows()
