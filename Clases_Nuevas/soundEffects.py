import pygame
import os

GLOBAL_VOLUME = 0.25

class SoundEffects:
    def __init__(self):
        # Initialize pygame music player
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
        pygame.mixer.init()

        # List with sounds, to adjust volume of each one
        self.soundList = []

        # Directory containing the sounds
        musicDirectory = "musicAndSounds"

        directory = os.path.join(musicDirectory, "sword_slash.ogg")
        self.swordSlashSound = pygame.mixer.Sound(directory)
        self.soundList.append(self.swordSlashSound)

        # Set default volume for every sound in the list
        for sound in self.soundList:
            sound.set_volume(GLOBAL_VOLUME)

    # Set volume for every sound on the list
    def setEffectsVolume(self, newVolume):
        for sound in self.soundList:
            sound.set_volume(newVolume)