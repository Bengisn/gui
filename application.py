from math import cos
from math import radians
from math import sin

from OpenGL.GLU import *
from OpenGL.GLUT import *
from pygame.locals import *

from antenna import Antenna
from ground import Ground
from model3d import *
from plane import Plane
from sidebar import SideBar


class Application:

    def __init__(self):

        self.display = (1000, 800)  # window'un boyutlari
        self.mouseX = 0  # mouse hareketinin x koordinati
        self.mouseY = 0  # mouse hareketinin y koordinati
        self.flag = False
        self.flag2 = False
        self.currentValue = 0
        self.antenna = Antenna()
        self.plane = Plane()
        self.ground = Ground(100, 100)  # ground'un boyutlari
        self.sidebar = SideBar()

    def resetCamera(self):
        glMatrixMode(GL_PROJECTION)  # characteristics of camera such as clip planes, field of view, projection method
        glLoadIdentity()  # replace the current matrix with the identity matrix
        width, height = self.display  # display'in degerleri width ve height'a atandi
        gluPerspective(90.0, width / float(height), 1, 200.0)  # set up a perspective projection matrix
        glTranslatef(0.0, 0.0, -5)  # multiply the current matrix by a translation matrix
        glEnable(GL_DEPTH_TEST)  # enable server-side GL capabilities
        glMatrixMode(GL_MODELVIEW)  # model matrix defines the frame’s position of the primitives you are going to draw
        # ModelView is the matrix that represents your camera(position, pointing and up vector.)
        # The reason for two separate matrices, instead of one, is that lighting is applied after the modelview view matrix
        # (i.e. on eye coordinates) and before the projection matrix. Otherwise, the matrices could be combined.

    def start(self):
        glutInit(sys.argv)  # used to initialize the GLUT library
        pygame.init()  # initialize all imported pygame modules
        self.screen = pygame.display.set_mode(self.display, OPENGL | DOUBLEBUF | OPENGLBLIT)  # initialize a window or screen for display

        glLightfv(GL_LIGHT0, GL_POSITION, (-40, 200, 100, 0.0))  # set light source parameters
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))  # set light source parameters
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))  # set light source parameters
        glEnable(GL_LIGHT0)  # enable server-side GL capabilities
        glEnable(GL_LIGHTING)  # enable server-side GL capabilities
        glEnable(GL_COLOR_MATERIAL)  # enable server-side GL capabilities
        glEnable(GL_DEPTH_TEST)  # enable server-side GL capabilities
        glShadeModel(GL_SMOOTH)  # most obj files expect to be smooth-shaded

        self.resetCamera()
        self.antenna.prepare()  # antenna objesi olusturuldu
        self.plane.prepare()  # plane objesi olusturuldu
        self.loop()

    def check(self):
        glMatrixMode(GL_PROJECTION)  # kamera ayarlarını sıfırla

        for event in pygame.event.get():  # pygame.event.get = (get events from the queue)
            if event.type == pygame.QUIT:
                self.plane.stop()  # plane objesi icin thread sona erer
                pygame.quit()  # uninitialize all pygame modules
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:  # eger mouse'a basili ise
                if event.button == 4:  # forward
                    glScaled(1.05, 1.05, 1.05)  # zoom-in
                elif event.button == 5:  # backward
                    glScaled(0.95, 0.95, 0.95)  # zoom-out

            if pygame.key.get_pressed()[K_LCTRL] and pygame.mouse.get_pressed()[0]:  # object rotation (CTRL ve mouse'un sol butonuna basilmis ise)
                if self.flag == True:  # ilk basistaki hareketi engellemek icin
                    self.mouseX, self.mouseY = pygame.mouse.get_rel()  # get the amount of mouse movement
                    glRotatef(self.mouseX / 5, 0.0, 0.0, 1.0)
                    glRotatef(self.mouseY / 5, cos(radians(self.currentValue)), abs(sin(radians(self.currentValue))),
                              0.0)
                    self.currentValue += self.mouseX / 5
                elif self.flag == False:
                    pygame.mouse.get_rel()  # get the amount of mouse movement
                    self.flag = True
            else:
                self.flag = False

            if pygame.key.get_pressed()[K_LCTRL] and pygame.mouse.get_pressed()[
                2]:  # camera rotation (CTRL ve mouse'un sag kligine basilmis ise)
                if self.flag2 == True:  # ilk basistaki hareketi engellemek icin
                    self.mouseX, self.mouseY = pygame.mouse.get_rel()  # get the amount of mouse movement
                    glTranslatef(-self.mouseX / 25, self.mouseY / 25, 0.0)
                elif self.flag2 == False:
                    pygame.mouse.get_rel()  # get the amount of mouse movement
                    self.flag2 = True
            else:
                self.flag2 = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:  # eger klavyeye basilmissa ve basilan harf r ise
                self.currentValue = 0
                self.resetCamera()
        glMatrixMode(
            GL_MODELVIEW)  # model çizmek için matrisi sıfırla. Applies subsequent matrix operations to the modelview matrix stack.

    def loop(self):
        self.plane.start()  # plane objesi icin thread baslatilir
        self.sidebar.setFunc(self.antenna, self.plane)

        while True:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear buffers to preset values

            self.antenna.rotateToPoint(self.plane.coord[0], self.plane.coord[1], self.plane.coord[2])
            self.check()  # mouse ve klavye kontrolleri icin
            self.ground.draw()  # ground objesini cizdir
            self.antenna.draw()  # antenna objesini cizdir
            self.plane.draw()  # plane objesini cizdir
            self.sidebar.draw() #sidebar objesini cizdir

            pygame.display.flip()  # update the full display surface to the screen
            pygame.time.wait(10)  # pause the program for an amount of time
