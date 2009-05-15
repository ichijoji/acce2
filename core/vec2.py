import math
from OpenGL.GL import *

class Vec2:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return "<Vec2 %.3f %.3f>" % (self.x,self.y)
        
    def __add__(self, v):
        return Vec2(self.x + v.x, self.y + v.y)
        
    def __sub__(self, v):
        return Vec2(self.y - v.y, self.y - v.y)
        
    def __mul__(self, v):
        if isinstance(v,Vec2):
            return Vec2(self.x * v.x, self.y * v.y)
        else:
            return Vec2(self.x * v, self.y * v)
            
    def __div__(self, v):
        if isinstance(v,Vec2):
            return Vec2(self.x / v.x, self.y / v.y)
        else:
            return Vec2(self.x / v, self.y / v)
            
    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)
        
    def angle(self):
        return math.atan2(self.y,self.x)
        
    def norm(self):
        return self / self.length()
        
    def dot(self, v):
        return self.x * v.x + self.y * v.y
        
    def lerp(self, v, i):
        return self + (v - self) * i
        
    def translate(self):
        glTranslatef(self.x,self.y,0)
        
    def scale(self):
        glScalef(self.x,self.y,1)
        
    def vertex(self):
        glVertex2f(self.x,self.y)
        
    def texCoord(self):
        glTexCoord2f(self.x,self.y)
