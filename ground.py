from OpenGL.GL import *

class Ground:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.vertices = (

            (-width, -height, 0),
            ( width, -height, 0),
            ( width,  height, 0),
            (-width,  height, 0)
        )

    def draw(self):
        #glPushAttrib — push the server attribute stack
        glPushAttrib(GL_LINE_BIT | GL_TRANSFORM_BIT | GL_ENABLE_BIT | GL_LIGHTING_BIT | GL_CURRENT_BIT | GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)
        glPushMatrix() #push the current matrix stack
        glLoadIdentity() #replace the current matrix with the identity matrix
        glColor3fv((0.95, 0.95, 0.95)) #grey
        glBegin(GL_QUADS) #delimit the vertices of a primitive or a group of like primitives
        for self.vertex in self.vertices:
            glVertex3fv(self.vertex) #glVertex3fv allows you to define where the vertex is in space
        glEnd() #delimit the vertices of a primitive or a group of like primitives
        glPopMatrix() #pop the current matrix
        glPopAttrib() #pop the server attribute stack
