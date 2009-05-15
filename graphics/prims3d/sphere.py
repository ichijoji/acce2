from sceneNode import SceneNode

from OpenGL.GL import *
from OpenGL.GLU import *

class Sphere(SceneNode):
    def onAttach(self):
        SceneNode.onAttach(self)

        self.defaultVar("radius",1)
        self.defaultVar("stacks",20)
        self.defaultVar("slices",20)

        self.sphere = gluNewQuadric()
        gluQuadricTexture(self.sphere,GL_TRUE)
        gluQuadricOrientation(self.sphere,GLU_OUTSIDE)
    
    def geom(self):
        gluSphere(self.sphere,self.radius,self.slices,self.stacks)
