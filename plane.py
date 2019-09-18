import threading
import time
from math import cos
from math import radians
from math import sin

from model3d import *


class Plane():
    def __init__(self):
        self.coord = [0, 0, 30] #plane'in baslangic koordinatlari
        self.x = threading.Thread(target=self.threadFunction)
        self.isAlive = True #thread'in bitip bitmediginin kontrolu icin
        self.obj = None
        self.m = 10

        self.radius = 70 #plane'in donecegi cemberin yaricapi
        self.angle = 0  # plane'in baslangictaki acisi
        self.centerX = 0 #plane'in donecegi cemberin merkez noktasinin x koordinati
        self.centerY = 0 #plane'in donecegi cemberin merkez noktasinin y koordinati

    def start(self):
        self.x.start() #thread baslatilir

    def stop(self):
        self.isAlive = False #thread sona erer

    def threadFunction(self):
        while self.isAlive:
            self.followCircle() #circle cizmesini istedigim icin followCircle fonksiyonu cagrilir

    def prepare(self):
        self.obj = MODEL3D("ANKA.obj", reversex=True, reversey=True, scale=0.0005) #plane objesi olusturuldu (ANKA icin)

    def followLine(self):
        for x in range(10):  # plane'in duz bir cizgide hareketi icin for dongusu
            self.coord = [self.coord[0] + self.m, self.coord[1], self.coord[2]] #bir line boyunca ilerlemesini istedigim icin x ekseninde m kadar hareket sagladim
            time.sleep(1)

    def followCircle(self):
        self.angle += 5  # plane, circle icinde her seferinde 5 birimlik aci artisi ile doner
        self.coord[0] = cos(radians(self.angle)) * self.radius + self.centerX  # plane'in belli bir radius uzaklikta cizilecegi yeni noktanin x koordinati(cembersel donusteki)
        self.coord[1] = sin(radians(self.angle)) * self.radius + self.centerY  # plane'in belli bir radius uzaklikta cizilecegi yeni noktanin y koordinati(cembersel donusteki)
        time.sleep(1)

    def draw(self):
        # glPushAttrib — push the server attribute stack
        glPushAttrib(GL_LINE_BIT | GL_TRANSFORM_BIT | GL_ENABLE_BIT | GL_LIGHTING_BIT | GL_CURRENT_BIT | GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)
        glPushMatrix() #push the current matrix stack
        glLoadIdentity() #replace the current matrix with the identity matrix
        glTranslatef(self.coord[0], self.coord[1], self.coord[2]) #plane, xyz koordinatlarina translate edilir
        glRotatef(self.angle, 0, 0, 1) #angle degeri kadar z ekseni etrafinda donus gerceklesir
        glCallList(self.obj.gl_list) #execute a display list
        glPopMatrix() #pop the current matrix stack
        glPopAttrib() #pop the server attribute stack
