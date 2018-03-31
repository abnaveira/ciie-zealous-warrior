import pygame
import os

class SoundEffects:
    def __init__(self):

        # Initialize Volume
        self.globalVolume = 0.25

        # Initialize pygame effects player
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
        pygame.mixer.init()

        # List with sounds, to adjust volume of each one
        self.soundList = []

        # Directory containing the sounds
        musicDirectory = "musicAndSounds"

        directory = os.path.join(musicDirectory, "sword_slash.ogg")
        self.swordSlashSound = pygame.mixer.Sound(directory)
        self.soundList.append(self.swordSlashSound)

        directory = os.path.join(musicDirectory, "laser.ogg")
        self.laserSound = pygame.mixer.Sound(directory)
        self.soundList.append(self.laserSound)

        directory = os.path.join(musicDirectory, "metal_clash.ogg")
        self.metalClashSound = pygame.mixer.Sound(directory)
        self.soundList.append(self.metalClashSound)

        directory = os.path.join(musicDirectory, "whoosh.ogg")
        self.whooshSound = pygame.mixer.Sound(directory)
        self.soundList.append(self.whooshSound)

        # Set default volume for every sound in the list
        for sound in self.soundList:
            sound.set_volume(self.globalVolume)

    # Set volume for every sound on the list
    def setEffectsVolume(self, newVolume):
        for sound in self.soundList:
            sound.set_volume(newVolume)