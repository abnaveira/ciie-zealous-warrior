# -*- encoding: utf-8 -*-

import sys
import os
import xml.etree.ElementTree as ET
from miscSprites import *
import pygame

BANNER_WIDTH = 58

def openXmlGetTree(xmlFileName):
    # Get the directory where this file is
    directory = sys.path[0]

    # Append the directory where levels are located
    directory = os.path.join(directory, "levelFiles")

    # Append the level we want to open
    xmlFile = os.path.join(directory, xmlFileName)

    # Parse the file and get the tree
    return ET.parse(xmlFile)

def getAllLevelFiles(levelsFile):
    tree = openXmlGetTree(levelsFile)
    # We get the "levels" tag
    root = tree.getroot()

    levelFilesList = []
    #Load all levels
    for level in root.iter("level"):
        levelFilesList.append(level.text)

    return levelFilesList


def loadLevelData(level):
    tree = openXmlGetTree(level)
    # We get the "level" tag
    root = tree.getroot()

    '''
    Decided to use a find implementation instead of addressing each tag by
    its position in the xml so that it can be easily extensible, albeit
    at the cost of efficiency.
    Will also trust the xml is well coded
    '''
    # Player position in the scenery
    playerPosition = root.find("playerPosition")
    playerX = int(playerPosition.find("x").text)
    playerY = int(playerPosition.find("y").text)

    # Scenery
    backgroundLayers = []
    scenery = root.find("scenery")
    #file = scenery.find("file").text
    background = scenery.find("background")
    if background is not None:
        for layer in background.iter("layer"):
            file = layer.find("file").text
            parallaxValueX = float(layer.find("parallaxValueX").text)
            parallaxValueY = float(layer.find("parallaxValueY").text)
            scaleX=int(layer.find("scaleX").text)
            scaleY=int(layer.find("scaleY").text)
            backgroundLayers.append((file,parallaxValueX,parallaxValueY,scaleX,scaleY))

    foregroundLayers=[]
    foreground = scenery.find("foreground")
    if foreground is not None:
        for layer in foreground.iter("layer"):
            file = layer.find("file").text
            parallaxValueX = float(layer.find("parallaxValueX").text)
            parallaxValueY = float(layer.find("parallaxValueY").text)
            scaleX=int(layer.find("scaleX").text)
            scaleY=int(layer.find("scaleY").text)
            foregroundLayers.append((file,parallaxValueX,parallaxValueY,scaleX,scaleY))

    # Scale = 0 if no scaling needed
    scaleX = int(scenery.find("scaleX").text)
    scaleY = int(scenery.find("scaleY").text)
    # window size
    windowWidth = int(scenery.find("windowWidth").text)
    windowHeight = int(scenery.find("windowHeight").text)
    # Minimum position of the player in the map
    leftMin = int(scenery.find("leftMin").text)
    topMin = int(scenery.find("topMin").text)
    # Background color
    backgroundColor = scenery.find("backgroundColor")
    red = int(backgroundColor.find("r").text)
    green = int(backgroundColor.find("g").text)
    blue = int(backgroundColor.find("b").text)
    subImagePosition = calculateInitialWindow(playerX, playerY,
                                                    windowHeight, windowWidth,
                                                    scaleY, scaleX)
    sceneryObj = SceneryClass(backgroundLayers,foregroundLayers, scaleX, scaleY, windowWidth, windowHeight,
                              leftMin, topMin, red, green, blue, subImagePosition)




    """
     This is the (0,0) of the window of the game in the background image
     Positions in the XML are based on their distance to the (0,0) of the
     background images, we need to convert this position to the window position
     by substracting this position from the (0,0) of the window
    """
    (winImageX, winImageY) = subImagePosition

    # Player position -> recalculated
    realPlayerPosition = (playerX,playerY)
    playerX = playerX - winImageX
    playerY = playerY - winImageY

    # Platforms
    platforms = root.find("platforms")
    platformList = []
    for platform in platforms.iter("platform"):
        # Id has only informative use
        id = platform.find("id").text
        left = int(platform.find("left").text) - winImageX
        top = int(platform.find("top").text) - winImageY
        width = int(platform.find("width").text)
        height = int(platform.find("height").text)

        platformList.append(Platform(pygame.Rect(left,top,width,height)))

    # Flag area of influence
    flagArea = root.find("flag")
    realFlagPos = (0,0)
    if flagArea is not None:
        left = int(flagArea.find("left").text) - winImageX
        top = int(flagArea.find("top").text) - winImageY
        width = int(flagArea.find("width").text)
        height = int(flagArea.find("height").text)
        realFlagPos = (left,top+height)

        flagArea = FlagArea(pygame.Rect(left, top, width, height))


    # Images on the front
    frontImages = root.find("frontImages")
    frontImagesList = []
    if frontImages is not None:
        for frontImage in frontImages.iter("frontImage"):
            file = frontImage.find("file").text
            # Scales and placements in the case we want to use the image
            # in various points
            scaleAndPlacements = frontImage.find("scaleAndPlacements")
            scaleAndPlacementList = []
            for scaleAndPlacement in scaleAndPlacements.iter("scaleAndPlacement"):
                # Scale = 0 if no scaling needed
                scaleX = int(scaleAndPlacement.find("scaleX").text)
                scaleY = int(scaleAndPlacement.find("scaleY").text)
                # Position of the image in the scenery
                x = int(scaleAndPlacement.find("x").text) - winImageX
                y = int(scaleAndPlacement.find("y").text) -winImageY
                scaleAndPlacementList.append(ScaleAndPlacementClass(scaleX, scaleY, x, y))
            frontImagesList.append(FrontImagesClass(file, scaleAndPlacementList))

    # Animations on the front
    frontAnimations = root.find("frontAnimations")
    frontAnimationsList = []
    if frontAnimations is not None:
        for frontAnimation in frontAnimations.iter("frontAnimation"):
            framesList = []
            frames = frontAnimation.find("frames")
            for frame in frames.iter("frame"):
                file = frame.find("file").text
                milis = float(frame.find("milis").text)
                framesList.append((file, milis))
            # Scales and placements in the case we want to use the animation
            # in various points
            scaleAndPlacements = frontAnimation.find("scaleAndPlacements")
            scaleAndPlacementList = []
            for scaleAndPlacement in scaleAndPlacements.iter("scaleAndPlacement"):
                # Scale = 0 if no scaling needed
                scaleX = int(scaleAndPlacement.find("scaleX").text)
                scaleY = int(scaleAndPlacement.find("scaleY").text)
                # Position of the animation in the scenery
                x = int(scaleAndPlacement.find("x").text) - winImageX
                y = int(scaleAndPlacement.find("y").text) - winImageY
                scaleAndPlacementList.append(ScaleAndPlacementClass(scaleX, scaleY, x, y))
            frontAnimationsList.append(AnimationClass(framesList, scaleAndPlacementList))


    # Animations on the back
    backAnimations = root.find("backAnimations")
    backAnimationsList = []
    if backAnimations is not None:
        for backAnimation in backAnimations.iter("backAnimation"):
            framesList = []
            frames = backAnimation.find("frames")
            for frame in frames.iter("frame"):
                file = frame.find("file").text
                milis = float(frame.find("milis").text)
                framesList.append((file, milis))
            # Scales and placements in the case we want to use the animation
            # in various points
            scaleAndPlacements = backAnimation.find("scaleAndPlacements")
            scaleAndPlacementList = []
            for scaleAndPlacement in scaleAndPlacements.iter("scaleAndPlacement"):
                # Scale = 0 if no scaling needed
                scaleX = int(scaleAndPlacement.find("scaleX").text)
                scaleY = int(scaleAndPlacement.find("scaleY").text)
                # Position of the animation in the scenery
                x = int(scaleAndPlacement.find("x").text) - winImageX
                y = int(scaleAndPlacement.find("y").text) - winImageY
                scaleAndPlacementList.append(ScaleAndPlacementClass(scaleX, scaleY, x, y))
            backAnimationsList.append(AnimationClass(framesList, scaleAndPlacementList))

    # List of enemies that can spawn in this level
    enemies = root.find("enemies")
    enemyList = []
    if enemies is not None:
        for enemy in enemies.iter("enemy"):
            enemyList.append(enemy.text)

    # SpawnPoints
    spawnPoints = root.find("spawnPoints")
    spawnPointList = []
    if spawnPoints is not None:
        for spawnPoint in spawnPoints.iter("spawnPoint"):
            id = int(spawnPoint.find("id").text)
            # SpawnPoints position on the map
            x = int(spawnPoint.find("x").text) - winImageX
            y = int(spawnPoint.find("y").text) - winImageY
            # Number of enemies
            enemiesNumber = int(spawnPoint.find("enemiesNumber").text)
            spawnPointList.append(SpawnPointClass(id, x, y, enemiesNumber))

    # Boss if there is any
    bosses = root.find("bosses")
    bossList = []
    if bosses is not None:
        for boss in bosses.iter("boss"):
            id = boss.find("id").text
            x = int(boss.find("x").text) - winImageX
            y = int(boss.find("y").text) - winImageY
            bossList.append(BossInfo(id, x, y))

    # Stage title and description
    stageInfoXml = root.find("stageInfo")
    title = stageInfoXml.find("title").text
    description = stageInfoXml.find("description").text
    stageInfo = StageInfo(title, description)

    # Stage intro stories
    stageIntroStory = root.find("stageIntroStory")
    stageIntroStoryList = []
    if stageIntroStory is not None:
        for story in stageIntroStory.iter("story"):
            directory = story.find("directory").text
            file = story.find("file").text
            left = int(story.find("left").text)
            top = int(story.find("top").text)
            width = int(story.find("width").text)
            height = int(story.find("height").text)
            stageIntroStoryList.append(IntroAndOutroStory(directory, file, left, top, width, height))

    # Stage outro stories
    stageOutroStory = root.find("stageOutroStory")
    stageOutroStoryList = []
    if stageOutroStory is not None:
        for story in stageOutroStory.iter("story"):
            directory = story.find("directory").text
            file = story.find("file").text
            left = int(story.find("left").text)
            top = int(story.find("top").text)
            width = int(story.find("width").text)
            height = int(story.find("height").text)
            stageOutroStoryList.append(IntroAndOutroStory(directory, file, left, top, width, height))

    # Stage death stories
    stageDeathStory = root.find("stageDeathStory")
    stageDeathStoryList = []
    if stageDeathStory is not None:
        for story in stageDeathStory.iter("story"):
            directory = story.find("directory").text
            file = story.find("file").text
            left = int(story.find("left").text)
            top = int(story.find("top").text)
            width = int(story.find("width").text)
            height = int(story.find("height").text)
            stageDeathStoryList.append(IntroAndOutroStory(directory, file, left, top, width, height))

    # Music file
    musicFile = root.find("musicFile").text
    musicFile = os.path.join("musicAndSounds", musicFile)

    return sceneryObj, frontImagesList, frontAnimationsList, backAnimationsList,\
           platformList, flagArea, realFlagPos, realPlayerPosition, playerX, playerY, spawnPointList, \
           enemyList, bossList, stageInfo, stageIntroStoryList,\
           stageOutroStoryList, stageDeathStoryList, musicFile

