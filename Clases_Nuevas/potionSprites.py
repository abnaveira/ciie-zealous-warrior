from standingSprites import *
from characters import *

POTIONS_ANIM_DELAY = 6

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
                speedy += GRAVITY * time

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
        if player.HP != PLAYER_BASE_HEALTH:
            # Update player hp
            newHP = player.HP + PLAYER_BASE_HEALTH * self.potionValue
            # If HP exceeds player base health, we truncate it
            if newHP > PLAYER_BASE_HEALTH:
                newHP = PLAYER_BASE_HEALTH
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
# TODO: functions to create a random potion with given chances of any potion appearing and individual %