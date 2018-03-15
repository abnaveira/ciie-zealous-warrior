# -*- encoding: utf-8 -*-
from projectiles import *

# -------------------------------------------------
# Class used for the window scroll control
# The values of the scroll will be positive,
# so the changes for the sprite positions in the screen will be:
# x - scroll[0] and y + scroll[1]
class scrollControl:

    # Input:
    # scroll: Value of the initial scroll, both "x" and "y" will be positive
    # minX, maxX, minY, maxY: Window edges for the scroll
    # wHeight, wWidth: height and width of the scene screen
    # scenery: Class that contains the scenary image
    def __init__(self, scroll, minX, maxX, minY, maxY, wHeight, wWidth,scenery):
        self.scroll = scroll
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY
        self.wHeight = wHeight
        self.wWidth = wWidth
        self.scenery =scenery

    # Input:
    # player: the charecter controlled by the player
    #
    # Output:
    # True: It updated scroll
    # False: It did not update the scroll
    def updateScrollX(self, player):
        # If the player overpass the left edge
        if (player.rect.left < self.minX):
            displacement = self.minX - player.rect.left

            # If there is no more scenary in the left
            if self.scroll[0] <= 0:
                self.scroll = (0, self.scroll[1])
                return False

            # If it is possible to scroll left
            else:
                self.scroll = (self.scroll[0] - displacement, self.scroll[1])
                return True

        # If the player overpass the right edge
        if (player.rect.right > self.maxX):
            displacement = player.rect.right - self.maxX

            # If there is no more scenary in the right
            if self.scroll[0] + self.wWidth >= self.scenery.rect.right:
                self.scroll = (self.scenery.rect.right - self.wWidth, self.scroll[1])
                return False

            # If it is possible to scroll right
            else:
                self.scroll = (self.scroll[0] + displacement, self.scroll[1])
                return True

        # If the player is between the edges
        return False

    # Input:
    # player: the charecter controlled by the player
    #
    # Output:
    # True: It updated scroll
    # False: It did not update the scroll
    def updateScrollY(self, player):
        # If the player overpass the top edge
        if (player.rect.top < self.minY):
            displacement = self.minY - player.rect.top

            # If there is no more scenary on the top
            if self.scroll[1] + self.wHeight >= self.scenery.rect.bottom:
                self.scroll = (self.scroll[0], self.scenery.rect.bottom - self.wHeight)
                return False

            # If it is possible to scroll top
            else:
                self.scroll = (self.scroll[0], self.scroll[1] + displacement)
                return True

        # If the player overpass the bottom edge
        if (player.rect.bottom > self.maxY):
            displacement = player.rect.bottom - self.maxY

            # If there is no more scenary on the bottom
            if self.scroll[1] <= 0:
                self.scroll = (self.scroll[0], 0)
                return False

            # If it is possible to scroll bottom
            else:
                self.scroll = (self.scroll[0], self.scroll[1] - displacement)
                return True

        # If the player is between the edges
        return False

    # Input:
    # player: the character controled by the player
    # sprites: The group of all the sprites that have to be updated
    def updateScroll(self, player, spritesList):

        updatedScrollX = self.updateScrollX(player)
        updatedScrollY = self.updateScrollY(player)
        if updatedScrollX or updatedScrollY:
            # Update the sprite positions and animations with the new scroll
            for group in spritesList:
                for sprite in iter(group):
                    sprite.setScreenPosition(self.scroll)

            # Update the scenery to show the new position
            self.scenery.update(self.scroll)

        return