class StageInfo:
    def __init__(self, title, description):
        self.title = title
        self.description = description

class BossInfo:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

class EnemyInSpawnPoint:
    def __init__(self, id, spawnFrecuency):
        self.id = id
        self.spawnFrecuency = spawnFrecuency

class SpawnPointClass:
    def __init__(self, id, x, y, enemiesNumber):
        self.id = id
        self.x = x
        self.y = y
        self.enemiesNumber = enemiesNumber

class SceneryClass:
    def __init__(self, backgroundLayers,foregroundLayers, scaleX, scaleY, windowWidth, windowHeight,
                 leftMin, topMin, red, green, blue, subImagePosition):
        self.backgroundLayers = backgroundLayers
        self.foregroundLayers=foregroundLayers
        self.scaleX = scaleX
        self.scaleY = scaleY
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.leftMin = leftMin
        self.topMin = topMin
        self.red = red
        self.green = green
        self.blue = blue
        self.subImagePosition = subImagePosition

class FrontImagesClass:
    def __init__(self, file, scaleAndPlacementList):
        self.file = file
        self.scaleAndPlacementList = scaleAndPlacementList

class AnimationClass:
    def __init__(self, frameList, scaleAndPlacementList):
        self.frameList = frameList
        self.scaleAndPlacementList = scaleAndPlacementList

