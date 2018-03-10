# -*- coding: utf-8 -*-

from scene import PygameScene

#---------------------------
#---------Constants---------
#---------------------------

# -------------------------------------------------
# Class for pygame scenes with one player

class PhaseScene(PygameScene):

    def __init__(self, director):
        PygameScene.__init__(self, director)

