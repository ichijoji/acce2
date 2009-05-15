from sceneNode import SceneNode

from OpenGL.GL import *

class Rect(SceneNode):
    def onAttach(self):
        SceneNode.onAttach(self)
        
        self.defaultVar("filled",True)
        self.defaultVar("center",True)
    
    def geom(self):
        if self.center:
            glTranslatef(-0.5,-0.5,0)
        if self.filled:
            glBegin(GL_QUADS)
        else:
            glBegin(GL_LINE_LOOP)
        glTexCoord2f(0,0)
        glVertex2f(0,0)
        glTexCoord2f(0,1)
        glVertex2f(0,1)
        glTexCoord2f(1,1)
        glVertex2f(1,1)
        glTexCoord2f(1,0)
        glVertex2f(1,0)
        glEnd()
        if self.center:
            glTranslatef(0.5,0.5,0)
