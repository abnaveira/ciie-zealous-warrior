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
        #self.image = pygame.Surface((0, 0))
        self.image = pygame.Surface((rectangle.width, rectangle.height))
        self.image.fill((255,0,0))

# -------------------------------------------------
# Class created for the flag

class FlagArea(MySprite):
    def __init__(self, rectangle):
        MySprite.__init__(self)
        # The flag will be a rectangle
        self.rect = rectangle
        # The position will be set as the size of the Flag
        self.setPosition((self.rect.left, self.rect.bottom))
        # The flag area is invisible
        #self.image = pygame.Surface((0, 0))
        self.image = pygame.Surface((rectangle.width, rectangle.height))
        self.image.fill((0,255,0))

# -------------------------------------------------
# Class for the background color

class BackgroundColor:
    def __init__(self, sceneryObj):
        self.color = (sceneryObj.red, sceneryObj.green, sceneryObj.blue)

    # It has to be implmented if there is some variations over time in the background
    def update(self, time):
        return

    def draw(self, screen):
        screen.fill(self.color)


# -------------------------------------------------
# Class for the scenary

class Background:
    def __init__(self, sceneryObj):
        self.layers=[]
        self.left = sceneryObj.subImagePosition[0]
        self.bottom = sceneryObj.subImagePosition[1] + sceneryObj.windowHeight
        for (file,parallaxValue,scaleX,scaleY) in sceneryObj.backgroundLayers:
            image = ResourcesManager.loadImageWithAlpha(file)
            if not (scaleX == 0 or scaleY == 0):
                image = pygame.transform.scale(image, (scaleX,scaleY))
            rect = image.get_rect()
            rectSubimage = pygame.Rect(0,0,sceneryObj.windowWidth,sceneryObj.windowHeight)
            rectSubimage.left = self.left
            rectSubimage.bottom = self.bottom
            self.layers.append((image,parallaxValue,rect,rectSubimage))

        self.rect = pygame.Rect((0,0),(sceneryObj.scaleX,sceneryObj.scaleY))

    def update(self, scroll):
        for (_,parallaxValue,_,rectSubimage) in self.layers:

            rectSubimage.left = self.left + scroll[0]-(scroll[0]*parallaxValue)
            rectSubimage.bottom = self.bottom - (scroll[1]-(scroll[1]*parallaxValue))

    def draw(self, screen):
        for(image,_,rect,rectSubimage) in self.layers:
            screen.blit(image, rect, rectSubimage)

class Foreground:
    def __init__(self, sceneryObj):
        self.layers=[]
        self.left = sceneryObj.subImagePosition[0]
        self.bottom = sceneryObj.subImagePosition[1] + sceneryObj.windowHeight
        for (file,parallaxValue,scaleX,scaleY) in sceneryObj.foregroundLayers:
            image = ResourcesManager.loadImageWithAlpha(file)
            if not (scaleX == 0 or scaleY == 0):
                image = pygame.transform.scale(image, (scaleX,scaleY))
            rect = image.get_rect()
            rectSubimage = pygame.Rect(0,0,sceneryObj.windowWidth,sceneryObj.windowHeight)
            rectSubimage.left = self.left
            rectSubimage.bottom = self.bottom
            self.layers.append((image,parallaxValue,rect,rectSubimage))

        self.rect = pygame.Rect((0,0),(sceneryObj.scaleX,sceneryObj.scaleY))

    def update(self, scroll):
        for (_,parallaxValue,_,rectSubimage) in self.layers:
            rectSubimage.left = self.left + scroll[0] - (scroll[0] * parallaxValue)
            rectSubimage.bottom = self.bottom - (scroll[1] - (scroll[1] * parallaxValue))

    def draw(self, screen):
        for(image,_,rect,rectSubimage) in self.layers:
            screen.blit(image, rect, rectSubimage)




