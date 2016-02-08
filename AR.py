import sys
sys.path.append("C:\OpenCV2.1\Python2.6\Lib\site-packages")
import cv
import math

def show_image():
    gray = cv.CreateImage((image.width, image.height), 8, 1)
    edge = cv.CreateImage((image.width, image.height), 8, 1)

    cv.CvtColor(image, gray, cv.CV_BGR2GRAY)

    cv.Canny(gray, edge, t_min, t_max, 3)
    
    cv.Dilate(edge, edge, None, dilatation)

    storage = cv.CreateMemStorage(0)

    contours = cv.FindContours(edge,
                               storage,
                               cv.CV_RETR_TREE,
                               cv.CV_CHAIN_APPROX_SIMPLE,
                               (0,0))
                               
    # houghlines = cv.HoughLines2(edge, storage, houghmethod, rho, math.radians(theta), threshold)

    # global points
    # points = [(line) for line in contours]

    # global points
    # points = []
    # if contours:
        # while contours:
            # seq = [(x,y) for x,y in contours if x < _WIDTH]
            # points.append(seq);
            # contours = contours.h_next()
            
    global points
    points = []
    if contours:
        while contours:
            seq = [(x,y) for x,y in contours if x < _WIDTH]
            points.extend(seq);
            contours = contours.h_next()
                               
    cv.ShowImage ("OpenCV visualization", edge)

    
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
        houghmethod = cv.CV_HOUGH_STANDARD
    elif position == 1:
        houghmethod = cv.CV_HOUGH_PROBABILISTIC
    elif position == 2:
       houghmethod =  cv.CV_HOUGH_MULTI_SCALE 
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


image = cv.LoadImage("stuff.jpg")

cv.NamedWindow ("OpenCV visualization", 2)
cv.CreateTrackbar ("t min", "OpenCV visualization", t_min, 1000, on_t_min)
cv.CreateTrackbar ("t max", "OpenCV visualization", t_max, 1000, on_t_max)
cv.CreateTrackbar ("dilatation", "OpenCV visualization", dilatation, 10, on_dilatation)

cv.CreateTrackbar ("H method", "OpenCV visualization", houghmethod, 2, on_hough_method)
cv.CreateTrackbar ("H rho", "OpenCV visualization", rho, 100, on_hough_rho)
cv.CreateTrackbar ("H theta", "OpenCV visualization", theta, 360, on_hough_theta)
cv.CreateTrackbar ("H threshold", "OpenCV visualization", threshold, 100, on_hough_threshold)

cv.CreateTrackbar ("Pts/Lines", "OpenCV visualization", vis, 2, on_vis)

show_image()

# cv.WaitKey()

##### Pyglet representation ######

import math
import pyglet
from pyglet.gl import *
from pyglet.window import key

window = pyglet.window.Window(_WIDTH,_HEIGHT, "Pyglet visualization")
    
keys = key.KeyStateHandler()
window.push_handlers(keys)

img = pyglet.resource.image("char.png")
char = pyglet.sprite.Sprite(img)
char.x = char.y = 100

img2 = pyglet.resource.image("stuff.jpg")
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
    
    for point in points:
        if char.x < point[0] < char.x + 16 and char.y < _HEIGHT-point[1] < char.y + 16:
            char.x, char.y = oldx, oldy


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
            print "plop"
            action = input[key][0]
            arguments = input[key][1]
            action(arguments)
    

    
@window.event
def on_draw():
    window.clear()
    bg.draw()
    char.draw()
    if vis == 1:
        for point in points:
            pyglet.gl.glRectf(point[0], _HEIGHT-point[1], point[0]+2, _HEIGHT-point[1]+2)
        
        # for shape in points:
            # for i, point in enumerate(shape):
                # if i != len(shape)-1:
                    # pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (shape[i][0], _HEIGHT-shape[i][1], shape[i+1][0], _HEIGHT-shape[i+1][1])))
        
        # for line in lines:
            # ax = line[0][0]
            # ay = line[0][1]
            # bx = line[1][0]
            # by = line[1][1]
            
            # pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (ax, _HEIGHT-ay, bx, _HEIGHT-by)))
            
            
    elif vis == 2:
        for i, point in enumerate(points):
            if i != len(points)-1:
                pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (points[i][0], _HEIGHT-points[i][1], points[i+1][0], _HEIGHT-points[i+1][1])))
    
pyglet.clock.schedule_interval(update, 1/30.0)
pyglet.app.run()