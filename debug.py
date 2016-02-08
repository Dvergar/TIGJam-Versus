#!/usr/bin/env python
import pyglet
from pyglet.gl import *
from pyglet.window import key
from math import sin, cos, pi
import random

class Camera(object):
    def __init__(self, pos, rot, speed=5):
        self.x, self.y, self.z = pos
        self.rx, self.ry, self.rz = rot
        self.speed = speed

    def apply(self):
        glLoadIdentity()
        glRotatef(self.rx, 1, 0, 0)
        glRotatef(self.ry, 0, 1, 0)
        glRotatef(self.rz, 0, 0, 1)
        glTranslatef(-self.x, -self.y, -self.z)

class Cube(object):
    TYPES = AIR, GRASS, DIRT, STONE, DEBUG = xrange(5)
    ALL_FACES = [
        # 0, 1, 2, 0, 2, 3, # Bottom
        # 0, 5, 1, 0, 4, 5, # Back
        # 0, 3, 4, 3, 7, 4, # Left
        # 3, 2, 7, 2, 6, 7, # Front
        # 1, 5, 2, 2, 5, 6, # Right
        # 4, 6, 5, 4, 7, 6, # Top
        0, 2, 1, 0, 3, 2, # Only-top (debug)
    ]

    def __init__(self, map_, x, y, z, type_):
        self.x = x
        self.y = y
        self.z = z
        self.map = map_
        self.vertices = (
            # x + 0., y + 0., z + 0.,
            # x + 1., y + 0., z + 0.,
            # x + 1., y + 0., z + 1.,
            # x + 0., y + 0., z + 1.,
            x + 0., y + 1., z + 0.,
            x + 1., y + 1., z + 0.,
            x + 1., y + 1., z + 1.,
            x + 0., y + 1., z + 1.,
        )
        self.set_type(type_)

    @property
    def indices(self):
        return Cube.ALL_FACES

    def set_type(self, type_):
        self.type = type_

        if self.type is Cube.GRASS:
            color = [0.0, 1.0, 0.0]
        elif self.type is Cube.DIRT:
            color = [0.7, 0.6, 0.1]
        elif self.type is Cube.AIR:
            color = [1.0, 1.0, 1.0]
        elif self.type is Cube.STONE:
            color = [0.6, 0.6, 0.6]
        elif self.type is Cube.DEBUG:
            color = [1.0, 0.0, 0.0]

        color[0] *= 0.1 * random.random() + 0.9
        color[1] *= 0.1 * random.random() + 0.9
        color[2] *= 0.1 * random.random() + 0.9
        self.colors = color * (len(self.vertices) / 3)

    def is_visible(self):
        if self.type is Cube.AIR:
            return False
        return self.map.type_at(self.x, self.y + 1, self.z) is Cube.AIR or \
               self.map.type_at(self.x, self.y - 1, self.z) is Cube.AIR or \
               self.map.type_at(self.x + 1, self.y, self.z) is Cube.AIR or \
               self.map.type_at(self.x - 1, self.y, self.z) is Cube.AIR or \
               self.map.type_at(self.x, self.y, self.z - 1) is Cube.AIR or \
               self.map.type_at(self.x, self.y, self.z + 1) is Cube.AIR

class Map(object):
    def __init__(self, width=16, height=128, depth=16):
        self.width = width
        self.height = height
        self.depth = depth
        self.cubes = []
        self.generate()

    def type_at(self, x, y, z):
        if x < 0 or y < 0 or z < 0:
            return Cube.AIR
        try:
            return self.cubes[x][y][z].type
        except IndexError:
            return Cube.AIR

    def generate(self):
        self.cubes = []
        for x in xrange(self.width):
            x_slice = []
            for y in xrange(self.height):
                y_slice = []
                for z in xrange(self.depth):
                    c_type = Cube.AIR
                    if y < 48:
                        c_type = Cube.STONE
                    elif 48 <= y < 64:
                        c_type = Cube.DIRT
                    elif y == 64:
                        c_type = Cube.GRASS
                    y_slice.append(Cube(self, x, y, z, c_type))
                x_slice.append(y_slice)
            self.cubes.append(x_slice)
        self._update_batch()

    def _update_batch(self):
        self.cubes_visible = 0
        self.cubes_culled = 0
        self.batch = pyglet.graphics.Batch()
        for x_slice in self.cubes:
            for y_slice in x_slice:
                for cube in y_slice:
                    self._add_cube_to_batch(cube)
        print str(self.cubes_visible * 12) + " tris in batch"
        print str(self.cubes_culled * 12) + " tris culled"

    def _add_cube_to_batch(self, cube):
        if cube.is_visible():
            self.cubes_visible += 1
            # XXX: Why are my vertex lists interfering with each other?
            self.batch.add_indexed(
                    len(cube.vertices) / 3,
                    GL_TRIANGLES,
                    None,
                    cube.indices,
                    ('v3f\static', cube.vertices),
                    ('c3f\static', cube.colors))
        else:
            self.cubes_culled += 1

    def draw(self):
        self.batch.draw()

# TODO: Move globals, bind window events in main()
window = pyglet.window.Window(resizable=True, caption="ShaftCraft", width=800, height=600)
window.set_exclusive_mouse(True)
camera = Camera((0, 66.8, 0), (0, 0, 0), speed=15)
world = Map()

keys = key.KeyStateHandler()
window.push_handlers(keys)

@window.event
def on_resize(width, height):
    if height == 0:
        height = 1
    glClearColor(0.0, 0.7, 0.9, 0)
    # glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / float(height), 0.1, 1000)
    glMatrixMode(GL_MODELVIEW)
    return pyglet.event.EVENT_HANDLED


@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    camera.apply()
    world.draw()


@window.event
def on_mouse_motion(x, y, dx, dy):
    camera.ry += dx / 8.0
    camera.rx -= dy / 8.0


def update(dt):
    if keys[key.W]:
        yrotrad = (camera.ry / 180 * pi)
        xrotrad = (camera.rx / 180 * pi)
        camera.x += float(sin(yrotrad)) * dt * camera.speed
        camera.z -= float(cos(yrotrad)) * dt * camera.speed
        camera.y -= float(sin(xrotrad)) * dt * camera.speed

    if keys[key.S]:
        yrotrad = (camera.ry / 180 * pi)
        xrotrad = (camera.rx / 180 * pi)
        camera.x -= float(sin(yrotrad)) * dt * camera.speed
        camera.z += float(cos(yrotrad)) * dt * camera.speed
        camera.y += float(sin(xrotrad)) * dt * camera.speed

    if keys[key.D]:
        yrotrad = (camera.ry / 180 * pi)
        camera.x += float(cos(yrotrad)) * dt * camera.speed
        camera.z += float(sin(yrotrad)) * dt * camera.speed

    if keys[key.A]:
        yrotrad = (camera.ry / 180 * pi)
        camera.x -= float(cos(yrotrad)) * dt * camera.speed
        camera.z -= float(sin(yrotrad)) * dt * camera.speed


def main():
    pyglet.clock.schedule_interval(update, 1/60.0)
    pyglet.app.run()


if __name__ == "__main__":
    main()