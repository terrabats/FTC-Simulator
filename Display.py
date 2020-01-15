import Nodes as nodes
import pygame
import math

width = 700 # screen
height = 700 # screen

#Display init
pygame.init()
gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption('FTC')
clock = pygame.time.Clock()
time = 0
done = False

#Font/Image init
comic = pygame.font.SysFont('Comic Sans MS', 30)
comicS = pygame.font.SysFont('Comic Sans MS', 15)
field = pygame.image.load('C:/Users/visha/Pictures/field.png').convert()
field = pygame.transform.scale(field, (width, height))

#Starting positions (inches)
startx = 12*11.25
starty = 12*9
starth = -90

#Robot Dimensions
robotWidth = 18
robotHeight = 18

#Simulation Update Speed (mills)
speedUp = 1 # keep < 5

#Velocitys of Robot
maxForVel = 30 #inch/s
maxStaVel = 20 #inch/s
maxTurVel = 90 #deg/s

#Robot Classes
rc = nodes.RobotConstraints(startx,starty,starth,robotWidth,robotHeight,maxForVel,maxStaVel,maxTurVel)
rp = nodes.RobotPos(rc)
pygame.mixer.music.load('zing.wav')
path = nodes.Path(rc, 0.5, pygame)

#Track
track = []

#Path Constraints

path.addPose(-10,0,0)
path.addPose(-22, -3, 45)
path.addPose(-4, 4, 0)
# path.addPose(20,20,45)
# path.addPose(-10,60,90)
# path.addPose(-4,0,0)x



#Drawing Classes
def drawRobot():
    c = rp.getCorners()
    for i in range(3):
        pygame.draw.line(gameDisplay,(0,0,0),c[i],c[i+1],3)
    pygame.draw.line(gameDisplay, (0, 0, 0), c[3], c[0], 3)
    v = rp.getVect()
    pygame.draw.line(gameDisplay,(204,102,0),(v[0],v[1]),(v[2],v[3]),3)
    track.append((rp.inchToPix(rp.x),rp.inchToPix(rp.y)))
def drawTimer():
    ts = comic.render(str(getTime()), False, (0, 0, 0))
    pygame.draw.rect(gameDisplay,(204,204,255),(10,8,100,50))
    pygame.draw.rect(gameDisplay,(51,0,102),(10,8,100,50),5)
    gameDisplay.blit(ts, (15, 10))
def drawPathTimes():
    if len(path.times) != 0:
        pygame.draw.rect(gameDisplay, (255,255,200), (10, 70, 80, 25*len(path.times)+10))
        pygame.draw.rect(gameDisplay, (199, 184, 133), (10, 70, 80, 25*len(path.times)+10), 5)
    i = 0
    for t in path.times:
        i+=1
        pt = comicS.render(str(i)+':  '+str(t), False, (255, 0, 0))
        gameDisplay.blit(pt, (15, 25*i+50))
def drawTrack():
    for (x,y) in track:
        pygame.draw.circle(gameDisplay, (0, 102, 0), (x, y), 1)
def drawPath():
    for (x,y,h) in path.getAllPoses():
        px = rp.inchToPix(x)
        py = rp.inchToPix(y)
        v = nodes.Vec2d(0,30)
        rv = v.getRotatedVec(-h)
        pygame.draw.line(gameDisplay,(255,255,200),(px,py),(px+rv.x,py-rv.y),3)
        pygame.draw.circle(gameDisplay, (100, 255, 0), (px, py), 3)

#Time
def getTime():
    return (math.trunc(time/10)/100)*speedUp

#Robot moving by path
def updateRobotPos():
    pows = path.update(rp.getPose(), getTime())
    rp.move(pows[0],pows[1],pows[2])

#Updating the display
def updateDisplay():
    gameDisplay.blit(field, (0, 0))
    drawRobot()
    drawTrack()
    drawTimer()
    drawPath()
    drawPathTimes()
    if(getTime() > 1):
        updateRobotPos()

#Main Display Loop
while not done:
    updateDisplay()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    pygame.display.update()
    clock.tick(100*speedUp)
    time = pygame.time.get_ticks()
