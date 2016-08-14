import cv2
import numpy as np
import sys
import time

red_on = False
lower_contour_bound = 100
upper_contour_bound = 1000


def setRed(b, control_list, time):
    global red_on
    if b != red_on:
        red_on = b
        control_list.append("Red-" + str(time))


def setBlue(b, control_list, time):
    global blue_on
    if b != blue_on:
        blue_on = b
        control_list.append("Blue-" + str(time))

def setGreen(b, control_list, time):
    global green_on
    if b != green_on:
        green_on = b
        control_list.append("Red-" + str(time))

def proc_vid(vid_path):
    global red_on
    global lower_contour_bound
    global upper_contour_bound

    control_list = []
    print(cv2.__version__)
    vid = cv2.VideoCapture(vid_path)
    if not vid.isOpened():
        print("video not opened!")
        return

    frame_cnt = 0
    start_time = time.clock()
    while(vid.isOpened()):
        ret, frame = vid.read()
        frame_cnt += 1
        if ret is False:
            break
        color = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # print frame number on frame

        # extract red led
        lower_red = np.array([0, 0, 255]) # 0, 0, 100
        upper_red = np.array([100, 255, 255]) # 35, 47, 98

        # create color mask
        mask_red = cv2.inRange(color, lower_red, upper_red)
        mask_red = cv2.blur(mask_red, (7, 7))

        # create contours from mask
        image_red, contours_red, h_red = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        mask_red = cv2.drawContours(mask_red, contours_red, -1, (255, 255, 0), -1)

        area_red = 0
        for c in contours_red:
            if cv2.contourArea(c) > area_red:
                area_red = cv2.contourArea(contours_red[0])
        if area_red > upper_contour_bound:
            setRed(True, control_list, time.clock())
        elif (area_red < lower_contour_bound or len(contours_red) == 0) and red_on:
            setRed(False, control_list, time.clock())


        # apply mask to image
        res = cv2.bitwise_and(frame, frame, mask=mask_red)

        cv2.putText(res, str(frame_cnt), (10,25), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255))
        cv2.namedWindow("Frame", cv2.WINDOW_NORMAL), cv2.imshow("Frame", frame), cv2.resizeWindow("Frame", 800, 800)
        cv2.namedWindow("Mask", cv2.WINDOW_NORMAL), cv2.imshow("Mask", mask_red), cv2.resizeWindow("Mask", 800, 800)
        cv2.namedWindow("Res", cv2.WINDOW_NORMAL), cv2.imshow("Res", res), cv2.resizeWindow("Res", 800, 800)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()

    return control_list


if __name__ == '__main__':
    file_name = "./control_lists/" + sys.argv[2] + ".clist"
    vid_path = sys.argv[1]
    control_list = proc_vid(vid_path)
    file = open(file_name, 'w+')
    if len(control_list) > 0:
        file.write(" : ".join(control_list))
    file.close()
