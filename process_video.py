import cv2
import numpy as np

def main():
    print(cv2.__version__)
    vid = cv2.VideoCapture("./media/led2.mov")
    if not vid.isOpened():
        print("video not opened!")
        return

    frame_cnt = 0
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
        mask = cv2.inRange(color, lower_red, upper_red)
        mask = cv2.blur(mask, (7, 7))

        # create contours from mask
        image, contours, h = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        mask = cv2.drawContours(mask, contours, -1, (255, 255, 0), -1)

        # apply mask to image
        res = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.putText(res, str(frame_cnt), (10,25), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255))
        cv2.namedWindow("Frame", cv2.WINDOW_NORMAL), cv2.imshow("Frame", frame), cv2.resizeWindow("Frame", 800, 800)
        cv2.namedWindow("Mask", cv2.WINDOW_NORMAL), cv2.imshow("Mask", mask), cv2.resizeWindow("Mask", 800, 800)
        cv2.namedWindow("Res", cv2.WINDOW_NORMAL), cv2.imshow("Res", res), cv2.resizeWindow("Res", 800, 800)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    vid.release()
    cv2.destroyAllWindows()




if __name__ == '__main__':
    # red = np.uint8([[[0,0,255]]])
    # hsv_red = cv2.cvtColor(red, cv2.COLOR_BGR2HSV)
    # print(hsv_red)
    main()