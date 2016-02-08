import pyglet

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



window = pyglet.window.Window()
img = pyglet.image.load('rocket.png')
biatch = pyglet.graphics.Batch()

class Rocket(Sprite):
    img = pyglet.resource.image('rocket.png')
    def __init__(self):
        print "rocket !"
        Sprite.__init__(self, self.img, 100, 100, biatch)

rocket = Rocket()

@window.event
def on_draw():
    window.clear()
    biatch.draw()

pyglet.app.run()