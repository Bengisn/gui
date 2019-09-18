import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class SideBar():

    def __init__(self):
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 128)
        self.black = (1, 1, 1)

    def setFunc(self,  antenna, plane):
        self.antenna1 = antenna
        self.plane1 = plane

    def drawText(self, text, x, y):
        font = pygame.font.Font(None, 25)
        textSurface = font.render(text, True, self.white, self.black)
        textData = pygame.image.tostring(textSurface, "RGBA", True)  # transfer image to string buffer
        glRasterPos2d(x, y)  # specifies the raster position for pixel operations.
        glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)  # write a block of pixels to the frame buffer

    def draw(self):

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 800, 0, 600)  # defines a 2-D orthographic projection matrix.
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        self.drawText("antenna azimuth: {0:.2f}".format(self.antenna1.azimuth), 0, 570)
        self.drawText("antenna elevation: {0:.2f}".format(self.antenna1.elevation), 0, 555)
        self.drawText("x coord of plane: {0:.2f}".format(self.plane1.coord[0]), 0, 540)
        self.drawText("y coord of plane: {0:.2f}".format(self.plane1.coord[1]), 0, 525)
        self.drawText("z coord of plane: {0:.2f}".format(self.plane1.coord[2]), 0, 510)
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

