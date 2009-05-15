from sceneNode import SceneNode
from OpenGL.GLU import *
from core.vec3 import Vec3

class Camera(SceneNode):
    def onAttach(self):
        self.defaultVar("static",False)
        self.defaultVar("position",Vec3(0,0,100))
        self.defaultVar("lookAt",Vec3())
        self.defaultVar("up",Vec3(0,1,0))
        SceneNode.onAttach(self)

    def transform(self):
        p = self.position
        l = self.lookAt
        u = self.up
        gluLookAt(p.x,p.y,p.z,l.x,l.y,l.z,u.x,u.y,u.z)
