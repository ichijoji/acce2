from sceneNode import SceneNode

from OpenGL.GL import *
from OpenGL.GLUT import *

class Text(SceneNode):
    def onAttach(self):
        SceneNode.onAttach(self)
        
        self.defaultVar("text","")
        self.defaultVar("align","left")
        
    def geom(self):
        w = sum([glutBitmapWidth(GLUT_BITMAP_HELVETICA_18,ord(c)) for c in self.text])
        self.log("w",w)
        if self.align == 'right':
            glRasterPos(-w,0,0)
        elif self.align == 'center':
            glRasterPos(-w/2.0,0,0)
        else:
            glRasterPos(0,0,0)
        for c in self.text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18,ord(c))
