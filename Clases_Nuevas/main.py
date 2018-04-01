# -*- coding: utf-8 -*-

# Importar modulos
from director import Director
from phase import PhaseScene
from xmlLevelParser import getAllLevelFiles
from menu import Menu
from soundEffects import *


if __name__ == '__main__':

    # Class for soundEffects control
    soundEffects = SoundEffects()

    # Create the director
    director = Director(soundEffects)

    director.stackGame()
    # Execute the game
    director.execute()
