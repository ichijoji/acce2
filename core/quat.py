import math

from OpenGL.GL import *

class Quat:
    def __init__(self, w = 1, x = 0, y = 0, z = 0):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        axis, angle = self.toAxisAngle()
        return "<Quat %.3f %s>" % (angle, axis)

    @staticmethod
    def fromAxisAngle(axis, angle):
        axis = axis.norm()
        sina = math.sin(angle/2.0)
        cosa = math.cos(angle/2.0)
        return Quat(cosa, axis.x * sina, axis.y * sina, axis.z * sina)

    def toAxisAngle(self):
        q = self.norm()
        cosa = q.w
        angle = math.acos(cosa) * 2
        sina = math.sqrt(1.0 - cosa * cosa)
        if abs(sina) < 0.0001:
            sina = 1
        axis = Vec3(q.x / sina, q.y / sina, q.z / sina)
        return axis, angle

    def __mul__(self, q):
        if isinstance(q,Quat):
            return Quat(self.w * q.w - self.x * q.x - self.y * q.y - self.z * q.z,
                        self.w * q.x + self.x * q.w + self.y * q.z - self.z * q.y,
                        self.w * q.y + self.y * q.w + self.z * q.x - self.x * q.z,
                        self.w * q.z + self.z * q.w + self.x * q.y - self.y * q.x)
        
        elif isinstance(q,Vec3):
            result = self * Quat(0,q.x,q.y,q.z) * self.inverse()
            return Vec3(result.x,result.y,result.z)
        
        else:
            return Quat(self.w * q, self.x * q, self.y * q, self.z * q)

    def __div__(self, q):
        return Quat(self.w / q, self.x / q, self.y / q, self.z / q)

    def conjugate(self):
        return Quat(self.w,-self.x,-self.y,-self.z)

    def magnitude(self):
        return math.sqrt(self.w * self.w +
                         self.x * self.x +
                         self.y * self.y +
                         self.z * self.z)

    def norm(self):
        return self / self.magnitude()

    def inverse(self):
        return self.norm().conjugate()

    def rotate(self):
        axis, angle = self.toAxisAngle()
        glRotate(math.degrees(angle),axis.x,axis.y,axis.z)

from vec3 import Vec3

if __name__ == "__main__":
    x = Vec3(1,0,0)
    v = Vec3(0,10,5)
    q = x.rotationTo(v)
    r = q * x
    vn = v.norm()
    assert abs(r.x - vn.x) < 0.1 and abs(r.y - vn.y) < 0.1 and abs(r.z - vn.z) < 0.1
