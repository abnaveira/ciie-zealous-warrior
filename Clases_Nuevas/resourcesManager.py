# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *


# -------------------------------------------------
# resourcesManager Class

#We implement an empty class, with only class methods
class ResourcesManager(object):
    resources = {}

    @classmethod
    def loadImage(cls, name, colorkey=None):
        # If the name of the file is amongst the already loaded resources
        if name in cls.resources:
            # That resource is returned
            return cls.resources[name]
        # If it hasn't been loaded previously
        else:
            # The image is loaded signaling the folder it is in
            fullname = os.path.join('images', name)
            try:
                image = pygame.image.load(fullname)
            except pygame.error, message:
                print 'Cannot load image:', fullname
                raise SystemExit, message
            image = image.convert()
            if colorkey is not None:
                if colorkey is -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, RLEACCEL)
            # It is stored
            cls.resources[name] = image
            # It is returned
            return image

    @classmethod
    def loadFileCoordinates(cls, name):
        # If the name of the file is amongst the already loaded resources
        if name in cls.resources:
            # That resource is returned
            return cls.resources[name]
        # If it hasn't been loaded previously
        else:
            # The resource is loaded signaling the folder it is in
            fullname = os.path.join('images', name)
            pfile = open(fullname, 'r')
            data = pfile.read()
            pfile.close()
            # It is stored
            cls.resources[name] = data
            # It is returned
            return data
