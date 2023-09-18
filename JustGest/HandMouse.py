import _thread as td
import cv2 as cv
import mediapipe as mp
import numpy as np
import pyautogui as pag
import time
from pynput.mouse import Controller as m_c

mouse = m_c()

r_sec = 0
id_points = {i: (0, 0) for i in range(1, 21)}
time_allowed = True
mouse_in_action = True
pag.FAILSAFE = False
left_click_var = 0
click_allowed = True
right_click_allowed=True
scroll_allowed = True
task_allowed = False
zoom_allowed = True
others_allowed = True
close_allowed = True
zoom_close_allowed = True
t_a = 0
s_w, s_h = pag.size()
smoothening = 35
plocX, plocY = 0, 0
clocX, clocY = 0, 0


def timer():
    global time_allowed, r_sec
    time_allowed = False
    time.sleep(1)
    r_sec += 1
    time_allowed = True


def close_curr_window():
    pag.keyDown('alt')
    pag.press('f4')
    pag.keyUp('alt')


def windows_tab():
    pag.keyDown('win')
    pag.press('tab')
    pag.keyUp('win')


def alt_tab():
    pag.keyDown('alt')
    pag.press('tab')
    pag.keyUp('alt')


def enable_others():
    global others_allowed
    pag.sleep(3)
    others_allowed = True


def enable_close():
    global close_allowed
    pag.sleep(3)
    close_allowed = True


def manip_zoom():
    global zoom_allowed
    zoom_allowed = False
    pag.sleep(1)
    zoom_allowed = True

def manip_z_close():
    global zoom_close_allowed
    zoom_close_allowed = False
    pag.sleep(2.5)
    zoom_close_allowed = True
def enable_task_once():
    global task_allowed
    task_allowed = False
    pag.sleep(3)
    task_allowed = True


def manip_task():
    global task_allowed
    task_allowed = False
    pag.sleep(5)
    task_allowed = True


def manip_up_down():
    global scroll_allowed
    scroll_allowed = False
    pag.sleep(1)
    scroll_allowed = True


def enable_click():
    global click_allowed
    pag.sleep(.2)
    click_allowed = True

def enable_right_click():
    global right_click_allowed
    pag.sleep(3)
    right_click_allowed=True

