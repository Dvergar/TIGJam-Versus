import pyglet
import sys
sys.path.append("C:\OpenCV2.1\Python2.6\Lib\site-packages")
from pyglet.window import key
from math import cos, sin, radians, exp
import collision

def rotate2d(degrees,point,origin):
    """
    A rotation function that rotates a point around a point
    to rotate around the origin use [0,0]
    """
    x = point[0] - origin[0]
    yorz = point[1] - origin[1]
    newx =    (x * cos(radians(-degrees)) - yorz * sin(radians(-degrees)))
    newyorz = (x * sin(radians(-degrees)) + yorz * cos(radians(-degrees)))
    newx += origin[0]
    newyorz += origin[1]

    return newx,newyorz

class Sprite(pyglet.sprite.Sprite):
    def __init__(self, img, x, y):
        image = pyglet.resource.image(img)
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2
        pyglet.sprite.Sprite.__init__(self, image, x, y)

    def __get_centerx(self):
        return self.x + self.width // 2
    centerx = property(__get_centerx)

    def __get_centery(self):
        return self.y + self.height // 2
    centery = property(__get_centery)

    def __get_left(self):
        return self.x - self.width // 2
    left = property(__get_left)

    def __get_right(self):
        return self.x + self.width // 2
    right = property(__get_right)

    def __get_top(self):
        return self.y + self.height // 2
    top = property(__get_top)

    def __get_bottom(self):
        return self.y - self.height // 2
    bottom = property(__get_bottom)

    def intersect(self, x,y):
        if self.left < x < self.right and self.bottom < y < self.top:
            return True

    def __get_topleft(self):
        return rotate2d(self.rotation, (self.left,self.top), (self.x,self.y))
    topleft = property(__get_topleft)

    def __get_topright(self):
        return rotate2d(self.rotation, (self.right,self.top), (self.x,self.y))
    topright = property(__get_topright)

    def __get_bottomright(self):
        return rotate2d(self.rotation, (self.right,self.bottom), (self.x,self.y))
    bottomright = property(__get_bottomright)

    def __get_bottomleft(self):
        return rotate2d(self.rotation, (self.left,self.bottom), (self.x,self.y))
    bottomleft = property(__get_bottomleft)

    def get_rect(self):
        corners = [self.topleft, self.topright, self.bottomright, self.bottomleft]
        left = min(x for x, y in corners)
        right = max(x for x,y in corners)
        top = max(y for x,y in corners)
        bottom = min(y for x,y in corners)
        return left, top, right, bottom

##################################

def overlap2(Aleft, Atop, Aright, Abottom, Bleft, Btop, Bright, Bbottom):
    if Aright <= Bleft:
        return False
    if Bright <= Aleft:
        return False
    if Atop <= Bbottom:
        return False
    if Btop <= Abottom:
        return False
    return True

def car_above(topleft, topright, bottomright, bottomleft, a,b):
    if bottomleft[1] > a*bottomleft[0] + b and bottomright[1] > a*bottomright[0] +b and topleft[1] > a*topleft[0] + b and topright[1] > a*topright[0] +b:
        return True

def car_below(topleft, topright, bottomright, bottomleft, a,b):
    if bottomleft[1] < a*bottomleft[0] + b and bottomright[1] < a*bottomright[0] +b and topleft[1] < a*topleft[0] + b and topright[1] < a*topright[0] +b:
        return True


window = pyglet.window.Window()
keys = key.KeyStateHandler()
window.push_handlers(keys)

car = Sprite("car2.png", 100,100)
car.oldx = car.x
car.oldy = car.y
# car.rotation = 10


points = [[ [152,123],[345,159] ],]
##points = [[(586, 478), (638, 478)], [(580, 478), (581, 478)], [(567, 478), (575, 478)], [(529, 478), (565, 478)], [(499, 478), (524, 478)], [(479, 478), (488, 478)], [(472, 478), (477, 478)], [(441, 478), (455, 478)], [(408, 478), (434, 478)], [(392, 478), (399, 478)], [(367, 478), (389, 478)], [(359, 478), (360, 478)], [(341, 478), (351, 478)], [(335, 478), (339, 478)], [(330, 478), (331, 478)], [(304, 478), (327, 478)], [(288, 478), (295, 478)], [(285, 478)], [(282, 478)], [(264, 478), (279, 478)], [(245, 478), (257, 478)], [(232, 478), (242, 478)], [(228, 478), (229, 478)], [(224, 478)], [(199, 478), (200, 478)], [(133, 478), (191, 478)], [(104, 478), (130, 478)], [(24, 478), (90, 478)], [(1, 478), (21, 478)], [(7, 170), (16, 170)], [(121, 167), (120, 168), (56, 168), (55, 169), (25, 169), (24, 170), (23, 170), (24, 170), (25, 169), (55, 169), (56, 168), (120, 168), (121, 167), (127, 167), (128, 168), (127, 167)], [(506, 1), (506, 78), (505, 79), (505, 114), (504, 115), (504, 116), (505, 117), (505, 122), (504, 123), (504, 158), (502, 160), (475, 160), (474, 161), (473, 161), (472, 160), (464, 160), (463, 161), (447, 161), (446, 162), (439, 162), (438, 161), (437, 162), (434, 162), (433, 161), (432, 162), (393, 162), (392, 163), (351, 163), (350, 164), (314, 164), (313, 163), (312, 163), (311, 164), (275, 164), (274, 165), (272, 165), (271, 164), (264, 164), (263, 165), (259, 165), (258, 164), (255, 164), (254, 165), (212, 165), (211, 166), (176, 166), (175, 167), (171, 167), (170, 166), (168, 166), (167, 167), (147, 167), (146, 166), (145, 166), (144, 167), (136, 167), (135, 168), (134, 167), (132, 167), (134, 167), (135, 168), (136, 167), (144, 167), (145, 166), (146, 166), (147, 167), (167, 167), (168, 166), (170, 166), (171, 167), (175, 167), (176, 166), (211, 166), (212, 165), (254, 165), (255, 164), (258, 164), (259, 165), (263, 165), (264, 164), (271, 164), (272, 165), (274, 165), (275, 164), (311, 164), (312, 163), (313, 163), (314, 164), (350, 164), (351, 163), (392, 163), (393, 162), (432, 162), (433, 161), (434, 162), (437, 162), (438, 161), (439, 162), (446, 162), (447, 161), (463, 161), (464, 160), (472, 160), (473, 161), (474, 161), (475, 160), (503, 160), (504, 159), (504, 123), (505, 122), (505, 117), (504, 116), (504, 115), (505, 114), (505, 79), (506, 78)]]
##points = [[(314, 164), (350, 164), (351, 163), (392, 163), (393, 162), (432, 162), (433, 161), (434, 162), (437, 162), (438, 161), (439, 162), (446, 162), (447, 161), (463, 161), (464, 160), (472, 160), (473, 161), (474, 161), (475, 160), (503, 160), (504, 159), (504, 123), (505, 122), (505, 117), (504, 116), (504, 115), (505, 114), (505, 79), (506, 78)]]

