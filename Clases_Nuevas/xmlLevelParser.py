#imports

import sys
import os
import xml.etree.ElementTree as ET
import fase
import pygame

def openXmlGetTree(xmlFileName):
    # Get the directory where this file is
    directory = sys.path[0]

    # Append the directory where levels are located
    # xmlFile = os.path.join(directory, "Carpeta donde Estan los niveles")

    # Append the level we want to open
    xmlFile = os.path.join(directory, xmlFileName)

    # Parse the file and get the tree
    return ET.parse(xmlFile)


def loadLevelData(level):
    tree = openXmlGetTree(level)
    #We get the "level" tag
    root = tree.getroot()

    '''
    Decided to use a find implementation instead of addressing each tag by
    its position in the xml so that it can be easily extensible, albeit
    at the cost of efficiency.
    Will also trust the xml is well coded
    '''
    #Scenery
    scenery = root.find("scenery")
    file = scenery.find("file").text
    #Scale = 0 if no scaling needed
    scaleX = int(scenery.find("scaleX").text)
    scaleY = int(scenery.find("scaleY").text)
    #window size
    windowWidth = int(scenery.find("windowWidth").text)
    windowHeight = int(scenery.find("windowHeight").text)
    #Minimum position of the player in the map
    leftMin = int(scenery.find("leftMin").text)
    topMin = int(scenery.find("topMin").text)
    #Background color
    backgroundColor = scenery.find("backgroundColor")
    red = int(backgroundColor.find("r").text)
    green = int(backgroundColor.find("g").text)
    blue = int(backgroundColor.find("b").text)
    sceneryObj = sceneryClass(file, scaleX, scaleY, windowWidth, windowHeight,
                              leftMin, topMin, red, green, blue)

    #Platforms
    platforms = root.find("platforms")
    platformList = []
    for platform in platforms.iter("platform"):
        #Id has only informative use
        id = platform.find("id").text
        top = int(platform.find("top").text)
        left = int(platform.find("left").text)
        width = int(platform.find("width").text)
        height = int(platform.find("height").text)

        platformList.append(fase.Plataforma(pygame.Rect(top,left,width,height)))

    #Images on the front
    frontImages = root.find("frontImages")
    frontImagesList = []
    if (frontImages != None):
        for frontImage in frontImages.iter("frontImage"):
            file = frontImage.find("file").text
            # Scale = 0 if no scaling needed
            scaleX = int(frontImage.find("scaleX").text)
            scaleY = int(frontImage.find("scaleY").text)
            #Position of the image in the scenery
            x = int(frontImage.find("x").text)
            y = int(frontImage.find("y").text)
            frontImagesList.append(frontImagesClass(file, scaleX, scaleY, x, y))

    #Animations on the front
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
            # Scale = 0 if no scaling needed
            scaleX = int(frontAnimation.find("scaleX").text)
            scaleY = int(frontAnimation.find("scaleY").text)
            # Position of the animation in the scenery
            x = int(frontAnimation.find("x").text)
            y = int(frontAnimation.find("y").text)
            frontAnimationsList.append(animationClass("front", framesList, scaleX, scaleY, x, y))

    #Animations on the back
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
            # Scale = 0 if no scaling needed
            scaleX = int(backAnimation.find("scaleX").text)
            scaleY = int(backAnimation.find("scaleY").text)
            # Position of the animation in the scenery
            x = int(backAnimation.find("x").text)
            y = int(backAnimation.find("y").text)
            frontAnimationsList.append(animationClass("front", framesList, scaleX, scaleY, x, y))


    #Player position in the scenery
    playerPosition = root.find("playerPosition")
    playerX = int(playerPosition.find("x").text)
    playerY = int(playerPosition.find("y").text)

    #SpawnPoints
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
            #SpawnPoints position on the map
            x = int(spawnPoint.find("x").text)
            y = int(spawnPoint.find("y").text)
            spawnPointList.append(spawnPointClass(id, enemyList, x, y))

    return sceneryObj, frontImagesList, frontAnimationsList, backAnimationsList,\
           platformList, playerX, playerY, spawnPointList

def main():
    loadLevelData("level1Example.xml")


#Define an enemy parser as well with ids

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
                 leftMin, topMin, red, green, blue):
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

class frontImagesClass:
    def __init__(self, file, scaleX, scaleY, x, y):
        self.file = file
        self.scaleX = scaleX
        self.scaleY = scaleY
        self.x = x
        self.y = y

class animationClass:
    def __init__(self, type, frameList, scaleX, scaleY, x, y):
        #Type can be front or back (if the animation is played in front or on
        #the back of the player
        self.type = type
        self.frameList = frameList
        self.scaleX = scaleX
        self.scaleY = scaleY
        self.x = x
        self.y = y


if __name__ == "__main__":
    main()