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
        platformList, flagArea, realFlagXPos, realPlayerPosition, playerX, playerY, spawnPointList, \
            enemyList, bossList, stageInfo,stageIntroStoryList, \
            stageOutroStoryList, musicFile= loadLevelData(levelFile)

        PygameScene.__init__(self, director, self.sceneryObj.windowWidth, self.sceneryObj.windowHeight)

        # Flag for music load and playback (scenes are pre-initialized, we cannot
        #  load music in each of them, as music uses a shared channel)
        self.musicLoaded = False
        # Store musicFile name
        self.musicFile = musicFile

        # Creates the background and backgroundColor
        self.background= Background(self.sceneryObj)
        self.foreground=Foreground(self.sceneryObj)
        self.backgroundColor = BackgroundColor(self.sceneryObj)

        # Creates the player and adds it to the group of players
        self.player = Player()
        self.playersGroup = pygame.sprite.Group(self.player)
        # Set the player in its initial position
        self.player.setPosition((playerX, playerY))

        # Initialises the enemy sprites group
        self.enemiesGroup = pygame.sprite.Group()

        # Initialises the bosses sprites group
        # Only used to test if the game is over (if you kill all the bosses)
        self.bossesGroup = pygame.sprite.Group()

        # Puts bosses in place if there are any
        # If there are bosses, this value is true
        self.thereAreBosses = len(bossList) > 0
        for boss in bossList:
            enemy = getBossFromName(boss.id)
            enemy.setPosition((boss.x,boss.y))
            self.enemiesGroup.add(enemy)
            self.bossesGroup.add(enemy)

        # Initializes spawn points list
        self.spawnPoints = []
        for spawnPoint in spawnPointList:
            self.spawnPoints.append(Spawn(spawnPoint, enemyList))

        self.lastSpawn = 0

        # Initializes the projectiles sprites group
        self.projectilesGroup = pygame.sprite.Group()

        # Stores all the platforms of the level
        self.platformsGroup = pygame.sprite.Group()
        for platform in platformList:
            self.platformsGroup.add(platform)

        # ---------------------------------------------------
        # TODO: implement this well
        # If there is no flag (this level has a boss)
        if flagArea is not None:
            self.thereIsFlag = True
        else:
            self.thereIsFlag = False

        self.flagRaised = False
        self.flagGroup = pygame.sprite.Group()
        self.bannerSpriteGroup = pygame.sprite.Group()
        self.realFlagXPos = realFlagXPos
        # To use as a timer when the flag is raised
        self.flagSpawnEnd = 0
        # If there is no Flag, none will be added
        if self.thereIsFlag:
            self.flagGroup.add(flagArea)

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
                animation.posX=scaleAndPlacement.x
                animation.posY=scaleAndPlacement.y
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

        # Creates a list for all the group sprites
        self.spritesList = [self.flagGroup, self.potionsGroup, self.playersGroup,
                            self.enemiesGroup, self.projectilesGroup, self.platformsGroup ]

        # Creates the class that will control the scroll
        self.controlScroll = scrollControl(self.sceneryObj.subImagePosition, self.sceneryObj.leftMin, self.sceneryObj.windowWidth - self.sceneryObj.leftMin,
                                           self.sceneryObj.topMin, self.sceneryObj.windowHeight - self.sceneryObj.topMin, self.sceneryObj.windowHeight, \
                                           self.sceneryObj.windowWidth, self.background,self.foreground)

        self.spriteStructure = SpriteStructure(self, self.player, self.enemiesGroup, self.platformsGroup, \
                                               self.projectilesGroup, None, None, self.potionsGroup)

        # Creates the HUD elements
        self.HUD = HUD(self.spriteStructure, stageInfo, stageIntroStoryList, stageOutroStoryList)
        # This variable controls the update of elements to show the text dialogs
        self.text_finished = False
        # This variable controls the draw of the final text
        self.final = False
        # This variable controls the update of elements to show the final text dialogs
        self.text_final_finished = False
        # Used for the music muting
        self.lastTimeMuted = pyTime.time()

    def update(self, time):
        if not self.final:
            if self.text_finished:
                if not self.musicLoaded:
                    # Load background music
                    pygame.mixer.music.load(self.musicFile)
                    # If the music is not muted
                    if not self.director.musicMuted:
                        # Play it indefinetely until method stop is called
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(0.25)
                    # Flag is now true
                    self.musicLoaded = True

                # Executes enemy AI
                for enemy in self.enemiesGroup:
                    enemy.move_cpu(self.spriteStructure)

                # Updates the player
                self.player.update(self.spriteStructure, time)

                # Updates the potions (destroys them if used)
                self.potionsGroup.update(self.player, self.platformsGroup, time)

                # ---------------------------------------------------
                # Flag logic

                # If there is flag
                if self.thereIsFlag:

                    # If the flag has already been raised
                    if self.flagRaised:
                        # If a minute has passed since the flag has been raised
                        if pyTime.time() > self.flagSpawnEnd:
                            # If there are no more enemies on the level
                            if len(self.enemiesGroup.sprites()) == 0:
                                # This changes scene
                                self.final = True
                        else:
                            millis = int(round(pyTime.time() * 1000))
                            timePassed = millis - self.lastSpawn
                            if timePassed >= 3000:
                                numPoints = []
                                for spawnPoint in iter(self.spawnPoints):
                                    distx = spawnPoint.x - self.player.position[0]
                                    disty = spawnPoint.y - self.player.position[1]
                                    if (distx * distx + disty * disty) > 250000:
                                        numPoints.append(spawnPoint.id)
                                point = random.randint(0, len(numPoints) - 1)
                                for spawnPoint in iter(self.spawnPoints):
                                    spawnPoint.spawnAfterFlag(self, self.player, numPoints[point])
                                self.lastSpawn = millis
                    else:
                        for spawnPoint in iter(self.spawnPoints):
                            spawnPoint.spawnBeforeFlag(self, self.player)

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
                            # Time a minute from now, when the spawning has ended
                            self.flagSpawnEnd = pyTime.time() + 60

                # --------------------------------------------------

                # If there are bosses and they are dead, you win
                if self.thereAreBosses:
                    if len(self.bossesGroup.sprites()) == 0:
                        self.final = True

                # Updates the banner sprite
                self.bannerSpriteGroup.update(self.player, time)

                # Updates the enemies
                self.enemiesGroup.update(self.spriteStructure, time)

                # Updates the projectiles
                self.projectilesGroup.update(self.spriteStructure, time)

                # Updates the platforms
                self.platformsGroup.update(time)

                # Update scroll
                self.controlScroll.updateScroll(self.player, self.spritesList,self.frontAnimations,self.backAnimations)

                # Update the background color if it is necessary
                self.backgroundColor.update(time)

                # Update HUD elements
                self.HUD.update()


    def draw(self, screen):
        # Background color
        self.backgroundColor.draw(screen)
        # Back animations
        for animation in self.backAnimations:
            animation.draw(screen)
        # Background
        self.background.draw(screen)
        # Flag Sprite
        self.bannerSpriteGroup.draw(screen)
        # Sprites
        for group in self.spritesList:
            group.draw(screen)
        #Foreground
        self.foreground.draw(screen)

        # Front animations
        for animation in self.frontAnimations:
            animation.draw(screen)
        # HUD
        self.HUD.draw(self.final, screen)

    def events(self, events_list):
        # Look in the events
        for event in events_list:
            # If there is a quit event indicate the director to leave
            if event.type == pygame.QUIT:
                self.director.leaveProgram()

        keysPressed = pygame.key.get_pressed()
        if not self.text_finished:
            # Updates the dialog box of the HUD if it is necessary
            self.text_finished = self.HUD.changeBox(keysPressed, K_RETURN, K_q)
            return
        if self.final:
            if not self.text_final_finished:
                # Updates the dialog box of the HUD if it is necessary
                self.text_final_finished = self.HUD.changeFinalBox(keysPressed, K_RETURN, K_q)
                return
            else:
                # Abort music playback
                pygame.mixer.music.stop()
                self.director.leaveScene()
        # If m key is pressed, mute/unmute
        if keysPressed[K_m]:
            # If it is not muted, mute it
            if pyTime.time() - self.lastTimeMuted > 0.5:
                if not self.director.musicMuted:
                    # Stop music
                    pygame.mixer.music.stop()
                    # Reverse the flag
                    self.director.musicMuted = True
                    self.lastTimeMuted = pyTime.time()
                    # If it was muted, unmute it
                else:
                    # Play music indefinetely until method stop is called
                    pygame.mixer.music.play(-1)
                    # Reverse the flag
                    self.director.musicMuted = False
                    self.lastTimeMuted = pyTime.time()
        if keysPressed[K_PLUS]:
            volume = pygame.mixer.music.get_volume()
            if volume < 1:
                pygame.mixer.music.set_volume(volume + 0.01)

        if keysPressed[K_MINUS]:
            volume = pygame.mixer.music.get_volume()
            if volume > 0:
                pygame.mixer.music.set_volume(volume - 0.01)

        # Indicates the actions to do to the player
        self.player.move(keysPressed, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE)

    def openDeathScreen(self):
        # Open the death screen passing the file of the level
        self.director.changeScene(DeathMenu(self.director, self.levelFile,
                                            self.sceneryObj.windowWidth, self.sceneryObj.windowHeight))

    # If the player is contained within the flag rectangle of influence
    # return true
    def checkFlag (self):
        flagList = self.flagGroup.sprites()
        flag = flagList.pop()
        return flag.rect.colliderect(self.player.rect)