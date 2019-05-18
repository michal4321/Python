from Operation import *
from copy import deepcopy
import cv2
import cv2 as cv
import numpy as np
import math

left_clicked = False
mouse_drawing_rect_coords = []


def all_same(table):
    tmp = table[0]
    if tmp == 0:
        return False
    for x in table:
        if x != tmp:
            return False
    return True


def handle_mouse_event(event, x, y, flags, param):
    global left_clicked
    global mouse_drawing_rect_coords

    if left_clicked:
        '''User is drawing case, so new end is taken'''
        if len(mouse_drawing_rect_coords) > 2:
            mouse_drawing_rect_coords = []
        if len(mouse_drawing_rect_coords) > 1:
            del (mouse_drawing_rect_coords[-1])
        mouse_drawing_rect_coords.append((x, y))

    if event == cv2.EVENT_LBUTTONDOWN and not left_clicked:
        '''User just clicked case - starting to draw'''
        mouse_drawing_rect_coords.append((x, y))
        left_clicked = True
    elif event == cv2.EVENT_LBUTTONUP:
        '''User stopped drawing case, so area is left as it is'''
        if len(mouse_drawing_rect_coords) == 2:
            del (mouse_drawing_rect_coords[-1])
        mouse_drawing_rect_coords.append((x, y))
        left_clicked = False


