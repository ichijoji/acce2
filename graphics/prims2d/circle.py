from sceneNode import SceneNode

from OpenGL.GL import *
import math

class Circle(SceneNode):
    def onAttach(self):
        SceneNode.onAttach(self)
        self.defaultVar("filled",True)
        self.defaultVar("slices",20)
        self.defaultVar("center",True)
    
    def geom(self):
        if not self.center:
            glTranslatef(0.5,0.5,0)
        
        if self.filled:
            glBegin(GL_TRIANGLE_FAN)
            glTexCoord2f(0.5,0.5)
            glVertex2f(0,0)
        else:
            glBegin(GL_LINE_LOOP)
        
        for i in range(self.slices+1):
            th = float(i)/float(self.slices)*math.pi*2
            x = math.cos(th)
            y = math.sin(th)
            glTexCoord2f((x+1)/2,(y+1)/2)
            glVertex2f(x,y)
        glEnd()

        if not self.center:
            glTranslatef(-0.5,-0.5,0)