class ScaleAndPlacementClass:
    def __init__(self, scaleX, scaleY, x, y):
        self.scaleX = scaleX
        self.scaleY = scaleY
        self.x = x
        self.y = y

class IntroAndOutroStory:
    def __init__(self, directory, file, left, top, width, height):
        if directory == " ":
            self.file = file
        else:
            self.file = os.path.join(directory, file)
        self.left = left
        self.top = top
        self.width = width
        self.height = height

# Calculates initial window screen using the player position
def calculateInitialWindow(posx, posy, winHeight, winWidth, imHeight, imWidth):
    # Left distance
    distanceX1 = posx
    # Right Distance
    distanceX2 = imWidth - posx
    # Top distance
    distanceY1 = posy
    # Bottom distance
    distanceY2 = imHeight - posy

    mediumWindowWidth = winWidth / 2
    mediumWindowHeigth = winHeight / 2

    # If left distance is bigger than middle window
    if distanceX1 > mediumWindowWidth:
        # If right distance is bigger than middle window
        if distanceX2 > mediumWindowWidth:
            # Set the window x in the middle of the player
            x = distanceX1 - mediumWindowWidth
        else:
            # Set player x in the most right window possible
            x = imWidth - winWidth
    else:
        # Set player x in the most left window possible
        x = 0

    # If top distance is bigger than middle window
    if distanceY1 > mediumWindowHeigth:
        # If bottom distance is bigger than middle window
        if distanceY2 > mediumWindowHeigth:
            # Set the window y in the middle of the player
            y = distanceY1 - mediumWindowHeigth
        else:
            # Set player y in the most right window possible
            y = imHeight - winHeight
    else:
        # Set player y in the most left window possible
        y = 0
    return (x, y)