class CameraOperator:

    def __init__(self):
        '''Global variable, when leave is true, program ends'''
        self.leave = False

        '''This attribute stores current user decision'''
        self.status = None
        self.status_move = None
        self.block = None

        '''This attribute shows if observer took status'''
        self.status_delivered = True

    def get_status(self):
        '''Function used by observer to get current user decision'''
        self.status_delivered = True
        return self.status

    def get_cropped_image(self, image, fist):
        '''if the area in which hand recognition maus take place was specified, this function prints cropped image'''

        for (x, y, w, h) in fist:
            leftdown = x - w
            rightdown = x + 2 * w
            leftup = y - h
            rightup = y + 2 * h

            cropped_image = image[leftdown:rightdown, leftup:rightup]

        return cropped_image

    def making_output(self, frame,left_up_corner_y,left_up_corner_x,right_down_corner_y,right_down_corner_x):

        h = right_down_corner_y - left_up_corner_y
        w = right_down_corner_x - left_up_corner_x
        shift = 30

        cv2.putText(frame, "Mode: " + str(self.status), (15, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.35,
                    (0, 0, 255), 1)
        if self.status == 1:
            cv2.putText(frame, "RADIO", (left_up_corner_x - shift, int(left_up_corner_y+h/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.35,
                        (0, 0, 255), 1)
            # cv2.putText(frame, "lewo góra", (left_up_corner_x -shift, left_up_corner_y), cv2.FONT_HERSHEY_SIMPLEX,
            #             0.35,
            #             (0, 0, 255), 1)
            # cv2.putText(frame, "Środek", (int(left_up_corner_x + w/2)-shift, left_up_corner_y), cv2.FONT_HERSHEY_SIMPLEX,
            #             0.35,
            #             (0, 0, 255), 1)
            # cv2.putText(frame, "Prawo góra", (right_down_corner_x, left_up_corner_y), cv2.FONT_HERSHEY_SIMPLEX,
            #             0.35,
            #             (0, 0, 255), 1)
            cv2.putText(frame, "LOGIN", (right_down_corner_x, int(left_up_corner_y + h / 2)), cv2.FONT_HERSHEY_SIMPLEX,
                        0.35,
                        (0, 0, 255), 1)
        if self.status == 2:
            cv2.putText(frame, "VOL -", (left_up_corner_x - shift, int(left_up_corner_y + h / 2)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.35,
                        (0, 0, 255), 1)
            cv2.putText(frame, "DISLIKE", (left_up_corner_x - shift, left_up_corner_y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.35,
                        (0, 0, 255), 1)
            # cv2.putText(frame, "Środek", (int(left_up_corner_x + w/2)-shift, left_up_corner_y), cv2.FONT_HERSHEY_SIMPLEX,
            #             0.35,
            cv2.putText(frame, "LIKE", (right_down_corner_x, left_up_corner_y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.35,
                        (0, 0, 255), 1)
            cv2.putText(frame, "Vol +", (right_down_corner_x, int(left_up_corner_y + h / 2)), cv2.FONT_HERSHEY_SIMPLEX,
                        0.35,
                        (0, 0, 255), 1)
        if self.status == 3:
            cv2.putText(frame, "<---", (left_up_corner_x - shift, int(left_up_corner_y + h / 2)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.35,
                        (0, 0, 255), 1)
            # cv2.putText(frame, "lewo góra", (left_up_corner_x - shift, left_up_corner_y), cv2.FONT_HERSHEY_SIMPLEX,
            #             0.35,
            #             (0, 0, 255), 1)
            cv2.putText(frame, "OKk", (int(left_up_corner_x + w / 2) - shift, left_up_corner_y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.35,
                        (0, 0, 255), 1)
            # cv2.putText(frame, "Prawo góra", (right_down_corner_x, left_up_corner_y), cv2.FONT_HERSHEY_SIMPLEX,
            #             0.35,
            #             (0, 0, 255), 1)
            cv2.putText(frame, "-->", (right_down_corner_x, int(left_up_corner_y + h / 2)), cv2.FONT_HERSHEY_SIMPLEX,
                        0.35,
                        (0, 0, 255), 1)
        if self.status == 4:
            cv2.putText(frame, "<<<", (left_up_corner_x - shift, int(left_up_corner_y + h / 2)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.35,
                        (0, 0, 255), 1)
            cv2.putText(frame, "B", (left_up_corner_x - shift, left_up_corner_y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.35,
                        (0, 0, 255), 1)
            cv2.putText(frame, "|> ||", (int(left_up_corner_x + w / 2) - shift, left_up_corner_y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.35,
                        (0, 0, 255), 1)
            # cv2.putText(frame, "Prawo góra", (right_down_corner_x, left_up_corner_y), cv2.FONT_HERSHEY_SIMPLEX,
            #             0.35,
            #             (0, 0, 255), 1)
            cv2.putText(frame, ">>>", (right_down_corner_x, int(left_up_corner_y + h / 2)), cv2.FONT_HERSHEY_SIMPLEX,
                        0.35,
                        (0, 0, 255), 1)

    def operate_cropped_file(self, thresh, img):

        if thresh is not None and img is not None:

            im2, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

            try:
                contour = max(contours, key=lambda x: cv.contourArea(x))

                x, y, w, h = cv.boundingRect(contour)

                cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 0)

                if x == 0 and y == 0:
                    self.status_move = 3
                else:
                    if x + w == img.shape[1] and y == 0:
                        self.status_move = 4
                    else:
                        if x + w == img.shape[1]:
                            self.status_move = 1
                        else:
                            if x == 0:
                                self.status_move = -1
                            else:
                                if y == 0:
                                    self.status_move = 2
                                else:
                                    self.status_move = 0

                hull = cv.convexHull(contour)

                drawing = np.zeros(img.shape, np.uint8)
                cv.drawContours(drawing, [contour], -1, (0, 255, 0), 0)
                cv.drawContours(drawing, [hull], -1, (0, 0, 255), 0)

                hull = cv.convexHull(contour, returnPoints=False)
                defects = cv.convexityDefects(contour, hull)
                if defects is not None:
                    count_defects = 0

                    for i in range(defects.shape[0]):
                        s, e, f, d = defects[i, 0]
                        start = tuple(contour[s][0])
                        end = tuple(contour[e][0])
                        far = tuple(contour[f][0])

                        a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                        b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                        c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                        angle = (math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180) / 3.14

                        if angle <= 90:
                            count_defects += 1
                            cv.circle(img, far, 1, [0, 0, 255], -1)

                        cv.line(img, start, end, [0, 255, 0], 2)
                    if not self.block:
                        self.status = count_defects

                    all = np.hstack((drawing, img))
                    # cv.imshow("Contours", all)

            except ValueError:
                print("err or")

    def start(self):

        capture = cv2.VideoCapture(0)

        key_pressed = 'q'

        fist_cascade = cv2.CascadeClassifier("/home/rafal/PycharmProjects/Python2/fist_v3.xml")

        main = "main"
        cv2.namedWindow(main)  # Create a named window
        cv2.moveWindow(main, 1800, 0)

        thresh1 = None
        darkness = 80
        flag = 1
        ly = 0
        lx = 0
        lw = 0
        lh = 0
        self.block = False
        # first_gray = None
        fist_detection = True
        mode = 2
        detection = False
        time_to_set = 5
        last_modes = np.zeros(time_to_set)
        i = 0
        while capture.isOpened() and (not self.leave):
            print(last_modes, i, self.status)
            '''Reading image:'''
            ret, frame = capture.read()

            if ret == False:
                print("Failed to catch")

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            fist = fist_cascade.detectMultiScale(gray, 1.3, 5)

            if flag == 1:
                cropped_image = None
                cropped_thresh = None

            if fist_detection:

                for x, y, w, h in fist:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    self.block = False
                    if fist != ():
                        ly = x
                        lx = y
                        lw = w
                        lh = h
                        flag = 0

            if flag == 0:

                left_up_corner_y = lx - lw
                right_down_corner_y = lx + 2 * lw
                left_up_corner_x = ly - lh
                right_down_corner_x = ly + 2 * lh
                if left_up_corner_y < 0:
                    left_up_corner_y = 0
                if right_down_corner_y > frame.shape[1]:
                    right_down_corner_y = frame.shape[1]
                if left_up_corner_x < 0:
                    left_up_corner_x = 0
                if right_down_corner_x > frame.shape[1]:
                    right_down_corner_x: frame.shape[1]
                cropped_image = frame[left_up_corner_y:right_down_corner_y, left_up_corner_x:right_down_corner_x]
                if thresh1 is not None:
                    cropped_thresh = thresh1[left_up_corner_y:right_down_corner_y, left_up_corner_x:right_down_corner_x]
                    cv2.rectangle(frame, (left_up_corner_x, left_up_corner_y),
                                  (right_down_corner_x, right_down_corner_y), (255, 255, 0))
                # if cropped_image != []:
                #
                #     cv2.imshow('sd', cropped_image)

                if detection:
                    self.operate_cropped_file(cropped_thresh, cropped_image)
                    last_modes[i] = self.status
                    i += 1
                    if i == time_to_set:
                        i = 0
                    if all_same(last_modes):
                        self.block = True
                        self.making_output(frame,left_up_corner_y,left_up_corner_x,right_down_corner_y,right_down_corner_x)

            cv2.imshow(main, frame)

            # difference = None
            if gray is not None:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (21, 21), 0)

                # In each iteration, calculate absolute difference between current frame and reference frame
                # difference = cv2.absdiff(gray, first_gray)
                # median = cv2.medianBlur(difference, 15)
                median2 = cv2.medianBlur(gray, 15)
                # difference = cv2.GaussianBlur(difference, (40, 40), 0)
                # Apply thresholding to eliminate noise
                # ret, thresh2 = cv.threshold(median, darkness, 255, cv.THRESH_BINARY)
                ret, thresh1 = cv.threshold(median2, darkness, 255, cv.THRESH_BINARY)
                cv2.imshow("get", thresh1)
                # cv2.imshow("get2", thresh2)

                # if mode % 2 == 0:
                #     thresh1 = thresh2

            # '''Label printing:'''
            # if printing_label:
            #     cv2.rectangle(output, (0, 0), (700, 100), (255, 255, 0), cv2.FILLED)
            #     cv2.putText(output,
            #                 "Callibrate threshold using W and S key untill your hand will have good contrast with background.",
            #                 (15, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            #     cv2.putText(output,
            #                 "Callibrate gausianBlur using E and D key untill your hand will have good contrast with background.",
            #                 (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            #     cv2.putText(output,
            #                 "Callibrate medianBlur using R and F key untill your hand will have good contrast with background.",
            #                 (15, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            #     cv2.putText(output,
            #                 "Use your mouse to specify hand gesture catching region",
            #                 (15, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            #     cv2.putText(output,
            #                 "WARNING: Select area with the greatest contrast beetween background and your hand",
            #                 (15, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            #     cv2.putText(output,
            #                 "When finished - press ENTER",
            #                 (15, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            #     cv2.putText(output,
            #                 "C - toggle label visibility",
            #                 (15, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            #     cv2.putText(output,
            #                 "Q - finish",
            #                 (15, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            #

            key_pressed = cv2.waitKey(10)

            # if key_pressed == ord('p'):
            #     ret, first = capture.read()
            #     first_gray = cv2.cvtColor(first, cv2.COLOR_BGR2GRAY)
            #
            #     first_gray = cv2.GaussianBlur(first_gray, (21, 21), 0)
            #     flag = 1

            if key_pressed == ord('l'):
                fist_detection = not fist_detection

            if key_pressed == ord('h'):
                detection = not detection

            if key_pressed == ord('+'):
                darkness += 1

            if key_pressed == ord('-'):
                darkness -= 1
                if darkness < 0:
                    darkness = 0
            if key_pressed == ord('k'):
                mode += 1

            if key_pressed == ord('q'):
                self.leave = True
            if key_pressed != -1:
                pass
        '''Cleaning:'''
        cv2.destroyAllWindows()
        capture.release()

    def multitasking_keyboard_input_testing(self):
        '''This method is made only to test if browser takes input from that thread'''
        capture = cv2.VideoCapture(0)
        ret, frame = capture.read()
        cv2.imshow("aaa", ret)
        key_pressed = cv2.waitKey(10)
        while key_pressed != ord('q'):
            self.status = key_pressed
            key_pressed = cv2.waitKey(10)
        cv2.destroyAllWindows()
        capture.release()