def the_h_mouse():
    global s_w, s_h
    cap = cv.VideoCapture(0, cv.CAP_DSHOW)
    c_w = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    c_h = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(max_num_hands=1)
    mpDraw = mp.solutions.drawing_utils

    global id_points, mouse_in_action, left_click_var, click_allowed, right_click_allowed,scroll_allowed, task_allowed, zoom_allowed, others_allowed, t_a, smoothening, \
        plocX, plocY,clocX, clocY, time_allowed, close_allowed, zoom_close_allowed
    try:
        while mouse_in_action:
            if time_allowed:
                td.start_new_thread(timer, ())
            success, img = cap.read()
            imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            results = hands.process(imgRGB)
            try:
                if results.multi_hand_landmarks:
                    for handLms in results.multi_hand_landmarks:
                        mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
                        for id, lm in enumerate(handLms.landmark):
                            h, w, _ = img.shape
                            cx, cy = int(lm.x * w), int(lm.y * h)
                            id_points[id] = (cx, cy)
                            left_click_var = id_points[6][1] - id_points[4][1]
                        # if 0:
                            if id_points[4][0] < id_points[6][0] and abs(id_points[0][0] - id_points[1][0]) < 19:
                                t_a = 0
                                task_allowed = False
                                if abs(id_points[12][0] - id_points[1][0]) > 125:
                                    if scroll_allowed and id_points[20][0] != max(id_points[20][0], id_points[19][0],
                                                                                  id_points[18][0]) \
                                            and id_points[16][0] != max(id_points[14][0], id_points[15][0],
                                                                        id_points[16][0]) and \
                                            id_points[12][0] == max(id_points[12][0], id_points[11][0],
                                                                    id_points[10][0]) \
                                            and (
                                            id_points[8][0] == max(id_points[6][0], id_points[7][0], id_points[8][0])):
                                        if left_click_var < 40:
                                            pag.press('pagedown')
                                            td.start_new_thread(manip_up_down, ())
                                            break
                                        else:
                                            pag.press('pageup')
                                            td.start_new_thread(manip_up_down, ())
                                            break
                                elif left_click_var > 40:
                                    if close_allowed and id_points[12][0] != max(id_points[10][0], id_points[11][0],
                                                                                 id_points[12][0]) \
                                            and id_points[16][0] != max(id_points[14][0], id_points[15][0],
                                                                        id_points[16][0]) and \
                                            id_points[20][0] != max(id_points[18][0], id_points[19][0],
                                                                    id_points[20][0]) \
                                            and (
                                            id_points[8][0] == max(id_points[6][0], id_points[7][0], id_points[8][0])):
                                        close_curr_window()
                                        close_allowed = False
                                        td.start_new_thread(enable_close, ())
                                elif right_click_allowed and [12][0] != max(id_points[10][0], id_points[11][0],id_points[12][0]) \
                                        and id_points[16][0] != max(id_points[14][0], id_points[15][0],id_points[16][0]) and \
                                        id_points[8][0] != max(id_points[8][0], id_points[7][0],id_points[6][0]) \
                                        and (id_points[20][0] == max(id_points[20][0], id_points[19][0], id_points[18][0])):
                                    pag.rightClick()
                                    right_click_allowed = False
                                    td.start_new_thread(enable_right_click,())
                            elif abs(id_points[1][0] - id_points[0][0]) > 19:
                                if not t_a:
                                    td.start_new_thread(enable_task_once, ())
                                    t_a += 1
                                if abs(id_points[4][0] - id_points[5][0]) > 45 and id_points[4][0] > id_points[3][0]:
                                    if task_allowed and (
                                            id_points[20][1] == min(id_points[18][1], id_points[19][1],
                                                                    id_points[20][1])) and \
                                            id_points[8][1] == min(id_points[6][1], id_points[7][1],
                                                                   id_points[8][1]) and (
                                            id_points[12][1] == min(id_points[10][1], id_points[11][1],
                                                                    id_points[12][1])) \
                                            and (id_points[16][1] == min(id_points[14][1], id_points[15][1],
                                                                         id_points[16][1])) and abs(
                                        id_points[0][1] - id_points[16][1]) > 120:
                                        td.start_new_thread(pag.hotkey,('win', '5'))
                                        td.start_new_thread(manip_task, ())
                                        break
                                    elif task_allowed and (id_points[16][1] == min(id_points[14][1], id_points[15][1],
                                                                                   id_points[16][1])) and (
                                            id_points[8][1] == min(id_points[6][1], id_points[7][1],
                                                                   id_points[8][1]) and (
                                                    id_points[12][1] == min(id_points[10][1], id_points[11][1],
                                                                            id_points[12][1])) \
                                            and (
                                                    id_points[20][1] != min(id_points[18][1], id_points[19][1],
                                                                            id_points[20][1]))) and abs(
                                        id_points[8][1] - id_points[1][1]) > 130:
                                        td.start_new_thread(pag.hotkey,('win', '4'))
                                        td.start_new_thread(manip_task, ())
                                        break
                                    elif task_allowed and (id_points[16][1] != min(id_points[14][1], id_points[15][1],
                                                                                   id_points[16][1])) \
                                            and (id_points[8][1] == min(id_points[6][1], id_points[7][1],
                                                                        id_points[8][1]) and (
                                                         id_points[12][1] == min(id_points[10][1], id_points[11][1],
                                                                                 id_points[12][1])) \
                                                 and (id_points[20][1] != min(id_points[18][1], id_points[19][1],
                                                                              id_points[20][1]))) \
                                            and abs(id_points[12][0] - id_points[4][0]) > 70 and abs(
                                        id_points[8][1] - id_points[1][1]) > 130:
                                        td.start_new_thread(pag.hotkey,('win', '3'))
                                        td.start_new_thread(manip_task, ())
                                        break
                                    elif task_allowed and (id_points[10][0]<id_points[6][0]) and  (
                                            id_points[8][1] == min(id_points[6][1], id_points[7][1],
                                                                   id_points[8][1]) and (
                                                    id_points[12][1] != min(id_points[10][1], id_points[11][1],
                                                                            id_points[12][1])) \
                                            and (id_points[16][1] != min(id_points[14][1], id_points[15][1],
                                                                         id_points[16][1])) and (
                                                    id_points[20][1] != min(id_points[18][1], id_points[19][1],
                                                                            id_points[20][1]))) \
                                            and abs(id_points[8][1] - id_points[1][1]) > 130:
                                        td.start_new_thread(pag.hotkey,('win', '2'))
                                        td.start_new_thread(manip_task, ())
                                        break
                                    else:
                                        if task_allowed and (id_points[8][1] != min(id_points[6][1], id_points[7][1],
                                                                                    id_points[8][1]) and (
                                                                     id_points[12][1] != min(id_points[10][1],
                                                                                             id_points[11][1],
                                                                                             id_points[12][1])) \
                                                             and (id_points[16][1] != min(id_points[14][1],
                                                                                          id_points[15][1],
                                                                                          id_points[16][1])) and (
                                                                     id_points[20][1] != min(id_points[18][1],
                                                                                             id_points[19][1],
                                                                                             id_points[20][1]))) \
                                                and abs(id_points[6][1] - id_points[19][1]) < 30:
                                            td.start_new_thread(pag.hotkey,('win', '1'))
                                            td.start_new_thread(manip_task, ())
                                            break

                                elif id_points[4][0] < id_points[3][0]:
                                    if (id_points[12][1] != min(id_points[10][1], id_points[11][1], id_points[12][1])) \
                                            and (id_points[16][1] != min(id_points[14][1], id_points[15][1],
                                                                         id_points[16][1])) and (
                                            id_points[20][1] != min(id_points[18][1], id_points[19][1],
                                                                    id_points[20][1])) \
                                            and abs(id_points[8][1] - id_points[1][1]) > 130:
                                        if id_points[8][1] == min(id_points[6][1], id_points[7][1],
                                                                  id_points[8][1]):
                                            m_x = np.interp(id_points[6][0], (0, c_w), (0, s_w))
                                            m_y = np.interp(id_points[6][1], (0, c_h), (0, s_h))
                                            clocX = plocX + (m_x - plocX) / smoothening
                                            clocY = plocY + (m_y - plocY) / smoothening
                                            td.start_new_thread(td.start_new_thread,(pag.moveTo, (s_w - clocX-50, clocY-50)))
                                            plocX, plocY = clocX, clocY
                                        elif id_points[8][1]<id_points[3][1] and (id_points[8][1]>id_points[7][1]) and click_allowed:
                                            click_allowed=False
                                            td.start_new_thread(pag.leftClick,())
                                            td.start_new_thread(enable_click,())
                                    if zoom_close_allowed and id_points[8][1] != min(id_points[6][1], id_points[7][1], id_points[8][1]) and (
                                            id_points[12][1] != min(id_points[10][1], id_points[11][1],
                                                                    id_points[12][1])) \
                                            and (id_points[16][1] != min(id_points[14][1], id_points[15][1],
                                                                         id_points[16][1])) \
                                            and id_points[8][1] > id_points[7][1] and id_points[12][1] > id_points[11][
                                        1] \
                                            and id_points[16][1] > id_points[15][1] and id_points[20][1] < \
                                            id_points[19][1] \
                                            and id_points[20][1] < id_points[4][1]:
                                        pag.hotkey('win', 'esc')
                                        td.start_new_thread(manip_z_close,())
                                    elif id_points[12][0] < id_points[8][0] and (
                                            (id_points[12][1] == min(id_points[10][1], id_points[11][1],id_points[12][1])) and \
                                            id_points[8][1] == min(id_points[6][1], id_points[7][1],
                                                                   id_points[8][1])) \
                                            and (id_points[16][1] != min(id_points[14][1], id_points[15][1],
                                                                         id_points[16][1])) and (
                                            id_points[20][1] != min(id_points[18][1], id_points[19][1],
                                                                    id_points[20][1])) \
                                            and abs(id_points[8][1] - id_points[1][1]) > 130:
                                        z_v = abs(id_points[8][0] - id_points[12][0])
                                        if zoom_allowed:
                                            if z_v > 55:
                                                pag.hotkey('win', '=')
                                                td.start_new_thread(manip_zoom, ())
                                            elif z_v < 25:
                                                pag.hotkey('win', '-')
                                                td.start_new_thread(manip_zoom, ())
                                    elif others_allowed:
                                        if id_points[8][1] > id_points[11][1] and id_points[12][1] < id_points[11][1] \
                                                and id_points[16][1] < id_points[15][1] and id_points[20][1] > \
                                                id_points[14][1] and abs(id_points[0][1] - id_points[16][1]) > 120:
                                            alt_tab()
                                            others_allowed = False
                                            td.start_new_thread(enable_others, ())
                                        if (id_points[12][1] != min(id_points[10][1], id_points[11][1],
                                                                    id_points[12][1])) \
                                                and (id_points[16][1] != min(id_points[14][1], id_points[15][1],
                                                                             id_points[16][1])) and (
                                                id_points[20][1] == min(id_points[18][1], id_points[19][1],
                                                                        id_points[20][1])) \
                                                and id_points[8][1] == min(id_points[6][1], id_points[7][1],
                                                                           id_points[8][1]) \
                                                and abs(id_points[8][1] - id_points[1][1]) > 130 \
                                                and id_points[20][1] < id_points[6][1]:
                                            windows_tab()
                                            others_allowed = False
                                            td.start_new_thread(enable_others, ())
            except: pass
            img = cv.flip(img, 1)
            # cv.imshow('HandMouse', img)
            if cv.waitKey(1) == ord('q'):
                break
    except Exception as e:
        import traceback
        import sys
        exc_type, exc_value, exc_traceback = sys.exc_info()
        filename, line_number, func_name, text = traceback.extract_tb(exc_traceback)[-1]
        print(f"Exception occurred in {filename} on line {line_number}: {e}")
        cap.release()
