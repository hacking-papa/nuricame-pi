#!/usr/bin/env python3
# -*-coding:utf-8-*-

import argparse

import cv2 as cv
import numpy as np

import ZhangSuen

parser = argparse.ArgumentParser()
parser.add_argument("--input", help="Path to input image.", required=True)
parser.add_argument("--width", help="Resize input image to a specific width.", default=384, type=int)
parser.add_argument("--height", help="Resize input image to a specific height.", default=384, type=int)
parser.add_argument("--output", help="Path to output image.", default="output.jpg")
args = parser.parse_args()


class CropLayer(object):
    def __init__(self, params, blobs):
        self.x_start = 0
        self.x_end = 0
        self.y_start = 0
        self.y_end = 0

    def getMemoryShapes(self, inputs):
        input_shape, target_shape = inputs[0], inputs[1]
        batch_size, num_channels = input_shape[0], input_shape[1]
        height, width = target_shape[2], target_shape[3]

        self.y_start = int((input_shape[2] - target_shape[2]) / 2)
        self.x_start = int((input_shape[3] - target_shape[3]) / 2)
        self.y_end = self.y_start + height
        self.x_end = self.x_start + width

        return [[batch_size, num_channels, height, width]]

    def forward(self, inputs):
        return [inputs[0][:, :, self.y_start:self.y_end, self.x_start:self.x_end]]


net = cv.dnn.readNetFromCaffe("deploy.prototxt", "hed_pretrained_bsds.caffemodel")
cv.dnn_registerLayer("Crop", CropLayer)

image = cv.imread(args.input)
image = cv.resize(image, (args.width, args.height))
input_blob = cv.dnn.blobFromImage(image, scalefactor=1.0, size=(args.width, args.height),
                                  mean=(104.00698793, 116.66876762, 122.67891434),
                                  swapRB=False, crop=False)
net.setInput(input_blob)
output = net.forward()

output = output[0, 0]
output = cv.resize(output, (image.shape[1], image.shape[0]))

# output = cv.cvtColor(output, cv.COLOR_GRAY2BGR)
output = 255 * output
output = output.astype(np.uint8)
output = cv.bitwise_not(output)

# output = ZhangSuen.ZhangSuen(output)

print(f"type(output): {type(output)}")
print(f"np.max(output): {np.max(output)}")
print(f"np.min(output): {np.min(output)}")
print(f"output.shape: {output.shape}")

cv.imwrite(args.output, output)
# output.save(args.output)
