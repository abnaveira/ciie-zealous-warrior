from standingSprites import *
#from characters import PLAYER_BASE_HEALTH
import characters
import random


POTIONS_ANIM_DELAY = 6

# Potion spawn chance after enemy kill is 30%
POTION_SPAWN_CHANCE = 0.3

# Potion chances must be ranges from 0 to 1, with differences being probabilities of each potion
POTION_SMALL_CHANCE_RANGE = 0.5
POTION_MEDIUM_CHANCE_RANGE = 0.85
POTION_LARGE_CHANCE_RANGE = 1.0

class Potion(StandingSprites):
    # Superclass with the behavior of potions
    def __init__(self, imageFile, coordFile, nImages, animDelay, looking, potionValue):
        StandingSprites.__init__(self, imageFile, coordFile, nImages, animDelay, looking)
        # Potion Value is assigned as a pectenage (I.E.: 25 will be 25% of the health)
        self.potionValue = potionValue
        self.onPlatform = False
        self.speed = (0,0)


    def update(self, player, platforms, time):

        # If on the air, we have to check if we are landing on a platform
        (speedx, speedy) = self.speed
        if not self.onPlatform:
            for platform in iter(platforms):
                if (platform.rect.top < self.rect.bottom) \
                            and ((self.rect.bottom - self.rect.height/2) < platform.rect.top):
                    # Set y value to top of the platform and break fall
                    self.setPosition((self.position[0], platform.position[1]-platform.rect.height+1))
                    self.onPlatform = True
                    speedy = 0

            # Otherwise, keep falling accelerated by gravity
            if not self.onPlatform:
                speedy += characters.GRAVITY * time

            # Update speed
            self.speed = (speedx, speedy)
        self.updateStance()

        # Update the scroll
        self.scroll = player.scroll

        # If the player collides with a potion
        if self.rect.colliderect(player.rect):
            # Use the potion
            self.usePotion(player)

        StandingSprites.update(self, time)

    def usePotion(self, player):
        # If the player is not at max health
        if player.HP != characters.PLAYER_BASE_HEALTH:
            # Update player hp
            newHP = player.HP + characters.PLAYER_BASE_HEALTH * self.potionValue
            # If HP exceeds player base health, we truncate it
            if newHP > characters.PLAYER_BASE_HEALTH:
                newHP = characters.PLAYER_BASE_HEALTH
            player.HP = newHP
            # Destroy the potion after use
            self.kill()

# --------------------------------------------------------------------------------
# Potion subclasses

class PotionSmall(Potion):
    # Small potion with 15% life regeneration
    def __init__(self):
        potionValue = 0.15
        Potion.__init__(self, 'potions.png', 'coordPotionSmall.txt', [1], POTIONS_ANIM_DELAY,
                        LEFT, potionValue)

class PotionMedium(Potion):
    # Medium potion with 25% life regeneration
    def __init__(self):
        potionValue = 0.25
        Potion.__init__(self, 'potions.png', 'coordPotionMedium.txt', [1], POTIONS_ANIM_DELAY,
                        LEFT, potionValue)

class PotionLarge(Potion):
    # Large potion with 50% life regeneration
    def __init__(self):
        potionValue = 0.5
        Potion.__init__(self, 'potions.png', 'coordPotionLarge.txt', [1], POTIONS_ANIM_DELAY,
                        LEFT, potionValue)

# -------------------------------------------------------------------------

# Function that returns a random potion or none, based on chances in the constant of this file
def getRandomPotion():
    # Initialize random seed
    random.seed
    # Get random number from 1.0 to 0.0
    drop = random.random()
    # If it is less than the spawn chance, get potion
    if (drop <= POTION_SPAWN_CHANCE):
        # Get another random number from 1.0 to 0.0
        potion = random.random()
        # Choose potion based on number
        if(potion <= POTION_SMALL_CHANCE_RANGE):
            return PotionSmall()
        elif(potion <= POTION_MEDIUM_CHANCE_RANGE):
            return PotionMedium()
        else:
            return PotionLarge()
    else:
        return None