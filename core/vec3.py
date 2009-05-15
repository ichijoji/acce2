import math

from OpenGL.GL import *

class Vec3:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "<Vec3 %.3f %.3f %.3f>" % (self.x,self.y,self.z)

    def __add__(self, v):
        assert isinstance(v,Vec3)
        return Vec3(self.x + v.x, self.y + v.y, self.z + v.z)

    def __sub__(self, v):
        assert isinstance(v,Vec3)
        return Vec3(self.x - v.x, self.y - v.y, self.z - v.z)

    def __mul__(self, v):
        if isinstance(v,Vec3):
            return Vec3(self.x * v.x,self.y * v.y,self.z * v.z)
        else:
            return Vec3(self.x * v, self.y * v, self.z * v)

    def __div__(self, v):
        if isinstance(v,Vec3):
            return Vec3(self.x / v.x,self.y / v.y,self.z / v.z)
        else:
            return Vec3(self.x / v, self.y / v, self.z / v)

    def __neg__(self):
        return Vec3(-self.x,-self.y,-self.z)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def norm(self):
        return self / self.length()

    def dot(self, v):
        return self.x * v.x + self.y * v.y + self.z * v.z

    def project(self, v):
        l = self.length()
        return self * (self.dot(v) / (l * l))

    def cross(self, v):
        return Vec3(self.y * v.z - self.z * v.y,
                    self.z * v.x - self.x * v.z,
                    self.x * v.y - self.y * v.x)

    def rotationTo(self, v):
        d = self.dot(v)
        if d > 0.99:
            return Quat()
        elif d < -0.99:
            return Quat.fromAxisAngle(self.makePerp(),math.pi)
        else:
            return Quat.fromAxisAngle(self.cross(v).norm(),
                                    math.acos(self.norm().dot(v.norm())))

    def makePerp(self):
        if self.dot(Vec3.UNIT_Y) < 0.8:
            return self.cross(Vec3.UNIT_Y)
        else:
            return self.cross(Vec3.UNIT_Z)

    def lerp(self, v, l):
        return self + (v - self) * l

    def toTuple(self):
        return (self.x,self.y,self.z)
        
    def translate(self):
        glTranslatef(self.x,self.y,self.z)
        
    def scale(self):
        glScalef(self.x,self.y,self.z)
        
    def vertex(self):
        glVertex3f(self.x,self.y,self.z)

Vec3.UNIT_X = Vec3(1,0,0)
Vec3.UNIT_Y = Vec3(0,1,0)
Vec3.UNIT_Z = Vec3(0,0,1)
Vec3.ZERO = Vec3(0,0,0)

from quat import Quat
