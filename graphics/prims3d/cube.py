from sceneNode import SceneNode

from OpenGL.GL import *

class Cube(SceneNode):
    def onAttach(self):
        SceneNode.onAttach(self)

        self.defaultVar("center",True)
    
    def geom(self):
        if self.center:
            glTranslatef(-0.5,-0.5,-0.5)
        
        glBegin(GL_QUADS)

        #top
        glTexCoord2f(0,0)
        glVertex3f(1,1,0)
        glTexCoord2f(0,1)
        glVertex3f(0,1,0)
        glTexCoord2f(1,1)
        glVertex3f(0,1,1)
        glTexCoord2f(1,0)
        glVertex3f(1,1,1)
        
        #bottom
        glTexCoord2f(0,0)
        glVertex3f(1,0,1)
        glTexCoord2f(0,1)
        glVertex3f(0,0,1)
        glTexCoord2f(1,1)
        glVertex3f(0,0,0)
        glTexCoord2f(1,0)
        glVertex3f(1,0,0)
        
        #front
        glTexCoord2f(1,0)
        glVertex3f(1,1,1)
        glTexCoord2f(0,0)
        glVertex3f(0,1,1)
        glTexCoord2f(0,1)
        glVertex3f(0,0,1)
        glTexCoord2f(1,1)
        glVertex3f(1,0,1)
        
        #back
        glTexCoord2f(0,0)
        glVertex3f(1,0,0)
        glTexCoord2f(0,1)
        glVertex3f(0,0,0)
        glTexCoord2f(1,1)
        glVertex3f(0,1,0)
        glTexCoord2f(1,0)
        glVertex3f(1,1,0)
        
        #right
        glTexCoord2f(0,0)
        glVertex3f(0,1,1)
        glTexCoord2f(0,1)
        glVertex3f(0,1,0)
        glTexCoord2f(1,1)
        glVertex3f(0,0,0)
        glTexCoord2f(1,0)
        glVertex3f(0,0,1)
        
        #left
        glTexCoord2f(0,0)
        glVertex3f(1,1,0)
        glTexCoord2f(0,1)
        glVertex3f(1,1,1)
        glTexCoord2f(1,1)
        glVertex3f(1,0,1)
        glTexCoord2f(1,0)
        glVertex3f(1,0,0)
        
        glEnd()

        if self.center:
            glTranslatef(0.5,0.5,0.5)
