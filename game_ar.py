# import psyco
from math import cos,sin, radians, fabs, sqrt, pow
from random import randint, choice
import cProfile
import time
import sys
import os

import pyglet
from pyglet.window import key

import pyar
import math
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
# psyco.bind(rotate2d)


class Sprite(pyglet.sprite.Sprite):
    def __init__(self, img, x, y, thebatch):
        pyglet.sprite.Sprite.__init__(self, img, x, y, batch=thebatch)

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

    def overlap(self, other):
        if self.right <= other.left:
            return False
        if other.right <= self.left:
            return False
        if self.top <= other.bottom:
            return False
        if other.top <= self.bottom:
            return False
        return True

def decrease(value, rate):
    if value > 0:
        value -= rate
    if value < 0:
        value += rate
    return value


class Lifebar:
    WIDTH = 20
    HEIGHT = 480
    def __init__(self, game, player, color, side):
        print "lifebar"
        self.game = game
        self.player = player
        self.y = 0
        self.hp = self.HEIGHT
        self.ratio = self.HEIGHT / 100.
        print self.ratio
        if color == "red":
            self.color = (0.65, 0.14, 0.14)
        elif color == "blue":
            self.color = (0.14, 0.30, 0.62)

        if side == "left":
            self.x = 0
            self.xtext = self.x + self.WIDTH + 30
        elif side == "right":
            self.x = self.game.window.width - self.WIDTH
            self.xtext = self.x - 30

        self.label = pyglet.text.Label("null",
                          font_size=20,
                          batch=self.game.mybatch,
                          anchor_x="center",
                          color=(0, 0, 0, 100),
                          x=self.xtext,
                          y=self.game.window.height - 30)


    def on_update(self, dt):
        self.hp = self.player.hp * self.ratio
        self.label.text = str(self.player.lives)

    def on_draw(self):
        pyglet.gl.glColor3f(*self.color)
        pyglet.gl.glRectf(self.x, self.y, self.x+self.WIDTH, self.y+self.hp)
        pyglet.gl.glColor3f(1, 1, 1)


class Explosion(pyglet.sprite.Sprite):
    _registry = []
    img = pyglet.image.load('assets/explosion3.png')
    def __init__(self, game, x,y):
        self._registry.append(self)
        self.game = game
        pyglet.sprite.Sprite.__init__(self, self.img)
        self.explosion_seq = pyglet.image.ImageGrid(self.img, 1, 16)

        self.image = self.explosion_seq[0]
        self.image.anchor_x = self.image.width // 2
        self.image.anchor_y = self.image.height // 2

        self.scale = 1 * self.game.kscale

        self.i = 0
        self.x,self.y = x,y
        self.chktime = time.time()

    def on_update(self,dt):
        if time.time() - self.chktime > 0.05:
            self.i +=1
            if self.i < len(self.explosion_seq):
                self.image = self.explosion_seq[self.i]
                self.image.anchor_x = self.image.width // 2
                self.image.anchor_y = self.image.height // 2
                self.scale = 1 * self.game.kscale
                self.chktime = time.time()
            else:
                self._registry.remove(self)


class Rocket(Sprite):
    _registry = []
    img = pyglet.resource.image('assets/rocket.png')
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2
    def __init__(self, game, owner, carrot, carx,cary):
        self._registry.append(self)
        print "rocket !"
        self.game = game
        Sprite.__init__(self, self.img, carx, cary, self.game.mybatch)
        self.scale = 1.2 * self.game.kscale
        self.rotation = carrot
        self.owner = owner

    def close(self):
        for shape in self.game.points:
            for point in shape:
                x_dist = point[0] - self.x
                y_dist = point[1] - self.y

                if x_dist < 0:
                    x_dist *= -1

                if y_dist < 0:
                    y_dist *= -1

                distance = x_dist + y_dist
                if distance < 100:
                    return True

    def explode(self):
        Explosion(self.game, self.x, self.y)

    def on_update(self, dt):
        self.oldx, self.oldy = self.x, self.y
        self.x += sin(radians(self.rotation))*10
        self.y += cos(radians(self.rotation))*10

        if not 0 < self.x < self.game.window.width or not 0 < self.y < self.game.window.height:
            self._registry.remove(self)
        else:
            # Obstacle collision
            if self.close():
                wallcollision = collision.Collision(self.game.points, self)

                if wallcollision.happened:
                        self.explode()
                        self._registry.remove(self)

            # Car collision
            for car in Car._registry:
                if self.owner != car:
                    if car.intersect(self.x, self.y):
                        self.explode()
                        car.update_hp(-self.owner.dmg)
                        self._registry.remove(self)

