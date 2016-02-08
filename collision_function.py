from math import sqrt, pow
import psyco




def collide(A,B, C,D):
    cC, cD = C,D
    wA, wB = A,B

    # wall projected on car
    vAB = (B[0] - A[0], B[1] - A[1])
    axe = getAxe(vAB)
    pC, pD, pS, pCA, pDA = projpoints(A,B, C,D, vAB, axe) # CD on AB
    minCD = min([pC,pD])
    maxCD = max([pC,pD])
    if not minCD <= pS <= maxCD:
        return False, (1,2,3,4)
##    else:
##        cV = (cD[0]-cC[0], cD[1]-cC[1])
##        vpj = project(cV, axe)
##        buildMTV(vpj, axe)

    # car projected on wall
    vCD = (D[0] - C[0], D[1] - C[1])
    axe = getAxe(vCD)
    pA, pB, pS2,pCA, pDA = projpoints(C,D, A,B, vCD, axe)
    minAB = min([pA,pB])
    maxAB = max([pA,pB])
    if not minAB <= pS2 <= maxAB:
        return False, (1,2,3,4)
##    else:
##        cV = (cD[0]-cC[0], cD[1]-cC[1])
##        vpj = project(cV, axe)
##        buildMTV(vpj, axe)

    return True, (cC, cD, wA, wB)

def projpoints(A,B, C,D, vAB, axeAB):
##        vAB = (B[0] - A[0], B[1] - A[1])
    vCA = (A[0] - C[0], A[1] - C[1])
    vDA = (A[0] - D[0], A[1] - D[1])


    pCA = project(vCA, axeAB)
    pDA = project(vDA, axeAB)
    pS  = project(vAB, axeAB)

    vpjCA = (axeAB[0]*pCA, axeAB[1]*pCA)
    vpjDA = (axeAB[0]*pDA, axeAB[1]*pDA)
    vpjS  = (axeAB[0]*pS , axeAB[1]*pS )

    pC = (A[0] + vpjCA[0], A[1] + vpjCA[1])
    pD = (A[0] + vpjDA[0], A[1] + vpjDA[1])
    pS = (A[0] + vpjS[0] , A[1] + vpjS[1] )

    return pC, pD, pS, pCA, pDA

def response():
    # car
    cDC = (cC[0] - cD[0], cC[1] - cD[1])
    cN = getnorm(cDC)
    cV = getnormalizedvector(cDC, cN)

    # wall
    wAB = (wB[0] - wA[0], wB[1] - wA[1])
    wN = getnorm(wAB)
    wV = getnormalizedvector(wAB, wN)

    return responsevector(cV,wV)

def getAxe(v):
    vlength = getnorm(v)
    try:
        axe = (-v[1]/vlength , v[0]/vlength)
    except ZeroDivisionError:
        axe = (0,0)
    return axe

def project(u,v):
    return -(u[0]*v[0] + u[1]*v[1])

def overlap(p1, p2):
    if p1 != 0 and p2 != 0:
        return True

def getMTV():
    return axe[0]*overlap, axe[1]*overlap

def buildMTV(p, axe):
##        print "p, axe", p,axe
    if p < overlap and p!=0:
        overlap = p
        axe = axe

def d0(v1,v2):
    out = 0
    for k in range(len(v1)):
        out += v1[k] * v2[k]
    return out

def getnorm(v):
    return sqrt(pow(v[0],2) + pow(v[1],2))

def getnormalizedvector(self, v, N):
    try:
        return (v[0]/N , v[1]/N)
    except ZeroDivisionError:
        return (0,0)

def responsevector(source,reflector):
    nu = (-reflector[1], reflector[0])
    msource = (source[0]*-1, source[1]*-1)
    Rx = source[0] + 2.* nu[0] * d0(msource, nu)
    Ry = source[1] + 2.* nu[1] * d0(msource, nu)
    return Rx, Ry



def Collision(points, car):
    axe = (0,0)
    overlap = 9999999999999999999999
##        vcar = (car.oldx - car.x, car.oldy - car.y)
##        axecar = getAxe(vcar)

    for shape in points:
        for i in range(len(shape)):
            # Looping vertices
            if i != len(shape)-1:
                collision, colpoints = collide(shape[i], shape[i+1], (car.x,car.y), (car.oldx,car.oldy))
                if collision:
##                    cV = (cD[0]-cC[0], cD[1]-cC[1])
##                    vpj = project(cV, axe)
##                    buildMTV(vpj, axe)
                    return True, colpoints
            # Closing shape case
            else:
                collision, colpoints = collide(shape[i], shape[0], (car.x,car.y), (car.oldx,car.oldy))
                if collision:
                   return True, colpoints

    return False, (1,2,3,4)

psyco.bind(Collision)