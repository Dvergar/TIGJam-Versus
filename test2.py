import pyglet
from pyglet.window import key
from math import cos, sin, sqrt, pow

def getAxe(v):
    vlength = sqrt( pow(v[0],2) + pow(v[1],2) )
    return (-v[1]/vlength , v[0]/vlength)

def project(u,v):
    return -(u[0]*v[0] + u[1]*v[1])

def overlap(p1, p2):
    print p1,p2
    if p1 != 0 and p2 != 0:
        return True

def projpoints(A,B, C,D):
    vAB = (B[0] - A[0], B[1] - A[1])
    vCA = (A[0] - C[0], A[1] - C[1])
    vDA = (A[0] - D[0], A[1] - D[1])
    axeAB = getAxe(vAB)

    pCA = project(vCA, axeAB)
    pDA = project(vDA, axeAB)
    pS  = project(vAB, axeAB)

    vpjCA = (axeAB[0]*pCA, axeAB[1]*pCA)
    vpjDA = (axeAB[0]*pDA, axeAB[1]*pDA)
    vpjS  = (axeAB[0]*pS , axeAB[1]*pS )

    pC = (A[0] + vpjCA[0], A[1] + vpjCA[1])
    pD = (A[0] + vpjDA[0], A[1] + vpjDA[1])
    pS = (A[0] + vpjS[0] , A[1] + vpjS[1] )

    return pC, pD, pS, axeAB, vpjCA


A, B = [100,100], [200,200]
C, D = [450,243], [120,230]

pA = (0,0)
pB = (0,0)
pC = (0,0)
pD = (0,0)
pS = (0,0)
pS2 = (0,0)
axe = (0,0)
axe2 = (0,0)
vpjCA = (0,0)


def collide():
    global pA,pB, pC,pD, pS, axe, vpjCA, pS2,axe2

    pC, pD, pS, axe, vpjCA = projpoints(A,B, C,D) # CD on AB
    minCD = min([pC,pD])
    maxCD = max([pC,pD])
    if not minCD < pS < maxCD:
        return False

    pA, pB, pS2, axe2, nimp = projpoints(C,D, A,B) # CD on AB
    minAB = min([pA,pB])
    maxAB = max([pA,pB])
    if not minAB < pS2 < maxAB:
        return False

    return True



################ PYGLET ################

window = pyglet.window.Window()
keys = key.KeyStateHandler()
window.push_handlers(keys)

i = 0
def on_update(dt):
    global C, D, i
    if keys[key.UP]:
        C[1] += 10
        D[1] += 10
    if keys[key.DOWN]:
        C[1] -= 10
        D[1] -= 10
    if keys[key.LEFT]:
        C[0] -= 10
        D[0] -= 10
    if keys[key.RIGHT]:
        C[0] += 10
        D[0] += 10

    if collide():
        i += 1
        print "collision",i


@window.event
def on_draw():
    window.clear()
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (A[0], A[1], B[0], B[1] )))
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (C[0], C[1], D[0], D[1] )))

    pyglet.gl.glColor3f(1,0,0)
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (A[0], A[1], A[0]+int(axe[0]*100), A[1]+int(axe[1]*100) )))
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (C[0], C[1], C[0]+int(axe2[0]*100), C[1]+int(axe2[1]*100) )))
    pyglet.gl.glColor3f(0,1,0)
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (A[0], A[1], A[0]+int(vpjCA[0]*100), A[1]+int(vpjCA[1]*100) )))
    pyglet.gl.glColor3f(1,1,1)

    pyglet.gl.glRectf(pA[0], pA[1], pA[0]+5, pA[1]+5)
    pyglet.gl.glRectf(pB[0], pB[1], pB[0]+5, pB[1]+5)
    pyglet.gl.glRectf(pS2[0], pS2[1], pS2[0]+5, pS2[1]+5)

    pyglet.gl.glRectf(pS[0], pS[1], pS[0]+5, pS[1]+5)
    pyglet.gl.glRectf(pC[0], pC[1], pC[0]+5, pC[1]+5)
    pyglet.gl.glRectf(pD[0], pD[1], pD[0]+5, pD[1]+5)

    # RESET
    pyglet.gl.glColor3f(1,1,1)

pyglet.clock.schedule_interval(on_update, 1/60.0)
pyglet.app.run()
