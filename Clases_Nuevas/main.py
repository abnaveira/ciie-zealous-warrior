# -*- coding: utf-8 -*-

# Importar modulos
from director import Director
from phase import PhaseScene
from xmlLevelParser import getAllLevelFiles
from menu import *


if __name__ == '__main__':

    # Create the director
    director = Director()

    # Get level files from an xml
    levelFilesList = getAllLevelFiles("zealous_warrior_all_levels.xml")
    # Reverse the order of the levels (to put in the stack)
    levelFilesList.reverse()

    # Initialize pygame music player
    #pygame.mixer.pre_init(44100, 16, 2, 4096)
    #pygame.mixer.init()
    # TODO: use this with sounds of characters and enemies, not used for music

    for level in levelFilesList:
        # Create the scene for the level
        scene = PhaseScene(director, level)
        # Put it on top of the stack
        director.stackScene(scene)

    # Loads the game menu in the director
    menu = Menu(director, 800, 600)#960, 540)
    director.stackScene(menu)

    # Execute the game
    director.execute()
