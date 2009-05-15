from core.object import Object
from core.vec2 import Vec2
from graphics.materialManager import materialManager
import math

from OpenGL.GL import *

class SceneNode(Object):
    genNode = None
    
    def onAttach(self):
        self.defaultVar("position",Vec2())
        self.defaultVar("scale",Vec2(1,1))
        self.defaultVar("rotation",0)
        self.defaultVar("material",{})
        self.defaultVar("static",True)
        self.list = None
    
    def msg_render2d(self, args):
        if args.get('picking'):
            glPushName(len(args['pickObjects']))
            args['pickObjects'].append(self)
        
        glPushMatrix()
        
        self.transform()
        
        if self.static and not SceneNode.genNode:
            if self.list:
                glCallList(self.list)
                return False
            else:
                self.list = glGenLists(1)
                glNewList(self.list,GL_COMPILE_AND_EXECUTE)
                SceneNode.genNode = self
            
        materialManager.bind(self.material)
        
        self.geom()
        
    def transform(self):
        self.position.translate()
        glRotatef(math.degrees(self.rotation),0,0,1)
        self.scale.scale()
        
    def geom(self):
        pass
        
    def unmsg_render2d(self, args):
        if not self.static or SceneNode.genNode:
            glPopMatrix()
            materialManager.unbind()
        if SceneNode.genNode == self:
            glEndList()
            SceneNode.genNode = None
        if args.get('picking'):
            glPopName()
