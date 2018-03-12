from mysprite import MySprite
from resourcesManager import *

# -------------------------------------------------
# Class created for the scenery platforms

class Platform(MySprite):
    def __init__(self, rectangle):
        MySprite.__init__(self)
        # The platforms will be rectangles
        self.rect = rectangle
        # The position will be set as the size of the platform
        self.setPosition((self.rect.left, self.rect.bottom))
        # The platforms are invisible
        self.image = pygame.Surface((0, 0))


# -------------------------------------------------
# Class for the background

class Background:
    def __init__(self, sceneryObj):
        self.color = (sceneryObj.red, sceneryObj.green, sceneryObj.blue)

    # It has to be implmented if there is some variations over time in the background
    def update(self, time):
        return

    def draw(self, screen):
        screen.fill(self.color)


# -------------------------------------------------
# Class for the scenary

class Scenary:
    def __init__(self, sceneryObj):
        self.image = ResourcesManager.loadImage(sceneryObj.file, -1)
        if sceneryObj.scaleX == 0 or sceneryObj.scaleY == 0:
            self.image = pygame.transform.scale(self.image, (sceneryObj.scaleX, sceneryObj.scaleY))

        self.rect = self.image.get_rect()

        # The subimage that we see
        self.rectSubimage = pygame.Rect(0, 0, sceneryObj.windowWidth, sceneryObj.windowHeight)
        self.rectSubimage.left = 0  # Starts on the left
        self.rectSubimage.bottom = self.rect.bottom # Starts on the bottom

    def update(self, scroll):
        self.rectSubimage.left = scroll[0]
        self.rectSubimage.bottom = self.rect.bottom - scroll[1]

    def draw(self, screen):
        screen.blit(self.image, self.rect, self.rectSubimage)



