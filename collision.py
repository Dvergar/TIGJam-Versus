from math import sqrt, pow
# import psyco

class Collision(object):
    def __init__(self, points, car):
        self.points = points
        self.car = car
        self.mcarx = (self.car.topleft[0] + self.car.topright[0]) / 2
        self.mcary = (self.car.topleft[1] + self.car.topright[1]) / 2
        self.axe = (0,0)
        self.overlap = 9999999999999999999999
        self.happened = False

        if self.find_collision():
            self.happened = True


    def find_collision(self):
        for shape in self.points:
            for i in range(len(shape)):
                # Looping vertices
                if i != len(shape)-1:
                   if self.collide(shape[i], shape[i+1], (self.car.x,self.car.y), (self.car.oldx,self.car.oldy)):
                      return True
                # Closing shape case
                else:
                    if self.collide(shape[i], shape[0], (self.car.x,self.car.y), (self.car.oldx,self.car.oldy)):
                       return True


    def collide(self, A,B, C,D):
        self.cC, self.cD = C,D
        self.wA, self.wB = A,B

        # wall projected on car
        vAB = (B[0] - A[0], B[1] - A[1])
        axe = self.getAxe(vAB)
        pC, pD, pS, pCA, pDA = self.projpoints(A,B, C,D, vAB, axe) # CD on AB
        minCD = min([pC,pD])
        maxCD = max([pC,pD])
        if not minCD <= pS <= maxCD:
            return False
        else:
            cV = (self.cD[0]-self.cC[0], self.cD[1]-self.cC[1])
            vpj = self.project(cV, axe)
            self.buildMTV(vpj, axe)

        # car projected on wall
        vCD = (D[0] - C[0], D[1] - C[1])
        axe = self.getAxe(vCD)
        pA, pB, pS2,pCA, pDA = self.projpoints(C,D, A,B, vCD, axe)
        minAB = min([pA,pB])
        maxAB = max([pA,pB])
        if not minAB <= pS2 <= maxAB:
            return False
        else:
            cV = (self.cD[0]-self.cC[0], self.cD[1]-self.cC[1])
            vpj = self.project(cV, axe)
            self.buildMTV(vpj, axe)
        return True

    def projpoints(self, A,B, C,D, vAB, axeAB):
##        vAB = (B[0] - A[0], B[1] - A[1])
        vCA = (A[0] - C[0], A[1] - C[1])
        vDA = (A[0] - D[0], A[1] - D[1])


        pCA = self.project(vCA, axeAB)
        pDA = self.project(vDA, axeAB)
        pS  = self.project(vAB, axeAB)

        vpjCA = (axeAB[0]*pCA, axeAB[1]*pCA)
        vpjDA = (axeAB[0]*pDA, axeAB[1]*pDA)
        vpjS  = (axeAB[0]*pS , axeAB[1]*pS )

        pC = (A[0] + vpjCA[0], A[1] + vpjCA[1])
        pD = (A[0] + vpjDA[0], A[1] + vpjDA[1])
        pS = (A[0] + vpjS[0] , A[1] + vpjS[1] )

        return pC, pD, pS, pCA, pDA

    def response(self):
        # car
        cDC = (self.cC[0] - self.cD[0], self.cC[1] - self.cD[1])
        cN = self.getnorm(cDC)
        cV = self.getnormalizedvector(cDC, cN)

        # wall
        wAB = (self.wB[0] - self.wA[0], self.wB[1] - self.wA[1])
        wN = self.getnorm(wAB)
        wV = self.getnormalizedvector(wAB, wN)

        return self.responsevector(cV,wV)

    def getAxe(self, v):
        vlength = self.getnorm(v)
        try:
            axe = (-v[1]/vlength , v[0]/vlength)
        except ZeroDivisionError:
            axe = (0,0)
        return axe

    def project(self, u,v):
        return -(u[0]*v[0] + u[1]*v[1])

    def overlap(self, p1, p2):
        if p1 != 0 and p2 != 0:
            return True

    def getMTV(self):
        return self.axe[0]*self.overlap, self.axe[1]*self.overlap

    def buildMTV(self, p, axe):
##        print "p, axe", p,axe
        if p < self.overlap and p!=0:
            self.overlap = p
            self.axe = axe

    def d0(self, v1,v2):
        out = 0
        for k in range(len(v1)):
            out += v1[k] * v2[k]
        return out

    def getnorm(self, v):
        return sqrt(pow(v[0],2) + pow(v[1],2))

    def getnormalizedvector(self, v, N):
        try:
            return (v[0]/N , v[1]/N)
        except ZeroDivisionError:
            return (0,0)

    def responsevector(self, source,reflector):
        nu = (-reflector[1], reflector[0])
        msource = (source[0]*-1, source[1]*-1)
        Rx = source[0] + 2.* nu[0] * self.d0(msource, nu)
        Ry = source[1] + 2.* nu[1] * self.d0(msource, nu)
        return Rx, Ry

# psyco.bind(Collision)