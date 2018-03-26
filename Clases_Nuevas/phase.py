# -*- coding: utf-8 -*-
from Clases_Nuevas.SpriteStructure import SpriteStructure
from scene import PygameScene
from xmlLevelParser import *
from characters import *
from scrollControl import *
from animationsPygame import *
from miscSprites import *
from director import *
from standingSprites import *
from potionSprites import *
from HUDElements import *
from spawn import *
from menu import DeathMenu
import time as pyTime

# -------------------------------------------------
# Class for pygame scenes with one player

class PhaseScene(PygameScene):

    def __init__(self, director, levelFile):
        # Save the director to call the end of the phase when necessary
        self.director = director
        self.levelFile = levelFile

        # It reads the file with the level paramethers
        self.sceneryObj, frontImagesList, frontAnimationsList, backAnimationsList, \
        platformList, flagArea, realFlagXPos, playerX, playerY, spawnPointList, \
            enemyList, bossList, stageInfo, musicFile= loadLevelData(levelFile)

        PygameScene.__init__(self, director, self.sceneryObj.windowWidth, self.sceneryObj.windowHeight)

        # Flag for music playBack (scenes are pre-initialized, we cannot load music in each
        # of them, as music uses a shared channel
        self.alreadyPlaying = False
        # Store musicFile name
        self.musicFile = musicFile

        # Creates the scenary and background
        self.scenery= Scenary(self.sceneryObj)
        self.background = Background(self.sceneryObj)

        # Set scroll to (0,0)
        self.scroll = (0, 0)

        # Creates the player and adds it to the group of players
        self.player = Player()
        self.playersGroup = pygame.sprite.Group(self.player)

        # Creates the HUD elements
        self.HUD = HUD(self.player, stageInfo.title, stageInfo.description)

        # Set the player in its initial position
        self.player.setPosition((playerX, playerY))

        # Initialises the enemy sprites group
        self.enemiesGroup = pygame.sprite.Group()

        # Puts bosses in place if there are any
        for boss in bossList:
            enemy = getBossFromName(boss.id)
            enemy.setPosition((boss.x,boss.y))
            self.enemiesGroup.add(enemy)

        # Initializes spawn points list
        self.spawnPoints = []
        for spawnPoint in spawnPointList:
            self.spawnPoints.append(Spawn(spawnPoint, enemyList))

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

        # To use as a timer when the flag is raised
        self.flagSpawnEnd = 0
        # ---------------------------------------------------

        # Initialize potions group
        self.potionsGroup = pygame.sprite.Group()

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
        self.spritesList = [self.flagGroup, self.potionsGroup, self.playersGroup,
                            self.enemiesGroup, self.projectilesGroup, self.platformsGroup ]

        # Creates the class that will control the scroll
        self.controlScroll = scrollControl(self.scroll, self.sceneryObj.leftMin, self.sceneryObj.windowWidth - self.sceneryObj.leftMin,
                                           self.sceneryObj.topMin, self.sceneryObj.windowHeight - self.sceneryObj.topMin, self.sceneryObj.windowHeight, \
                                           self.sceneryObj.windowWidth, self.scenery)

        self.spriteStructure = SpriteStructure(self, self.player, self.enemiesGroup, self.platformsGroup, \
                                               self.projectilesGroup, None, None, self.potionsGroup)

    # Allows to add enemies to the phase
    def addEnemies(self, enemySprite):
        self.enemiesGroup.add(enemySprite)
        self.dinamicSpritesGroup.add(enemySprite)

    def update(self, time):

        if not self.alreadyPlaying:
            # Load background music
            pygame.mixer.music.load(self.musicFile)
            # Play it indefinetely until method stop is called
            pygame.mixer.music.play(-1)
            # Flag is now true
            self.alreadyPlaying = True

        # Executes enemy AI
        for enemy in self.enemiesGroup:
            enemy.move_cpu(self.spriteStructure)

        # Updates the player
        self.player.update(self.spriteStructure, time)

        # Updates the potions (destroys them if used)
        self.potionsGroup.update(self.player, self.platformsGroup, time)

        # ---------------------------------------------------
        # Flag logic

        # If the flag hasn't been raised
        if not self.flagRaised:
            self.flagRaised = PhaseScene.checkFlag(self)
            # The FIRST time the flag is raised
            if self.flagRaised:
                flagList = self.flagGroup.sprites()
                flag = flagList.pop()
                # We set the Banner in its position
                bannerSprite = Banner((self.realFlagXPos,flag.rect.bottom))
                self.bannerSpriteGroup.add(bannerSprite)
                # We destroy enemies
                for spawnPoint in iter(self.spawnPoints):
                    spawnPoint.clear()
                self.enemiesGroup.empty()
                for sprite in iter(self.dinamicSpritesGroup):
                    if sprite != self.player:
                        self.dinamicSpritesGroup.remove(sprite)
                # We add new enemies
                for spawnPoint in iter(self.spawnPoints):
                    spawnPoint.add_enemies(20)
                # Time a minute from now, when the spawning has ended
                self.flagSpawnEnd = pyTime.time() + 60

        # If the flag has already been raised
        if self.flagRaised:
            # If a minute has passed since the flag has been raised
            if pyTime.time() > self.flagSpawnEnd:
                # If there are no more enemies on the level
                if (len(self.enemiesGroup.sprites()) == 0):
                    # Abort music playback
                    pygame.mixer.music.stop()
                    # TODO: put a message, and press enter to change level
                    # This changes scene
                    self.director.leaveScene()
        # ---------------------------------------------------

        # Updates the banner sprite
        self.bannerSpriteGroup.update(self.player, time)

        # Updates the enemies
        self.enemiesGroup.update(self.spriteStructure, time)

        # Updates the projectiles
        self.projectilesGroup.update(self.spriteStructure, time)

        # Updates the platforms
        self.platformsGroup.update(time)

        # Update scroll
        self.controlScroll.updateScroll(self.player, self.spritesList)

        # Update the background if it is necessary
        self.background.update(time)

        # Update HUD elements
        self.HUD.update()

        # Spawn enemies
        for spawnPoint in iter(self.spawnPoints):
            spawnPoint.spawn(self)

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
        # Update HUD elements
        self.HUD.draw(screen)

    def events(self, events_list):
        # Miramos a ver si hay algun evento de salir del programa
        for event in events_list:
            # Si se quiere salir, se le indica al director
            if event.type == pygame.QUIT:
                self.director.leaveProgram()

        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        keysPressed = pygame.key.get_pressed()
        self.player.move(keysPressed, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE)

    def openDeathScreen(self):
        # Open the death screen passing the file of the level
        self.director.changeScene(DeathMenu(self.director, self.levelFile,
                                            self.sceneryObj.windowWidth, self.sceneryObj.windowHeight))

    # If the player is contained within the flag rectangle of influence
    # return true
    def checkFlag (self):
        (speedx, speedy) = self.player.speed
        flagList = self.flagGroup.sprites()
        flag = flagList.pop()
        return flag.rect.colliderect(self.player.rect)