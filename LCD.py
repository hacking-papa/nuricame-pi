#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time

import spidev as SPI
from PIL import Image, ImageDraw

import ST7789

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 24
bus = 0
device = 0

# 240x240 display with hardware SPI:
display = ST7789.ST7789(SPI.SpiDev(bus, device), RST, DC, BL)

# Initialize library.
display.init()

# Clear display.
display.clear()

# Create blank image for drawing.
image1 = Image.new("RGB", (display.width, display.height), "WHITE")
draw = ImageDraw.Draw(image1)

print("***draw line")
draw.line([(60, 60), (180, 60)], fill="BLUE", width=5)
draw.line([(180, 60), (180, 180)], fill="BLUE", width=5)
draw.line([(180, 180), (60, 180)], fill="BLUE", width=5)
draw.line([(60, 180), (60, 60)], fill="BLUE", width=5)

print("***draw rectangle")
draw.rectangle([(70, 70), (170, 80)], fill="RED")

print("***draw text")
draw.text((90, 70), "WaveShare ", fill="BLUE")
draw.text((90, 120), "Electronic ", fill="BLUE")
draw.text((90, 140), "1.3inch LCD ", fill="BLUE")
display.show_image(image1, 0, 0)

time.sleep(3)

image = Image.open("sample_images/sample_240x240.jpg")
display.show_image(image, 0, 0)
