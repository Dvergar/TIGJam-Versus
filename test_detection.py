import sys
import math

import cv2
import numpy as np
np.set_printoptions(threshold='nan')


def show_image():
    image = cv2.imread("assets/map.png")
    height, width, _ = image.shape

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    thresh, im_bw = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    global contours
    _, contours, _ = cv2.findContours(im_bw.copy(),
                               cv2.RETR_LIST ,
                               cv2.CHAIN_APPROX_SIMPLE)

    global points
    points = []
    for shape in contours:
        points.append([point[0] for point in shape])

    cv2.drawContours(image, contours, -1, (0,255,0), 3)
    cv2.imshow("OpenCV visualization", image)
    
def on_t_min(position):
    global t_min
    t_min = position
    show_image()
    
def on_t_max(position):
    global t_max
    t_max = position
    show_image()
    
def on_dilatation(position):
    global dilatation
    dilatation = position
    show_image()
    
def on_hough_method(position):
    global houghmethod
    if position == 0:
        houghmethod = cv2.CV_HOUGH_STANDARD
    elif position == 1:
        houghmethod = cv2.CV_HOUGH_PROBABILISTIC
    elif position == 2:
       houghmethod =  cv2.CV_HOUGH_MULTI_SCALE
    show_image()
       
def on_hough_rho(position):
    global rho
    rho = position
    show_image()
    
def on_hough_theta(position):
    global theta
    theta = position
    show_image()
    
def on_hough_threshold(position):
    global threshold
    threshold = position
    show_image()

def on_vis(position):
    global vis
    vis = position
    show_image()

    
_WIDTH = 640
_HEIGHT = 480
t_min = 0
t_max = 100
points = None
dilatation = 4
vis = 1
houghmethod = 1
rho = 1
threshold = 15
theta = 180

# cv2.namedWindow("OpenCV visualization", 2)
# cv2.createTrackbar("t min", "OpenCV visualization", t_min, 1000, on_t_min)
# cv2.createTrackbar("t max", "OpenCV visualization", t_max, 1000, on_t_max)
# cv2.createTrackbar("dilatation", "OpenCV visualization", dilatation, 10, on_dilatation)

# cv2.createTrackbar("H method", "OpenCV visualization", houghmethod, 2, on_hough_method)
# cv2.createTrackbar("H rho", "OpenCV visualization", rho, 100, on_hough_rho)
# cv2.createTrackbar("H theta", "OpenCV visualization", theta, 360, on_hough_theta)
# cv2.createTrackbar("H threshold", "OpenCV visualization", threshold, 100, on_hough_threshold)

# cv2.createTrackbar ("Pts/Lines", "OpenCV visualization", vis, 2, on_vis)

show_image()
cv2.waitKey()

##### Pyglet representation ######

import math
import pyglet
from pyglet.gl import *
from pyglet.window import key

window = pyglet.window.Window(_WIDTH,_HEIGHT, "Pyglet visualization")
    
keys = key.KeyStateHandler()
window.push_handlers(keys)

img = pyglet.resource.image("assets/car2.png")
char = pyglet.sprite.Sprite(img)
char.x = char.y = 100

img2 = pyglet.resource.image("assets/map.png")
bg = pyglet.sprite.Sprite(img2)

def move(direction):
    directions = {
            'up' : (0, 10),
            'down' : (0, -10), 
            'left' : (-10, 0),
            'right' : (10, 0),
            }
    dx, dy = directions[direction]
    oldx, oldy = char.x, char.y
    char.set_position(char.x+dx, char.y+dy)
    
    # for point in points:
    #     if char.x < point[0] < char.x + 16 and char.y < _HEIGHT-point[1] < char.y + 16:
    #         char.x, char.y = oldx, oldy


keys = key.KeyStateHandler()
window.push_handlers(keys)

input = {
        key.UP : (move, 'up'),
        key.DOWN : (move, 'down'),
        key.LEFT : (move, 'left'),
        key.RIGHT : (move, 'right'),
        }

        
def update(dt):
    for key, key_pressed in keys.iteritems():
        if key_pressed and key in input:
            print("plop")
            action = input[key][0]
            arguments = input[key][1]
            action(arguments)
    
    
@window.event
def on_draw():
    window.clear()
    bg.draw()
    char.draw()
    pyglet.gl.glColor4f(0, 1, 0, 1.0) 
    if vis == 1:
        for shape in points:
            for i, point in enumerate(shape):
                if i != len(shape)-1:
                    pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (shape[i][0], _HEIGHT-shape[i][1], shape[i+1][0], _HEIGHT-shape[i+1][1])))

    elif vis == 2:
        pass
        # for i, point in enumerate(points):
        #     if i != len(points)-1:
        #         pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (points[i][0], _HEIGHT-points[i][1], points[i+1][0], _HEIGHT-points[i+1][1])))
    
pyglet.clock.schedule_interval(update, 1/30.0)
pyglet.app.run()