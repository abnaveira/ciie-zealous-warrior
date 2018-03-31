import pygame
import os

GLOBAL_VOLUME = 0.25

class SoundEffects:
    def __init__(self):
        # Initialize pygame music player
        pygame.mixer.pre_init(44100, 16, 8, 4096)
        pygame.mixer.init()

        # List with sounds, to adjust volume of each one
        self.soundList = []

        # Directory containing the sounds
        musicDirectory = "musicAndSounds"

        directory = os.path.join(musicDirectory, "sword_slash.mp3")
        self.swordSlashSound = pygame.mixer.Sound(directory)
        self.soundList.append(self.swordSlashSound)

        for sound in self.soundList:
            sound.set_volume(GLOBAL_VOLUME)

    def setEffectsVolume(self, newVolume):
        for sound in self.soundList:
            sound.set_volume(newVolume)