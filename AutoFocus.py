#!/usr/bin/env python3
import os
import time
from datetime import datetime

import cv2

try:
    import picamera
    from picamera.array import PiRGBArray
except:
    sys.exit(0)


def focusing(val):
    value = (val << 4) & 0x3ff0
    data1 = (value >> 8) & 0x3f
    data2 = value & 0xf0
    os.system("i2cset -y 0 0x0c %d %d" % (data1, data2))


def sobel(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img_sobel = cv2.Sobel(img_gray, cv2.CV_16U, 1, 1)
    return cv2.mean(img_sobel)[0]


def laplacian(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img_sobel = cv2.Laplacian(img_gray, cv2.CV_16U)
    return cv2.mean(img_sobel)[0]


def calculation(camera):
    raw_capture = PiRGBArray(camera)
    camera.capture(raw_capture, format="bgr", use_video_port=True)
    image = raw_capture.array
    raw_capture.truncate(0)
    return laplacian(image)


def main():
    camera = picamera.PiCamera()
    camera.start_preview()
    camera.resolution = (640, 480)

    print("Start focusing")

    max_index = 10
    max_value = 0.0
    last_value = 0.0
    dec_count = 0
    focal_distance = 10

    while focal_distance < 1000:
        focusing(focal_distance)
        val = calculation(camera)
        if max_value < val:
            max_index = focal_distance
            max_value = val

        if val < last_value:
            dec_count += 1
        else:
            dec_count = 0
        if 6 < dec_count:
            break
        last_value = val
        focal_distance += 10

    focusing(max_index)
    time.sleep(1)
    camera.resolution = (2592, 1944)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    camera.capture(f"original_{now}.jpg")
    print("max index = %d, max value = %lf" % (max_index, max_value))
    camera.stop_preview()
    camera.close()


if __name__ == "__main__":
    main()