# psyco.bind(Rocket)

class Car(Sprite):
    _registry = []
    glowimg = pyglet.image.load('assets/glow.png')
    glowimg.anchor_x = glowimg.width // 2
    glowimg.anchor_y = glowimg.height // 2
    def __init__(self, game, player, img, x, y, left, up, right, down, fire):
        print "popcar"

        self.game = game
        self._registry.append(self)
        self.game.window.push_handlers(self)

        self.img = pyglet.resource.image(img)
        self.img.anchor_x = self.img.width // 2
        self.img.anchor_y = self.img.height // 2
        Sprite.__init__(self, self.img, x, y, self.game.mybatch)

        self.glowsprite = pyglet.sprite.Sprite(self.glowimg, self.x, self.y)
        self.glowsprite.opacity = 0

        self.l = left
        self.u = up
        self.r = right
        self.d = down
        self.fire = fire
        self.player = player

        self.bonusdmg = 1
        self.hp = 100
        self.lives = 10

        # pymike? physics
        self.angle = 0
        self.nose = 0
        self.force = 0
        self.velocity = [0,0]
        self.friction = 0.05
        self.accel = 0.1

        self.rockettime = time.time()

    def on_key_press(self, symbol, modifiers):
        if time.time() - self.rockettime > 0.1:
            self.rockettime = time.time()
            if symbol == self.fire:
                Rocket(self.game, self, self.rotation, self.x,self.y)

    def reset(self):
        self.hp = 100
        self.lives = 10
        self.die()

    def x2(self):
        print "start x2"
        if self.bonusdmg > 1:
            pyglet.clock.unschedule(self.stop_x2)
        self.bonusdmg = 2
        self.glowsprite.opacity = 255
        pyglet.clock.schedule_once(self.stop_x2, 10)

    def stop_x2(self, dt):
        print "stop x2"
        self.glowsprite.opacity = 0
        self.bonusdmg = 1

    def update_hp(self, dhp):
        self.hp = self.hp + dhp
        if self.hp <= 0:
            self.lives -= 1
            self.hp = 100
            self.die()
        if self.hp > 100:
            self.hp = 100
        if self.lives <= 0:
            self.game.over(self.player)

    def die(self):
        self.x = self.y = 4242424242
        pyglet.clock.schedule_once(self.repop, 3)

    def repop(self, dt):
        self.x,self.y = choice(self.game.lastpop)
        self.game.pop[self.player] = True

    def on_draw(self):
        if self.bonusdmg > 1:
            self.glowsprite.x, self.glowsprite.y = self.x, self.y
            self.glowsprite.scale = self.scale
            self.glowsprite.rotation = self.rotation
            self.glowsprite.draw()

    def on_update(self, dt):
        self.oldx, self.oldy = self.x, self.y

        self.dmg = 10 * self.bonusdmg
        self.scale = 0.5 * self.game.kscale

        if self.game.keys[self.l]:
            self.nose -= (self.force)/1.5
        if self.game.keys[self.r]:
            self.nose += (self.force)/1.5
        if self.game.keys[self.d]:
            self.force -= 0.2
            if self.force < -2:
                self.force = -2
            pass
        if self.game.keys[self.u]:
            self.force += self.accel
            if self.force > 6:
                self.force = 6
        else:
            self.force = decrease(self.force, self.accel)
            self.velocity[0] = decrease(self.velocity[0], self.accel)
            self.velocity[1] = decrease(self.velocity[1], self.accel)

        self.velocity[0] = +math.sin(math.radians(self.nose))*self.force
        self.velocity[1] = +math.cos(math.radians(self.nose))*self.force

        # Moving
        self.rotation = self.nose
        self.x += self.velocity[0]
        self.y += self.velocity[1]

        # Obstacle collision
        wallcollision = collision.Collision(self.game.points, self)
        if wallcollision.happened:
            responsevec = wallcollision.response()
            mtv = wallcollision.getMTV()
            self.x = self.x - mtv[0] + responsevec[0]
            self.y = self.y - mtv[1] + responsevec[1]
            self.force = decrease(self.force, self.accel*2)

            # If response collides as well...
            wallcollision2 = collision.Collision(self.game.points, self)
            if wallcollision2.happened:
                self.x = self.oldx
                self.y = self.oldy

        # Bonus collision
        for bonus in Bonus._registry:
            if self.overlap(bonus):
                bonus.do(self)


