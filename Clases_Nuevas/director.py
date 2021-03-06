# -*- encoding: utf-8 -*-

# Modules
import pygame, pyglet
import sys
from pygame.locals import *
from scene import *
from phase import PhaseScene
from xmlLevelParser import getAllLevelFiles
from menu import Menu

FPS = 60
LEVELS = "zealous_warrior_all_levels.xml"

class Director():

    def __init__(self, soundEffects):
        # Scene stack
        self.stack = []
        # Flag that indicates when to leave pygame scene
        self.leave_scene_pygame = False
        # Flag for music play and stop, here to ensure it stays across levels
        self.musicMuted = False
        # Sound effects class
        self.soundEffects = soundEffects

    def loopPygame(self, scene):

        # Take pygame clock
        clock = pygame.time.Clock()

        # Leave scene flag is false
        self.leave_scene_pygame = False

        # Erase all events prior to entering the loop
        pygame.event.clear()

        # The loop of the game, actions that will take place in each scene
        while not self.leave_scene_pygame:

            # Synchronize the game at 60 fps
            time_passed = clock.tick(FPS)

            # Hand on the events to the secene
            scene.events(pygame.event.get())

            # Update the scene
            scene.update(time_passed)

            # Draw in the screen
            scene.draw(scene.screen)
            pygame.display.flip()


    def execute(self):

        # Initialize pygame library (if it wasn't already)
        pygame.init()
        # Create pygame display (if it wasn't already)
        #self.screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))

        # While the stack contains scenes, we execute the top one
        while (len(self.stack) > 0):

            # We take the scene on the top of the stack to execute it
            scene = self.stack[len(self.stack) - 1]

            # If the scene is pygame's
            if isinstance(scene, PygameScene):

                # Execute the loop
                self.loopPygame(scene)
            else:
                raise Exception('Unrecogniced scene type')

        # Stop pygame library and close all windows
        pygame.quit()


    def stopScene(self):
        if (len(self.stack)>0):
            scene = self.stack[len(self.stack) - 1]
            # If the scene is pygame's
            if isinstance(scene, PygameScene):
                # We indicate with the flag we want to leave it
                self.leave_scene_pygame = True
            else:
                raise Exception('Unrecogniced scene type')

    def leaveScene(self):
        self.stopScene()
        # Erase scene on top of the stack (if there's any)
        if (len(self.stack)>0):
            self.stack.pop()

    def leaveProgram(self):
        self.stopScene()
        # Clear scene stack
        self.stack = []

    def changeScene(self, scene):
        self.stopScene()
        # Erase scene on top of the stack (if there's any)
        if (len(self.stack)>0):
            self.stack.pop()
        # Put argument scene on top of the stack
        self.stack.append(scene)

    def stackScene(self, scene):
        # Put argument scene on top of the stack (over the current one)
        self.stack.append(scene)

    def addPhase(self, levelFile):
        self.stopScene()
        self.stack.append(PhaseScene(self, levelFile, self.soundEffects))

    def stackGame(self):
        # Get level files from an xml
        levelFilesList = getAllLevelFiles(LEVELS)
        # Reverse the order of the levels (to put in the stack)
        levelFilesList.reverse()

        for level in levelFilesList:
            # Create the scene for the level
            scene = PhaseScene(self, level, self.soundEffects)
            # Put it on top of the stack
            self.stackScene(scene)

        # Loads the game menu in the director
        menu = Menu(self, 960, 540)
        self.stackScene(menu)