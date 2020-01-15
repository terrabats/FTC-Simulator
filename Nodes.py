import math

class Vec2d(object):
    def __init__(self, x1, y1):
        self.x = x1
        self.y = y1
        self.theta = math.atan2(self.y,self.x)
    def getPos(self):
        return (self.x,self.y)
    def getTheta(self):
        return self.theta
    def getRotatedVec(self, deg):
        ang = self.theta + math.radians(deg)
        radius = math.sqrt(self.x*self.x + self.y*self.y)
        return Vec2d(math.cos(ang)*radius, math.sin(ang)*radius)

class RobotPos(object):
    def __init__(self, rc):
        self.x = rc.sx
        self.y = rc.sy
        self.h = rc.sh
        self.wi = rc.wi
        self.he = rc.he
        self.rm = RobotMovement(rc)
    def inchToPix(self, inches):
        return int(inches * (700 / 144))
    def pixToInch(self, pixels):
        return pixels * (144 / 700)
    def getCorners(self):
        self.rm.update()
        pos = self.rm.getPos()
        self.x = pos[0]
        self.y = pos[1]
        self.h = pos[2]
        c = []
        x = self.inchToPix(self.x)
        y = self.inchToPix(self.y)
        width2 = self.inchToPix(self.wi/2)
        height2 = self.inchToPix(self.he/2)
        cv = Vec2d(width2,height2)
        for i in range(4):
            rcv = cv.getRotatedVec((90*i)+self.h)
            c.append((x - rcv.x,y - rcv.y))
        return c
    def getVect(self):
        pos = self.rm.getPos()
        x = self.inchToPix(self.x)
        y = self.inchToPix(self.y)
        height2 = self.inchToPix(self.he/2)
        cv = Vec2d(0,height2)
        rcv = cv.getRotatedVec(self.h)
        v = [x,y,x - rcv.x,y - rcv.y]
        return v
    def getPose(self):
        return (self.x,self.y,self.h)
    def move(self, fp, sp, tp):
        self.rm.move(fp,sp,tp)

class RobotConstraints():
    def __init__(self, sx, sy, sh, wi, he , fv, sv, tv):
        self.sx = sx
        self.sy = sy
        self.sh = sh
        self.wi = wi
        self.he = he
        self.fv = fv
        self.sv = sv
        self.tv = tv


class RobotMovement(object):
    def __init__(self, rc):
        self.x = rc.sx
        self.y = rc.sy
        self.h = rc.sh
        self.fv = rc.fv/91
        self.sv = rc.sv/91
        self.tv = rc.tv/91
        self.fp = 0
        self.sp = 0
        self.tp = 0
    def move(self, fp, sp, tp):
        self.fp = fp
        self.sp = sp
        self.tp = tp
    def update(self):
        out = []
        theta = math.radians(self.h)
        self.x += math.sin(theta)*self.fp*self.fv + math.cos(theta)*self.sp*self.sv
        self.y -= math.cos(theta)*self.fp*self.fv - math.sin(theta)*self.sp*self.sv
        self.h += self.tp*self.tv
    def getPos(self):
        return [self.x,self.y,self.h]
    def inchToPix(self, inches):
        return int(inches * (700 / 144))

class Path(object):
    def __init__(self,rc, ac, py):
        self.sx = rc.sx
        self.sy = rc.sy
        self.sh = rc.sh
        self.poses = [(self.sx,self.sy,self.sh)]
        self.times = []
        self.count = 1
        self.acc = ac
        self.xe = 0
        self.ye = 0
        self.he = 0
        self.py = py
    def update(self, curentPose, currentTime):
        if self.count < len(self.poses):
            self.xe = curentPose[0] - self.poses[self.count][0]
            self.ye = curentPose[1] - self.poses[self.count][1]
            self.he = curentPose[2] - self.poses[self.count][2]
            self.isEnd(currentTime)
            return self.calcVels(curentPose)
        else:
            return (0,0,0)

    def calcVels(self, currentPose):
        out = [0,0,0]
        targetTheta = math.atan2(self.ye,self.xe)
        robotTheta = math.radians(currentPose[2])
        out[1] = -math.cos(targetTheta-robotTheta)
        out[0] = math.sin(targetTheta-robotTheta)
        out[2] = -self.sigNum(self.he)
        return out
    def isEnd(self, time):
        if math.fabs(self.xe) < self.acc and math.fabs(self.ye) < self.acc and math.fabs(self.he) < self.acc:
            self.count += 1
            self.times.append(time)
            self.py.mixer.music.play()

    def addPose(self, x, y, h):
        self.poses.append((self.poses[-1][0]+x,self.poses[-1][1]-y,self.poses[-1][2]+h))
    def getAllPoses(self):
        return self.poses
    def sigNum(self, input):
        if input > 0:
            return 1.0
        elif input < 0:
            return -1.0
        else:
            return 0.0