class Bonus(Sprite):
    _registry = []
    imglist = {}
    imglist['hp'] = pyglet.image.load('assets/health.png')
    imglist['x2'] = pyglet.image.load('assets/x2.png')

    def __init__(self, game, type, x,y):
        self._registry.append(self)
        self.game = game
        self.type = type
        Sprite.__init__(self, self.imglist[type], x,y, self.game.mybatch)

    def detach(self):
        self._registry.remove(self)

    def do(self, car):
        print "do"
        if self.type == 'hp':
            car.update_hp(+8)
        if self.type == 'x2':
            car.x2()
        self.detach()

    def on_update(self, dt):
        newopacity = self.opacity - 0.5
        if newopacity < 0:
            self.detach()
        else:
            self.opacity = newopacity


class Mousetext(pyglet.text.Label):
    def __init__(self, game, dx, txt):
        self.game = game
        pyglet.text.Label.__init__(self, "Click "+txt+" to join !",
                                  font_size=10,
                                  anchor_x="center",
                                  color=(45, 36, 33, 255),
                                  x=dx,
                                  y=20)



class Game:
    def __init__(self):
        self.window = pyglet.window.Window(640, 480)
        self.window.push_handlers(self)
        self.keys = key.KeyStateHandler()
        self.window.push_handlers(self.keys)
        self.mybatch = pyglet.graphics.Batch()

        self.gaming = False
        self.gameover = False
        self.debug_collision = False
        self.kscale = 0.5
        self.pop = [False, False]
        self.lastpop = []
        self.shapedetector = None # Prevent error when quitting on menu

        self.gameoverlabel = pyglet.text.Label("GAMEOVER",
                          font_size=20,
                          anchor_x="left",
                          color=(239, 214, 193, 100),
                          x=100,
                          y=200)

        self.menu = pyglet.image.load('assets/menu.png')

        self.helpleft = Mousetext(self, 100, "mouse left")
        self.firstlefthelp = True
        self.helpright = Mousetext(self, self.window.width - 100, "mouse right")
        self.firstrighthelp = True

        pyglet.clock.schedule_interval(self.update, 1/60.0)

    def popbonus(self, dt):
        x = randint(0, self.window.width)
        y = randint(0, self.window.height)
        bonus = choice(('hp','x2'))
        Bonus(self, bonus, x,y)

    def dostart(self, type):
        self.shapedetector = pyar.ShapeDetector(self.window.width, self.window.height)
        if type == "pic":
            self.shapedetector.setcapturetype(type, 'assets/map.png')
        else:
            self.shapedetector.setcapturetype(type)
        self.getpoints("dummy")
        pyglet.clock.schedule_interval(self.getpoints, 1/1.0)
        pyglet.clock.schedule_interval(self.popbonus, 8.0)

    def over(self, dead):
        self.gameover = True
        self.dead = dead + 1
        if self.dead == 1:
            self.deadmsg = "Blue"
        else:
            self.deadmsg = "Red"
        self.gameoverlabel.text = self.deadmsg+" player wins ! (ENTER to restart)"

        for car in Car._registry:
            car.reset()

        for bonus in Bonus._registry:
            bonus.detach()

    def getpoints(self, dt):
        self.points, self.bgimg = self.shapedetector.get_points()
        self.bg = pyglet.image.ImageData(640, 480, self.bgimg.mode, self.bgimg.tobytes())

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            pyglet.app.exit()

        if symbol == key.PAUSE:
            if self.debug_collision:
                self.debug_collision = False
            else:
                self.debug_collision = True

        if self.gaming:
            if symbol == key.NUM_SUBTRACT:
                self.kscale -= 0.1
            if symbol == key.NUM_ADD:
                self.kscale += 0.1
        else:
            if symbol == key.W:
                self.gaming = True
                self.dostart("cam")
            if symbol == key.P:
                self.gaming = True
                self.dostart("pic")

        if self.gameover:
            if symbol == key.ENTER:
                self.gameover = False

