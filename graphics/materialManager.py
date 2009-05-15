from core.fileServer import fileServer
from core import util

import pygame

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class MaterialManager:
    def __init__(self):
        self.textures = {}
        
        self.bindFuncs = util.getFuncs(self,"bind_")
        
    def loadTexture(self, filename):
        texture = pygame.image.load(fileServer.getFile(filename))
        w,h = texture.get_size()
        textureData = pygame.image.tostring(texture,"RGBA",0)
        textureId = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D,textureId)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_REPEAT)
        try:
            gluBuild2DMipmaps(GL_TEXTURE_2D,GL_RGBA,w,h,GL_RGBA,GL_UNSIGNED_BYTE,textureData)
        except OpenGL.error.NullFunctionError: 
            glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,w,h,0,GL_RGBA,GL_UNSIGNED_BYTE,textureData)
        glBindTexture(GL_TEXTURE_2D,0)
        return textureId
        
    def bindTexture(self, filename):
        if filename not in self.textures:
            self.textures[filename] = self.loadTexture(filename)
        glBindTexture(GL_TEXTURE_2D,self.textures[filename])
        
    def bind(self, args):
        glMatrixMode(GL_TEXTURE)
        glLoadIdentity()
        glPushAttrib(GL_CURRENT_BIT | GL_LIGHTING_BIT)
        for key, val in args.iteritems():
            assert key in self.bindFuncs
            self.bindFuncs[key](val)
        glMatrixMode(GL_MODELVIEW)

    def unbind(self):
        glPopAttrib()

    def bind_texture(self, filename):
        self.bindTexture(filename)

    def bind_color(self, c):
        glColor(*c)

    def bind_ambient(self, c):
        glMaterialfv(GL_FRONT_AND_BACK,GL_AMBIENT,c)

    def bind_diffuse(self, c):
        glMaterialfv(GL_FRONT_AND_BACK,GL_DIFFUSE,c)

    def bind_specular(self, c):
        glMaterialfv(GL_FRONT_AND_BACK,GL_SPECULAR,c)

    def bind_emission(self, c):
        glMaterialfv(GL_FRONT_AND_BACK,GL_EMISSION,c)

    def bind_shininess(self, f):
        glMaterialf(GL_FRONT_AND_BACK,GL_SHININESS,f)

    def bind_scale(self, v):
        v.scale()

materialManager = MaterialManager()
