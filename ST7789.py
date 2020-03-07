# -*- coding:utf-8 -*-

import time

import RPi.GPIO as GPIO
import numpy as np


class ST7789(object):
    """ Class for ST7789  240*240 1.3inch OLED displays. """

    def __init__(self, spi, rst=27, dc=25, bl=24):
        self.width = 240
        self.height = 240
        # Initialize DC RST pin
        self._dc = dc
        self._rst = rst
        self._bl = bl
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self._dc, GPIO.OUT)
        GPIO.setup(self._rst, GPIO.OUT)
        GPIO.setup(self._bl, GPIO.OUT)
        GPIO.output(self._bl, GPIO.HIGH)
        # Initialize SPI
        self._spi = spi
        self._spi.max_speed_hz = 40000000

    def command(self, cmd):
        GPIO.output(self._dc, GPIO.LOW)
        self._spi.writebytes([cmd])

    def data(self, val):
        GPIO.output(self._dc, GPIO.HIGH)
        self._spi.writebytes([val])

    def init(self):
        """ Initialize display """
        self.reset()

        self.command(0x36)
        self.data(0x70)  # self.data(0x00)

        self.command(0x3A)
        self.data(0x05)

        self.command(0xB2)
        self.data(0x0C)
        self.data(0x0C)
        self.data(0x00)
        self.data(0x33)
        self.data(0x33)

        self.command(0xB7)
        self.data(0x35)

        self.command(0xBB)
        self.data(0x19)

        self.command(0xC0)
        self.data(0x2C)

        self.command(0xC2)
        self.data(0x01)

        self.command(0xC3)
        self.data(0x12)

        self.command(0xC4)
        self.data(0x20)

        self.command(0xC6)
        self.data(0x0F)

        self.command(0xD0)
        self.data(0xA4)
        self.data(0xA1)

        self.command(0xE0)
        self.data(0xD0)
        self.data(0x04)
        self.data(0x0D)
        self.data(0x11)
        self.data(0x13)
        self.data(0x2B)
        self.data(0x3F)
        self.data(0x54)
        self.data(0x4C)
        self.data(0x18)
        self.data(0x0D)
        self.data(0x0B)
        self.data(0x1F)
        self.data(0x23)

        self.command(0xE1)
        self.data(0xD0)
        self.data(0x04)
        self.data(0x0C)
        self.data(0x11)
        self.data(0x13)
        self.data(0x2C)
        self.data(0x3F)
        self.data(0x44)
        self.data(0x51)
        self.data(0x2F)
        self.data(0x1F)
        self.data(0x1F)
        self.data(0x20)
        self.data(0x23)

        self.command(0x21)

        self.command(0x11)

        self.command(0x29)

    def reset(self):
        """ Reset the display """
        GPIO.output(self._rst, GPIO.HIGH)
        time.sleep(0.01)
        GPIO.output(self._rst, GPIO.LOW)
        time.sleep(0.01)
        GPIO.output(self._rst, GPIO.HIGH)
        time.sleep(0.01)

    def set_windows(self, x_start, y_start, x_end, y_end):
        # set the X coordinates
        self.command(0x2A)
        self.data(0x00)  # Set the horizontal starting point to the high octet
        self.data(x_start & 0xff)  # Set the horizontal starting point to the low octet
        self.data(0x00)  # Set the horizontal end to the high octet
        self.data((x_end - 1) & 0xff)  # Set the horizontal end to the low octet

        # set the Y coordinates
        self.command(0x2B)
        self.data(0x00)
        self.data((y_start & 0xff))
        self.data(0x00)
        self.data((y_end - 1) & 0xff)

        self.command(0x2C)

    def show_image(self, image, x_start, y_start):
        """ Set buffer to value of Python Imaging Library image. """
        """ Write display buffer to physical display """
        img_width, img_height = image.size
        if img_width != self.width or img_height != self.height:
            raise ValueError(f"Image must be same dimensions as display ({self.width}x{self.height}).")
        img = np.asarray(image)
        pix = np.zeros((self.width, self.height, 2), dtype=np.uint8)
        pix[..., [0]] = np.add(np.bitwise_and(img[..., [0]], 0xF8), np.right_shift(img[..., [1]], 5))
        pix[..., [1]] = np.add(np.bitwise_and(np.left_shift(img[..., [1]], 3), 0xE0), np.right_shift(img[..., [2]], 3))
        pix = pix.flatten().tolist()
        self.set_windows(0, 0, self.width, self.height)
        GPIO.output(self._dc, GPIO.HIGH)
        for i in range(0, len(pix), 4096):
            self._spi.writebytes(pix[i:i + 4096])

    def clear(self):
        """ Clear contents of image buffer """
        _buffer = [0xff] * (self.width * self.height * 2)
        self.set_windows(0, 0, self.width, self.height)
        GPIO.output(self._dc, GPIO.HIGH)
        for i in range(0, len(_buffer), 4096):
            self._spi.writebytes(_buffer[i:i + 4096])