##        if symbol == key.U:
##            self.over(1)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.gaming:
            if button == 1:
                self.lastpop.append((x,y))
                if not self.pop[0]:
                    self.car = Car(self, 0, 'assets/car2.png', x,y, key.LEFT, key.UP, key.RIGHT, key.DOWN, key.P)
                    self.lifebar = Lifebar(self, self.car, "red", "left")
                    self.pop[0] = True
                    self.firstlefthelp = False
                else:
                    print "plop"
                    self.car.x, self.car.y = x,y

            if button == 4:
                self.lastpop.append((x,y))
                if not self.pop[1]:
                    self.car2 = Car(self, 1, 'assets/car3.png', x,y, key.F, key.T, key.H, key.G, key.W)
                    self.lifebar2 = Lifebar(self, self.car2, "blue", "right")
                    self.pop[1] = True
                    self.firstrighthelp = False
                else:
                    print "plop2"
                    self.car2.x, self.car2.y = x,y


    def on_draw(self):
        self.window.clear()
        if self.gaming:
            self.bg.blit(0,0)

            if self.pop[0]:
                self.lifebar.on_draw()
            if self.pop[1]:
                self.lifebar2.on_draw()

            for car in Car._registry:
                car.on_draw()

            if self.firstlefthelp:
                self.helpleft.draw()
            if self.firstrighthelp:
                self.helpright.draw()
        else:
            self.menu.blit(0,0)

        self.mybatch.draw()
        for explosion in Explosion._registry:
            explosion.draw()

        for bonus in Bonus._registry:
            bonus.draw()

        if self.debug_collision:
            pyglet.gl.glColor3f(1,0,0)
            for shape in self.points:
                pyglet.gl.glRectf(shape[0][0], shape[0][1], shape[0][0]+5,shape[0][1]+5)
                for i, point in enumerate(shape):
                    pyglet.gl.glRectf(shape[i][0], shape[i][1], shape[i][0]+5,shape[i][1]+5)
##                    if i != len(shape)-1:
##                        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (shape[i][0], shape[i][1], shape[i+1][0], shape[i+1][1])))
##                    else:
##                        # Closing path
##                        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (shape[i][0], shape[i][1], shape[0][0], shape[0][1])))
            fps_display.draw()


        if self.gameover:
            pyglet.gl.glColor3f(0.10, 0.08, 0.05)
            pyglet.gl.glRectf(0, 0, 640,480)
            self.gameoverlabel.draw()
        pyglet.gl.glColor3f(1,1,1)


    def update(self, dt):
        if self.pop[0]:
            self.car.on_update(dt)
            self.lifebar.on_update(dt)
        if self.pop[1]:
            self.car2.on_update(dt)
            self.lifebar2.on_update(dt)

        for rocket in Rocket._registry:
            rocket.on_update(dt)

        for explosion in Explosion._registry:
            explosion.on_update(dt)

        for bonus in Bonus._registry:
            bonus.on_update(dt)

        if self.window.has_exit and self.shapedetector != None:
            self.shapedetector.release()


game = Game()
##cProfile.run('Game()', 'fooprof')
fps_display = pyglet.clock.ClockDisplay()
pyglet.app.run()

