# -*- coding: utf-8 -*-

from scene import PygameScene
from xmlLevelParser import *
from characters import *
from scrollControl import *
from animationsPygame import *
from miscSprites import *
from director import *
from standingSprites import *
from potionSprites import *

# -------------------------------------------------
# Class for pygame scenes with one player

class PhaseScene(PygameScene):

    def __init__(self, director, levelFile):
        # Save the director to call the end of the phase when necessary
        self.director = director

        # It reads the file with the level paramethers
        sceneryObj, frontImagesList, frontAnimationsList, backAnimationsList, \
        platformList, flagArea, realFlagXPos, playerX, playerY, spawnPointList\
            = loadLevelData(levelFile)

        PygameScene.__init__(self, director, sceneryObj.windowWidth, sceneryObj.windowHeight)

        # Creates the scenary and background
        self.scenery= Scenary(sceneryObj)
        self.background = Background(sceneryObj)

        # Set scroll to (0,0)
        self.scroll = (0, 0)

        # Creates the player and adds it to the group of players
        self.player = Player()
        self.playersGroup = pygame.sprite.Group(self.player)

        # Set the player in its initial position
        self.player.setPosition((playerX, playerY))

        # Initializes the enemy sprites group
        enemy1 = Imp()
        enemy1.setPosition((741, 210))
        enemy2 = AxeKnight()
        enemy2.setPosition((300, 418))
        self.enemiesGroup = pygame.sprite.Group(enemy1, enemy2)

        # Initializes the projectiles sprites group
        self.projectilesGroup = pygame.sprite.Group()

        # Stores all the platforms of the level
        self.platformsGroup = pygame.sprite.Group()
        for platform in platformList:
            self.platformsGroup.add(platform)
        # ---------------------------------------------------
        # FLAG AS PLATFORM TEMPORARY
        # self.platformsGroup.add(Platform(flag))
        # TODO: implement this well
        self.flagRaised = False
        self.flagGroup = pygame.sprite.Group()
        self.bannerSpriteGroup = pygame.sprite.Group()
        self.flagGroup.add(flagArea)
        self.realFlagXPos = realFlagXPos
        # ---------------------------------------------------

        # Potions group
        self.potionsGroup = pygame.sprite.Group()
        # Put a potion in the map
        potion1 = PotionLarge()
        potion1.setPosition((300,418))
        self.addPotions(potion1)
        potion2 = PotionMedium()
        potion2.setPosition((400, 418))
        self.addPotions(potion2)

        # Loads the animations in the front
        self.frontAnimations = []
        for frontAnimation in frontAnimationsList:
            for scaleAndPlacement in frontAnimation.scaleAndPlacementList:
                animation = AnimationFromList(frontAnimation.frameList)
                if ((scaleAndPlacement.scaleX != 0) and (scaleAndPlacement.scaleY != 0)):
                    animation.scale((scaleAndPlacement.scaleX, scaleAndPlacement.scaleY))
                animation.positionX = scaleAndPlacement.x
                animation.positionY = scaleAndPlacement.y
                animation.play()
                self.frontAnimations.append(animation)

        # Loads the animations in the back
        self.backAnimations = []
        for backAnimation in backAnimationsList:
            for scaleAndPlacement in backAnimation.scaleAndPlacementList:
                animation = AnimationFromList(backAnimation.frameList)
                if ((scaleAndPlacement.scaleX != 0) and (scaleAndPlacement.scaleY != 0)):
                    animation.scale((scaleAndPlacement.scaleX, scaleAndPlacement.scaleY))
                animation.positionX = scaleAndPlacement.x
                animation.positionY = scaleAndPlacement.y
                animation.play()
                self.backAnimations.append(animation)

        # Creates a group for the dinamic sprites
        self.dinamicSpritesGroup = pygame.sprite.Group(self.player)

        # Creates a list for all the group sprites
        self.spritesList = [self.flagGroup, self.playersGroup,self.potionsGroup,
                            self.enemiesGroup, self.projectilesGroup, self.platformsGroup ]

        # Creates the class that will control the scroll
        self.controlScroll = scrollControl(self.scroll, sceneryObj.leftMin, sceneryObj.windowWidth - sceneryObj.leftMin,
                                           sceneryObj.topMin, sceneryObj.windowHeight - sceneryObj.topMin, sceneryObj.windowHeight, \
                                           sceneryObj.windowWidth, self.scenery)

    # Allows to add enemies to the phase
    def addEnemies(self, enemySprite):
        self.enemiesGroup.add(enemySprite)
        self.dinamicSpritesGroup.add(enemySprite)

    # Allows to add potions to the phase
    def addPotions(self, potionSprite):
        self.potionsGroup.add(potionSprite)

    def update(self, time):
        # Executes enemy AI
        for enemy in self.enemiesGroup:
            enemy.move_cpu(self.player, self.platformsGroup)

        # Updates the player
        self.player.update(self.platformsGroup, self.projectilesGroup, time)

        # Updates the potions (destroys them if used)
        self.potionsGroup.update(self.player, self.platformsGroup, time)

        # ---------------------------------------------------
        # CODE TO TRY FLAGS
        if not self.flagRaised:
            self.flagRaised = PhaseScene.checkFlag(self)
            if self.flagRaised:
                flagList = self.flagGroup.sprites()
                flag = flagList.pop()
                # We set the Banner in its position
                bannerSprite = Banner((self.realFlagXPos,flag.rect.bottom))
                self.bannerSpriteGroup.add(bannerSprite)
                # This changes scene
                #Director.leaveScene(self.director)

        # ---------------------------------------------------

        # Updates the banner sprite
        self.bannerSpriteGroup.update(self.player, time)

        # Updates the enemies
        self.enemiesGroup.update(self.platformsGroup, self.projectilesGroup, time)

        # Updates the projectiles
        self.projectilesGroup.update(self.player, self.enemiesGroup, self.platformsGroup, self.projectilesGroup, time)

        # Updates the platforms
        self.platformsGroup.update(time)

        # Update scroll
        self.controlScroll.updateScroll(self.player, self.spritesList)

        # Update the background if it is necessary
        self.background.update(time)

    def draw(self, screen):
        # Background
        self.background.draw(screen)
        # Back animations
        for animation in self.backAnimations:
            animation.draw(screen)
        # Scenery
        self.scenery.draw(screen)
        # Flag Sprite
        self.bannerSpriteGroup.draw(screen)
        # Sprites
        for group in self.spritesList:
            group.draw(screen)
        # Front animations
        for animation in self.frontAnimations:
            animation.draw(screen)

    def events(self, events_list):
        # Miramos a ver si hay algun evento de salir del programa
        for event in events_list:
            # Si se quiere salir, se le indica al director
            if event.type == pygame.QUIT:
                self.director.leaveProgram()

        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        keysPressed = pygame.key.get_pressed()
        self.player.move(keysPressed, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE)

    # If the player is contained within the flag rectangle of influence
    # return true
    def checkFlag (self):
        (speedx, speedy) = self.player.speed
        flagList = self.flagGroup.sprites()
        flag = flagList.pop()
        return flag.rect.colliderect(self.player.rect)