def on_update(dt):
    car.oldx,car.oldy = car.x, car.y

    if keys[key.UP]:
        car.y += 10
    if keys[key.DOWN]:
        car.y -= 10
    if keys[key.LEFT]:
        car.x -= 10
    if keys[key.RIGHT]:
        car.x += 10

    global points
    if keys[key.Z]:
        points[0][0][1] += 10
    if keys[key.D]:
        points[0][0][0] += 10
    if keys[key.S]:
        points[0][0][1] -= 10
    if keys[key.Q]:
        points[0][0][0] -= 10

    if keys[key.L]:
        car.rotation -= 10
    if keys[key.M]:
        car.rotation += 10


@window.event
def on_draw():
    window.clear()
    wallcollision, colpoints = collision.Collision(points, car)

    if wallcollision:
        print "collision"
##        responsevec = wallcollision.response()
##        mtv = wallcollision.getMTV()
##        print "mtv",mtv
##        car.x = car.x - mtv[0]
##        car.y = car.y - mtv[1]

##        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (200, 200, 200+int(mtv[0]*exp(100)), 200+int(mtv[1]*exp(100)))))

        if not 0 < car.x < 640 or not 0 < car.y < 480:
           pyglet.app.exit()

##        sx = sy = 300
##        tx, ty = sx+int(responsevec[0]*100), sy+int(responsevec[1]*100)
##        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (sx, sy, tx, ty)))
##        pyglet.gl.glRectf(tx, ty, tx+10,ty+10)

    ##############

    car.draw()
    pyglet.gl.glColor3f(1,1,1)

    for c, shape in enumerate(points):
        for i, point in enumerate(shape):
            # pyglet.gl.glRectf(shape[i][0], shape[i][1], shape[i][0]+5,shape[i][1]+5)
            if i != len(shape)-1:
                pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (shape[i][0], shape[i][1], shape[i+1][0], shape[i+1][1])))
            else:
                pyglet.gl.glRectf(shape[i][0], shape[i][1], shape[i][0]+5, shape[i][1]+5)

    pyglet.gl.glColor3f(1,0,0)
##    pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (colA[0], colA[1], colB[0], colB[1])))
    # CAR CORNERS
    # pyglet.gl.glColor3f(0,1,0)
    # pyglet.gl.glRectf(car.topleft[0], car.topleft[1], car.topleft[0]+5, car.topleft[1]+5)
    # pyglet.gl.glColor3f(0,0,1)
    # pyglet.gl.glRectf(car.topright[0], car.topright[1], car.topright[0]+5, car.topright[1]+5)
    # pyglet.gl.glColor3f(1,0,0)
    # pyglet.gl.glRectf(car.bottomright[0], car.bottomright[1], car.bottomright[0]+5, car.bottomright[1]+5)
    # pyglet.gl.glColor3f(0,1,1)
    # pyglet.gl.glRectf(car.bottomleft[0], car.bottomleft[1], car.bottomleft[0]+5, car.bottomleft[1]+5)

    # pyglet.gl.glRectf(car.x, car.y, car.x+5, car.y+5)
    # pyglet.gl.glRectf(ix, iy, ix+5, iy+5)

    # REFLECTION
    # pyglet.gl.glColor3f(0,1,0)
    # pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (int(ix), int(iy), int(ix+Rx*1000), int(iy+Ry*1000) )))

    # DROITE CAR
    # pyglet.gl.glColor3f(1,0,0)
    # pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (int(car.x), int(car.y), int(car.x+cu[0]*1000), int(car.y+cu[1]*1000))))

    # Perpendicular
    # pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (int(mp[0]), int(mp[1]), int(xr), int(yr))))
    # pyglet.gl.glColor3f(0,1,0)

    pyglet.gl.glColor3f(1,1,1)

pyglet.clock.schedule_interval(on_update, 1/60.0)
pyglet.app.run()