import sys

import cv2
import numpy as np
from PIL import Image


class ShapeDetector:
    def __init__(self, winwidth, winheight):
        self.winwidth = winwidth
        self.winheight = winheight
        self.t_min = 80
        self.t_max = 105

    def setcapturetype(self, type, img=None):
        self.type = type
        self.img = img
        if type == "cam":
            self.cam = cv2.VideoCapture(0)
            self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def create_sliders(self):
        cv.NamedWindow ("Tweak sliders", 2)
        cv.CreateTrackbar ("t min", "Tweak sliders", self.t_min, 500, self.on_t_min)
        cv.CreateTrackbar ("t max", "Tweak sliders", self.t_max, 500, self.on_t_max)

    def on_t_min(self, position):
        self.t_min = position

    def on_t_max(self, position):
        self.t_max = position

    def release(self):
        if self.type == "cam":
            del(self.cam)

    def get_points(self):
        if self.type == "pic":
            image = cv2.imread(self.img)
        elif self.type == "cam":
            _, image = self.cam.read()

        height, width, channels = image.shape
        pilimage = Image.frombytes("RGB", (width, height), image.tostring())
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        thresh, im_bw = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        _, contours, _ = cv2.findContours(im_bw,
                                   cv2.RETR_LIST,
                                   cv2.CHAIN_APPROX_SIMPLE)

        points = []
        for shape in contours:
            points.append([point[0] for point in shape])

        return points, pilimage
