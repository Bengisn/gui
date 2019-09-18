import pygame
from OpenGL.GL import *

class MODEL3D:
    def __init__(self, filename, swapyz=False, swapxz=False, swapxy=False, reversex=False, reversey=False, reversez=False, scale = 1, use_mtl=True):
        """Loads a Wavefront OBJ file"""
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []

        material = None

        glPushMatrix() # push the current matrix stack
        for line in open(filename, "r"):
            if line.startswith('#'): continue #yorum satirlarini gormezden gel
            values = line.split() #The split() method splits a string into a list.
            if not values:
                continue #eger yorum satiri degil ise
            if values[0] == 'v':
                v = [float(i) * scale for i in values[1:4]]
                if swapxy:
                    v = v[1], v[0], v[2]
                if swapxz:
                    v = v[2], v[1], v[0]
                if swapyz:
                    v = v[0], v[2], v[1]
                if reversex:
                    v= -v[0], v[1], v[2]
                if reversey:
                    v = v[0], -v[1], v[2]
                if reversez:
                    v = v[0], v[1], -v[2]

                self.vertices.append(v)

            elif values[0] == 'vn':
                v = [float(i) for i in values[1:4]]
                if swapxy:
                    v = v[1], v[0], v[2]
                if swapxz:
                    v = v[2], v[1], v[0]
                if swapyz:
                    v = v[0], v[2], v[1]
                if reversex:
                    v= -v[0], v[1], v[2]
                if reversey:
                    v = v[0], -v[1], v[2]
                if reversez:
                    v = v[0], v[1], -v[2]
                self.normals.append(v)

            elif values[0] == 'vt':
                self.texcoords.append(list(map(float, values[1:3])))
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'mtllib':
                if use_mtl:
                 self.mtl = self.MTL(values[1])
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append((face, norms, texcoords, material))

        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)
        for face in self.faces:
            vertices, normals, texture_coords, material = face
            if use_mtl: #eger mtl dosyasi varsa
                mtl = self.mtl[material]
                if 'texture_Kd' in mtl:
                    # use diffuse texmap
                    glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
                else:
                    # just use diffuse color
                    glColor(*mtl['Kd'])

            glBegin(GL_POLYGON)
            for i in range(len(vertices)):
                if normals[i] > 0:
                    glNormal3fv(self.normals[normals[i] - 1]) #set the current normal vector
                if texture_coords[i] > 0:
                    glTexCoord2fv(self.texcoords[texture_coords[i] - 1]) #set the current texture coordinates
                glVertex3fv(self.vertices[vertices[i] - 1]) #specifies a vertex
            glEnd() #delimit the vertices of a primitive or a group of like primitives
        glDisable(GL_TEXTURE_2D) #enable or disable server-side GL capabilities
        #GL_TEXTURE_2D - If enabled and no fragment shader is active, two-dimensional texturing is performed (unless three-dimensional or cube-mapped texturing is also enabled)
        glEndList() #create or replace a display list
        glPopMatrix() #pop the current matrix stack

    @staticmethod
    def MTL(filename):
        contents = {}
        mtl = None
        for line in open(filename, "r"):
            if line.startswith('#'):
                continue
            values = line.split()
            if not values: continue
            if values[0] == 'newmtl':
                mtl = contents[values[1]] = {}
            elif mtl is None:
                raise ValueError("mtl file doesn't start with newt1 stmt")
            elif values[0] == 'map_Kd':
                # load the texture referred to by this declaration
                mtl[values[0]] = values[1]
                surf = pygame.image.load(mtl['map_Kd'])
                image = pygame.image.tostring(surf, 'RGBA', 1)   #SOR
                ix, iy = surf.get_rect().size
                texid = mtl['texture_Kd'] = glGenTextures(1)
                glBindTexture(GL_TEXTURE_2D, texid)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
            else:
                mtl[values[0]] = list(map(float, values[1:]))
        return contents
