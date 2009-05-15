from sceneNode import SceneNode

from OpenGL.GL import *
from OpenGL.GLUT import *

class Text(SceneNode):
    def onAttach(self):
        SceneNode.onAttach(self)
        
        self.defaultVar("text","")
        self.defaultVar("align","center")
        self.defaultVar("centerHeight",True)
        
    def geom(self):
        w = sum([glutBitmapWidth(GLUT_BITMAP_HELVETICA_18,ord(c)) for c in self.text])
        
        glPushMatrix()
        m = glGetFloatv(GL_MODELVIEW_MATRIX)
        glScalef(1.0/m[0][0],1.0/m[1][1],1)
        
        if self.centerHeight:
            h = -glutBitmapHeight(GLUT_BITMAP_HELVETICA_18)/2.0
        else:
            h = 0
        
        if self.align == 'right':
            glRasterPos(-w,h,0)
        elif self.align == 'center':
            glRasterPos(-w/2.0,h,0)
        else:
            glRasterPos(0,h,0)
            
        for c in self.text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18,ord(c))
            
        glPopMatrix()
