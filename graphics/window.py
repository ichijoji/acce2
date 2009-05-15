from core.object import Object
from core.optionServer import optionServer
from core import util

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Window(Object):
    def onAttach(self):
        self.initGraphics()
        self.initInput()
        
    def initInput(self):
        self.keyNames = {}
        self.keyMods = {}
        for name in dir(pygame):
            if name.startswith('K_'):
                self.keyNames[getattr(pygame,name)] = name[2:].lower()
            elif name.startswith('KMOD_'):
                self.keyMods[name[5:].lower()] = getattr(pygame,name)

        self.joystickCount = pygame.joystick.get_count()
        self.joysticks = []
        for i in range(self.joystickCount):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            self.joysticks.append(joystick)

        self.mouseButtonNames = {1:'left',2:'middle',3:'right'}

        self.inputFuncs = util.getFuncs(self,'input_')
        
    def initGraphics(self):
        self.fps = optionServer.get('fps',60)
        self.res = optionServer.get('res',(800,600))
        self.fullscreen = optionServer.get('fullscreen',False)
        
        pygame.init()
        glutInit(())
        flags = pygame.OPENGL | pygame.DOUBLEBUF | pygame.HWSURFACE
        if self.fullscreen:
            flags |= pygame.FULLSCREEN
            
        self.screen = pygame.display.set_mode(self.res,flags)
        pygame.display.set_caption("ACCE2")
        
        glEnable(GL_TEXTURE_2D)
        glShadeModel(GL_SMOOTH)
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
        glLineWidth(2)
        glClearColor(1,1,1,1)
        
        self.lastFrameTime = None
        self.frameTime = 1.0 / 60.0
        
    def onDetach(self):
        pygame.quit()
        
    def msg_tick(self, args):
        time = args['time']
        
        if not self.lastFrameTime: self.lastFrameTime = time
        
        if time - self.lastFrameTime > self.frameTime:
            self.lastFrameTime += self.frameTime
            
            glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)
            
            self.set3dProjection(False)
            self.publish("render3d",**args)
            self.set2dProjection(False)
            self.publish("render2d",**args)
            
            glFlush()
            pygame.display.flip()
            
        for event in pygame.event.get():
            eventName = pygame.event.event_name(event.type)
            eventName = eventName[0].lower() + eventName[1:]
            if eventName in self.inputFuncs:
                self.inputFuncs[eventName](event)
                
    def input_quit(self, event):
        self.publish('shutdownApp')

    def input_keyDown(self, event):
        if event.key == pygame.K_ESCAPE:
            self.publish('shutdownApp')
        else:
            name, mods = self.keyInfo(event)
            self.publish('keyDown', name = name, mods = mods, key = event.key)

    def input_keyUp(self, event):
        name, mods = self.keyInfo(event)
        self.publish('keyUp', name = name, mods = mods, key = event.key)

    def input_joyButtonDown(self, event):
        self.publish('joyButtonDown',joy = event.joy, button = event.button)

    def input_joyButtonUp(self, event):
        self.publish('joyButtonUp',joy = event.joy, button = event.button)

    def input_joyAxisMotion(self, event):
        self.publish('joyAxisMotion',joy = event.joy, value = event.value, axis = event.axis)

    def input_mouseButtonDown(self, event):
        buttonName, relPos = self.mouseInfo(event)
        self.publish('mouseButtonDown',button = event.button, pos = event.pos, relPos = relPos, buttonName = buttonName)
        self.doPicking(event,"Up")

    def input_mouseButtonUp(self, event):
        buttonName, relPos = self.mouseInfo(event)
        self.publish('mouseButtonUp', button = event.button, pos = event.pos, relPos = relPos, buttonName = buttonName)
        self.doPicking(event,"Down")

    def input_mouseMotion(self, event):
        relPos = self.relPos(event)
        buttonNames = [self.mouseButtonNames.get(i) for i in event.buttons]
        self.publish('mouseMotion', pos = event.pos, relPos = relPos, buttons = event.buttons, buttonNames = buttonNames)
        
    def keyInfo(self, event):
        name = self.keyNames.get(event.key)

        mods = []
        for modName, mod in self.keyMods.iteritems():
            if mod & event.mod:
                mods.append(modName)

        return name, mods

    def relPos(self, event):
        return (event.pos[0]/float(self.res[0]),event.pos[1]/float(self.res[1]))

    def mouseInfo(self, event):
        return self.mouseButtonNames.get(event.button), self.relPos(event)

    def doPicking(self, event, suffix):
        pickObjects = []
        
        def pickRender3d():
            self.set3dProjection(True)
            self.publish("render3d",picking = True, pickObjects = pickObjects)

        def pickRender2d():
            self.set2dProjection(True)
            self.publish("render2d",picking = True, pickObjects = pickObjects)
        
        from OpenGL import GL
        selectFunction = getattr(GL,"glSelectWithCallback",my_glSelectWithCallback)

        buf = list(selectFunction(event.pos[0],event.pos[1],pickRender2d,5,5))
        buf.extend(list(selectFunction(event.pos[0],event.pos[1],pickRender3d,5,5)))
        hits = [i[2][0] for i in buf]
        #self.log("pick",pickObjects,hits)
        if hits:
            buttonName, relPos = self.mouseInfo(event)
            for hit in hits:
                self.publish("objectClick" + suffix,object = pickObjects[hit],button = event.button, pos = event.pos, relPos = relPos, buttonName = buttonName)

    def set2dProjection(self, picking):
        if not picking:
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluOrtho2D(0,self.res[0],0,self.res[1])

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslate(0,self.res[1],0)
        glScalef(1,-1,1)

        glColor(1,1,1,1)
        glBindTexture(GL_TEXTURE_2D,0)

        #glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_NORMALIZE)

    def set3dProjection(self, picking):
        if not picking:
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(45,float(self.res[0])/float(self.res[1]),1,1000)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glColor(1,1,1,1)
        glBindTexture(GL_TEXTURE_2D,0)
        glBindTexture(GL_TEXTURE_3D,0)

        #glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)

def my_glSelectWithCallback(x, y, callback, xsize = 5, ysize = 5, buffer_size = 512):
    viewport = glGetIntegerv(GL_VIEWPORT)
    glSelectBuffer(buffer_size)
    glRenderMode(GL_SELECT)
    glInitNames()
    glMatrixMode(GL_PROJECTION)
    previousviewmatrix = glGetDoublev(GL_PROJECTION_MATRIX)
    glLoadIdentity()
    gluPickMatrix(x, viewport[3] - y, xsize, ysize, viewport)
    glMultMatrixd(previousviewmatrix)
    callback()
    glFlush()
    glMatrixMode(GL_PROJECTION)
    glLoadMatrixd(previousviewmatrix)
    return glRenderMode(GL_RENDER)
