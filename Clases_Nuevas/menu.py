# -*- encoding: utf-8 -*-

from scene import *
from resourcesManager import *

# -------------------------------------------------
# Abstract class for GUIElements

class GUIElement:
    def __init__(self, screen, rectangle):
        self.screen = screen
        self.rect = rectangle

    def setPosition(self, position):
        (positionx, positiony) = position
        self.rect.left = positionx
        self.rect.bottom = positiony

    def positionAtElement(self, position):
        (positionx, positiony) = position
        if (positionx>=self.rect.left) and (positionx<=self.rect.right) and (positiony>=self.rect.top) and (positiony<=self.rect.bottom):
            return True
        else:
            return False

    def draw(self):
        raise NotImplemented("It has to be implemented")
    def action(self):
        raise NotImplemented("It has to be implemented")


# -------------------------------------------------
# Class button and different buttons implementations

class Button(GUIElement):
    def __init__(self, screen, imageName, position):
        # Loads the image
        self.image = ResourcesManager.loadImage(imageName,-1)
        self.image = pygame.transform.scale(self.image, (130, 60))
        GUIElement.__init__(self, screen, self.image.get_rect())
        # Sets button in position
        self.setPosition(position)
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class PlayButton(Button):
    def __init__(self, screen, window_width, window_height):
        Button.__init__(self, screen, 'PlayButton.png', (window_width/5*2, window_height/8*6))
    def action(self):
        self.screen.menu.executeGame()

class LeaveButton(Button):
    def __init__(self, screen, window_width, window_height):
        Button.__init__(self, screen, 'ExitButton.png', (window_width/5*2, window_height/8*7))
    def action(self):
        self.screen.menu.exitProgram()

# -------------------------------------------------
# Class GUIText and different text implementations

class GUIText(GUIElement):
    def __init__(self, screen, font, color, text, position):
        # Creates the text image
        self.image = font.render(text, True, color)
        GUIElement.__init__(self, screen, self.image.get_rect())
        # Sets text in position
        self.setPosition(position)
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class PlayText(GUIText):
    def __init__(self, screen, window_width, window_height):
        # Asks the resource manager for the font
        font = ResourcesManager.loadFont('arial', 26)
        GUIText.__init__(self, screen, font, (0, 0, 0), 'Play', (window_width/5*2, window_height/7*5))
    def action(self):
        self.screen.menu.executeGame()

class LeaveText(GUIText):
    def __init__(self, screen, window_width, window_height):
        # Asks the resource manager for the font
        font = ResourcesManager.loadFont('arial', 26)
        GUIText.__init__(self, screen, font, (0, 0, 0), 'Exit', (window_width/5*2, window_height/7*6))
    def action(self):
        self.screen.menu.exitProgram()

# -------------------------------------------------
# Clase screenGUI y las distintas screens

class GUIScreen:
    def __init__(self, menu, imageName):
        self.menu = menu
        # Loads menu image
        self.image = ResourcesManager.loadImage(imageName)
        self.image = pygame.transform.scale(self.image, (menu.window_width, menu.window_height))
        # List of GUI elements
        self.GUIelements = []
        # List of animations
        self.animations = []

    def events(self, event_list):
        for event in event_list:
            if event.type == MOUSEBUTTONDOWN:
                self.elementClic = None
                for element in self.GUIelements:
                    if element.positionAtElement(event.pos):
                        self.elementClic = element
            if event.type == MOUSEBUTTONUP:
                for element in self.GUIelements:
                    if element.positionAtElement(event.pos):
                        if (element == self.elementClic):
                            element.action()

    def draw(self, screen):
        # Draws first the menu image
        screen.blit(self.image, self.image.get_rect())
        # After, draws the animations
        for animation in self.animations:
            animation.draw(screen)
        # Finally, draws the buttons
        for element in self.GUIelements:
            element.draw(screen)

class GUIInitialScreen(GUIScreen):
    def __init__(self, menu):
        GUIScreen.__init__(self, menu, 'menuBackground.png')
        # Creates the buttons
        playButton = PlayButton(self, menu.window_width, menu.window_height)
        leaveButton = LeaveButton(self, menu.window_width, menu.window_height)
        self.GUIelements.append(playButton)
        self.GUIelements.append(leaveButton)
        # Creates the texts
        #playText = PlayText(self, menu.window_width, menu.window_height)
        #leaveText = LeaveText(self, menu.window_width, menu.window_height)
        #self.GUIelements.append(playText)
        #self.GUIelements.append(leaveText)

# -------------------------------------------------
# Class for the menu scene

class Menu(PygameScene):

    def __init__(self, director, window_width, window_height):
        PygameScene.__init__(self, director, window_width, window_height);
        self.window_width = window_width
        self.window_height = window_height
        # Creates the list of screens
        self.screenList = []
        self.screenList.append(GUIInitialScreen(self))
        self.showInitialWindow()

    def update(self, *args):
        return

    def events(self, event_list):
        for event in event_list:
            # If the key scape is pressed
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.exitProgram()
            elif event.type == pygame.QUIT:
                self.director.leaveProgram()

        self.screenList[self.actualScreen].events(event_list)

    def draw(self, screen):
        self.screenList[self.actualScreen].draw(screen)

    def exitProgram(self):
        self.director.leaveProgram()

    def executeGame(self):
        self.director.leaveScene()
        return

    def showInitialWindow(self):
        self.actualScreen = 0

    # def mostrarPantallaConfiguracion(self):
    #    self.actualScreen = ...


