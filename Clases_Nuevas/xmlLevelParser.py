# -*- encoding: utf-8 -*-

import sys
import os
import xml.etree.ElementTree as ET
from miscSprites import *
import pygame

def openXmlGetTree(xmlFileName):
    # Get the directory where this file is
    directory = sys.path[0]

    # Append the directory where levels are located
    #directory = os.path.join(directory, "Clases_Nuevas")

    # Append the level we want to open
    xmlFile = os.path.join(directory, xmlFileName)

    # Parse the file and get the tree
    return ET.parse(xmlFile)


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
    scenery = root.find("scenery")
    file = scenery.find("file").text
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
    sceneryObj = sceneryClass(file, scaleX, scaleY, windowWidth, windowHeight,
                              leftMin, topMin, red, green, blue, subImagePosition)




    """
     This is the (0,0) of the window of the game in the background image
     Positions in the XML are based on their distance to the (0,0) of the
     background images, we need to convert this position to the window position
     by substracting this position from the (0,0) of the window
    """
    (winImageX, winImageY) = subImagePosition

    # Player position -> recalculated
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

    # Images on the front
    frontImages = root.find("frontImages")
    frontImagesList = []
    if (frontImages != None):
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
                scaleAndPlacementList.append(scaleAndPlacementClass(scaleX, scaleY, x, y))
            frontImagesList.append(frontImagesClass(file, scaleAndPlacementList))

    # Animations on the front
    frontAnimations = root.find("frontAnimations")
    frontAnimationsList = []
    if (frontAnimations != None):
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
                scaleAndPlacementList.append(scaleAndPlacementClass(scaleX, scaleY, x, y))
            frontAnimationsList.append(animationClass(framesList, scaleAndPlacementList))

    # Animations on the back
    backAnimations = root.find("backAnimations")
    backAnimationsList = []
    if (backAnimations != None):
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
                scaleAndPlacementList.append(scaleAndPlacementClass(scaleX, scaleY, x, y))
            backAnimationsList.append(animationClass(framesList, scaleAndPlacementList))



    # SpawnPoints
    spawnPoints = root.find("spawnPoints")
    spawnPointList = []
    if (spawnPoints != None):
        for spawnPoint in spawnPoints.iter("spawnPoint"):
            id = spawnPoint.find("id").text
            enemies = spawnPoint.find("enemies")
            enemyList = []
            for enemy in enemies.iter("enemy"):
                enemyId = enemy.find("id").text
                spawnFrecuency = enemy.find("spawnFrecuency").text
                enemyList.append(enemyInSpawnPoint(enemyId,spawnFrecuency))
            # SpawnPoints position on the map
            x = int(spawnPoint.find("x").text) - winImageX
            y = int(spawnPoint.find("y").text) - winImageY
            spawnPointList.append(spawnPointClass(id, enemyList, x, y))

    return sceneryObj, frontImagesList, frontAnimationsList, backAnimationsList,\
           platformList, playerX, playerY, spawnPointList


# TODO: Define an enemy parser as well with ids

class enemyInSpawnPoint:
    def __init__(self, id, spawnFrecuency):
        self.id = id
        self.spawnFrecuency = spawnFrecuency

class spawnPointClass:
    def __init__(self, id, enemyList, x, y):
        self.id = id
        self.enemyList = enemyList
        self.x = x
        self.y = y
        
class sceneryClass:
    def __init__(self, file, scaleX, scaleY, windowWidth, windowHeight,
                 leftMin, topMin, red, green, blue, subImagePosition):
        self.file = file
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

class frontImagesClass:
    def __init__(self, file, scaleAndPlacementList):
        self.file = file
        self.scaleAndPlacementList = scaleAndPlacementList

class animationClass:
    def __init__(self, frameList, scaleAndPlacementList):
        self.frameList = frameList
        self.scaleAndPlacementList = scaleAndPlacementList

class scaleAndPlacementClass:
    def __init__(self, scaleX, scaleY, x, y):
        self.scaleX = scaleX
        self.scaleY = scaleY
        self.x = x
        self.y = y

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
    print(str(x) + ", " + str(y))
    return (x, y)



def main():
    loadLevelData("level1Example.xml")

if __name__ == "__main__":
    calculateInitialWindow(50,450,600,800,1000,3000)