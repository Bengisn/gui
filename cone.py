from OpenGL.GL import *
from OpenGL.GLUT import *
from math import sin
from math import cos
from math import radians


class Cone:

    def __init__(self, base, height):

        self.base = base
        self.height = height
        self.slices = 10
        self.stacks = 8

        self.coord = [0, 0, 0.5] #baslangic koordinatlari

        self.elevation = 0 #glutWireCone'un cizilme durumunda dolayı 90 derece elevation uygulamak gerekiyor ki cone ters donsun
        self.azimuth = 0


        self.centerX = self.coord[0]
        self.centerY = self.coord[1]

    def draw(self):
        # glPushAttrib — push the server attribute stack
        glPushAttrib(GL_LINE_BIT | GL_TRANSFORM_BIT | GL_ENABLE_BIT | GL_LIGHTING_BIT | GL_CURRENT_BIT | GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)
        glPushMatrix() #push the current matrix stack
        glLoadIdentity() #replace the current matrix with the identity matrix
        glTranslatef(self.coord[0], self.coord[1], self.coord[2]) #cone, xyz'ye tasinir - multiply the current matrix by a translation matrix
        #glColor3f(0.6, 0.4, 0.4) #cone'un rengi ayarlandi
        #glColor3f(0.996, 0.797, 0.598)  # cone'un rengi ayarlandi
        glColor3f(1,  0.797, 0.699)
        #asagida yapilan islemler cone'un hareketi icin yazilmistir
        glRotatef(90-self.elevation, -sin(radians(self.azimuth)), cos(radians(self.azimuth)), 0.0)
        #self.ilk()
        #glRotatef(self.elevation2, -sin(radians(self.azimuth)), -cos(radians(self.azimuth)), 0.0)
        print("cone azimuth", self.azimuth)
        print("cone elevation", self.elevation)
        glRotatef(180, -sin(radians(self.azimuth)), cos(radians(self.azimuth)), 0) #cone'u ters cevirmek icin yazilmistir
        glTranslatef(0, 0, -self.height) #cone -self.heigth kadar mesafeye tasinmistir - multiply the current matrix by a translation matrix
        #If the matrix mode is either GL_MODELVIEW or GL_PROJECTION all objects drawn after glScale is called are scaled
        glutWireCone(self.base, self.height, self.slices, self.stacks) #render a wireframe cone
        glPopMatrix() #pop the current matrix stack
        glPopAttrib() #pop the server attribute stack
