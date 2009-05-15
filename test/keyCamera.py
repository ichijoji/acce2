from graphics.prims3d.camera import Camera
from core.vec3 import Vec3

import math

class KeyCamera(Camera):
    def onAttach(self):
        Camera.onAttach(self)

        self.defaultVar("yaw",0)
        self.defaultVar("height",0)
        self.defaultVar("dist",100)
        self.defaultVar("yawSpeed",1)
        self.defaultVar("heightSpeed",50)
        self.defaultVar("distSpeed",50)

        self.dyaw = 0
        self.dheight = 0
        self.ddist = 0

    def msg_keyDown(self, args):
        name = args['name']

        if name == 'left':
            self.dyaw = self.yawSpeed
        elif name == 'right':
            self.dyaw = -self.yawSpeed
        elif name == 'up':
            self.dheight = self.heightSpeed
        elif name == 'down':
            self.dheight = -self.heightSpeed
        elif name == 'pageup':
            self.ddist = -self.distSpeed
        elif name == 'pagedown':
            self.ddist = self.distSpeed

    def msg_keyUp(self, args):
        name = args['name']

        if name in ('left','right'):
            self.dyaw = 0
        elif name in ('up','down'):
            self.dheight = 0
        elif name in ('pageup','pagedown'):
            self.ddist = 0

    def msg_tick(self, args):
        dtime = args['dtime']

        self.yaw += self.dyaw * dtime
        self.height += self.dheight * dtime
        self.dist += self.ddist * dtime

        x = self.lookAt.x + self.dist * math.cos(self.yaw)
        y = self.lookAt.y + self.height
        z = self.lookAt.z + self.dist * math.sin(self.yaw)
        self.position = Vec3(x,y,z)
