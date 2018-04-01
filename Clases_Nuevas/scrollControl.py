# -*- encoding: utf-8 -*-

# -------------------------------------------------
# Class used for the window scroll control
# The values of the scroll will be positive,
# so the changes for the sprite positions in the screen will be:
# x - scroll[0] and y + scroll[1]
class scrollControl:

    # Input:
    # subImagePosition: Position of the window screen in the background
    # minX, maxX, minY, maxY: Window edges for the scroll
    # wHeight, wWidth: height and width of the scene screen
    # background, foreground: Classes that contain the scenery of the image
    def __init__(self, subImagePosition, minX, maxX, minY, maxY, wHeight, wWidth, background, foreground):
        # Position of the initial window screen
        (posX, posY) = subImagePosition
        # Calculates left and top limits for the scroll with the window screen and background size
        self.limits = (posX * -1, (background.rect.bottom - (posY + wHeight) ) * -1)
        self.scroll = (0,0)

        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY
        self.wHeight = wHeight
        self.wWidth = wWidth
        self.background = background
        self.foreground = foreground

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
            if self.scroll[0] <= self.limits[0]:
                self.scroll = (self.limits[0], self.scroll[1])
                return False

            # If it is possible to scroll left
            else:
                self.scroll = (self.scroll[0] - displacement, self.scroll[1])
                return True

        # If the player overpass the right edge
        if (player.rect.right > self.maxX):
            displacement = player.rect.right - self.maxX

            # If there is no more scenary in the right
            if self.scroll[0] + self.wWidth - self.limits[0] >= self.background.rect.right:
                self.scroll = (self.background.rect.right - self.wWidth + self.limits[0], self.scroll[1])
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
            if self.scroll[1] + self.wHeight - self.limits[1] >= self.background.rect.bottom:
                self.scroll = (self.scroll[0], self.background.rect.bottom - self.wHeight + self.limits[1])
                return False

            # If it is possible to scroll top
            else:
                self.scroll = (self.scroll[0], self.scroll[1] + displacement)
                return True

        # If the player overpass the bottom edge
        if (player.rect.bottom > self.maxY):
            displacement = player.rect.bottom - self.maxY

            # If there is no more scenary on the bottom
            if self.scroll[1] <= self.limits[1]:
                self.scroll = (self.scroll[0], self.limits[1])
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
    # animationsList: The group of all the animations that have to be updated
    def updateScroll(self, player, spritesList, frontAnimations, backAnimations):
        updatedScrollX = self.updateScrollX(player)
        updatedScrollY = self.updateScrollY(player)
        if updatedScrollX or updatedScrollY:
            # Update the sprite positions and animations with the new scroll
            for group in spritesList:
                for sprite in iter(group):
                    sprite.setScreenPosition(self.scroll)

            # Update the animations positions
            for animation in frontAnimations:
                animation.setScreenPosition(self.scroll)
            for animation in backAnimations:
                animation.setScreenPosition(self.scroll)

            # Update the scenery to show the new position
            self.background.update(self.scroll)
            self.foreground.update(self.scroll)

        return



