import threading
import time
from math import asin, degrees, atan, cos, radians, sin, sqrt
from cone import Cone
from model3d import *

class Antenna:

    def __init__(self):
        self.cone = Cone(10, 100)  # cone icin base ve height bilgisi
        self.obj = None

        self.elevation = 0
        self.azimuth = 0

        self.triX = 0  # azimuth hesabinda uçgenin x eksenindeki kenar uzunlugu (findAzimuth)
        self.triY = 0  # azimuth hesabinda ucgenin y eksenindeki kenar uzunlugu (findAzimuth)
        self.distanceAP = 0  # antenna plane arasindaki uzaklik

        self.coord = [0.0, 0.0, 1.5]


    def prepare(self):
        self.obj = MODEL3D("antenaParabolica.obj", swapyz=True, swapxz=False, scale=2, use_mtl=False)  # antenna objesi olusturuldu

    def rotateToPoint(self, x, y, z):

        self.triX = x - self.coord[0] #azimuth hesabi icin plane'in x koordinati degerinden azimuth'un x koordinati degeri cikarilir
        self.triY = y - self.coord[1] #azimuth hesabi icin plane'in y koordinati degerinden azimuth'un y koordinati degeri cikarilir

        if self.triX < 0: #arctan hesabında triX 0dan kucuk oldukca 90 ve 270 araliklarinde sorun cikmaktadir bunu engellemek icin 180 eklenir
            self.azimuth = degrees(atan(self.triY / self.triX)) + 180 # finding azimuth
        else: #triX'in pozitif oldugu yerlerde
            self.azimuth = degrees(atan(self.triY / self.triX))  # finding azimuth

        self.cone.azimuth = self.azimuth  # cone'un azimuth'u her seferinde antenna'nın azimuthuna esitlenir

        self.distanceAP = sqrt((x - self.coord[0]) ** 2 + (y - self.coord[1]) ** 2 + (z - self.coord[2]) ** 2) #antenna ve plane arasindaki uzaklik 3 boyutlu uzayda 2 nokta arasindaki uzakliktan yola cikilarak bulunur
        self.elevation = degrees(asin(z / self.distanceAP))  # finding elevation


        self.cone.elevation = self.elevation

        print("plane x:", x, "plane y:", y, "plane z:", z)
        #print(self.coord)
        print("azimuth:", self.azimuth)
        print("elevation:", self.elevation)
        #print("distanceAP:", self.distanceAP)
        print("")

    def draw(self):
        # glPushAttrib — push the server attribute stack
        glPushAttrib(GL_LINE_BIT | GL_TRANSFORM_BIT | GL_ENABLE_BIT | GL_LIGHTING_BIT | GL_CURRENT_BIT | GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)
        glPushMatrix()  # push the current matrix stack
        glLoadIdentity()  # replace the current matrix with the identity matrix
        glTranslatef(self.coord[0], self.coord[1], self.coord[2])  # antenna, xyz kadar translate edilir - multiply the current matrix by a translation matrix
        glColor3fv((0.996, 0.797, 0.398)) #antenna'nın rengi ayarlandi
        glRotatef(300, 0, 0, 1)  # antenna, z ekseni etrafinda dondurulur (daha iyi bir goruntusu olması icin) (olmasa da olur, gorsellik disinda bir onemi yok)
        # asagidaki glRotatef'lerde yazilan formulasyonlar ile antenna'nın hareketi ayarlandi
        glRotatef(self.elevation, sin(radians(self.elevation)), 0.0, 0.0)
        glRotatef(self.elevation, 0.0, cos(radians(self.elevation)), 0.0)
        glRotatef(self.azimuth, 0.0, 0.0, 1.0)  #antenna, azimuth kadar z ekseni etrafinda doner
        glCallList(self.obj.gl_list)  # execute a display list
        glPopMatrix()  # pop the current matrix stack
        glPopAttrib()
        glPushMatrix()
        self.cone.draw()  # cone objesini cizdir
        glPopMatrix() #pop the server attribute stack

