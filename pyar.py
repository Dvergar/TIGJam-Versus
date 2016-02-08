import sys
import cv
import Image


class ShapeDetector:
    def __init__(self, winwidth, winheight):
        self.winwidth = winwidth
        self.winheight = winheight
        self.t_min = 80
        self.t_max = 105
        # self.create_sliders()

    def setcapturetype(self, type, img=None):
        self.type = type
        self.img = img
        if type == "cam":
            self.cam = cv.CaptureFromCAM(-1)
            cv.SetCaptureProperty( self.cam, cv.CV_CAP_PROP_FRAME_WIDTH, 640  )
            cv.SetCaptureProperty( self.cam, cv.CV_CAP_PROP_FRAME_HEIGHT, 480  )

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
            image = cv.LoadImage(self.img)
        elif self.type == "cam":
            image = cv.QueryFrame(self.cam)

        pilimage = Image.fromstring("RGB", cv.GetSize(image), image.tostring())
        gray = cv.CreateImage((image.width, image.height), 8, 1)
        edge = cv.CreateImage((image.width, image.height), 8, 1)

        cv.CvtColor(image, gray, cv.CV_BGR2GRAY)
        cv.Canny(gray, edge, self.t_min, self.t_max, 3)

        storage = cv.CreateMemStorage(0)
        contours = cv.FindContours(edge,
                                   storage,
                                   cv.CV_RETR_TREE,
                                   cv.CV_CHAIN_APPROX_SIMPLE,
                                   (0,0))

        points = []
        if contours:
            while contours:
                seq = [(x,y) for x,y in contours if x < self.winwidth]
                points.append(seq);
                contours = contours.h_next()

        return points, pilimage
