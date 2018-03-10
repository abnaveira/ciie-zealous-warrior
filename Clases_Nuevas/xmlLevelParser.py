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
    scaleX = int(scenery.find("scaleX").text)
    scaleY = int(scenery.find("scaleY").text)
    windowWidth = int(scenery.find("windowWidth").text)
    windowHeight = int(scenery.find("windowHeight").text)
    leftMin = int(scenery.find("leftMin").text)
    topMin = int(scenery.find("topMin").text)
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
        #el id no le doy uso por ahora
        id = platform.find("id").text
        top = int(platform.find("top").text)
        left = int(platform.find("left").text)
        width = int(platform.find("width").text)
        height = int(platform.find("height").text)

        platformList.append(fase.Plataforma(pygame.Rect(top,left,width,height)))

    #Player position
    playerPosition = root.find("playerPosition")
    playerX = int(playerPosition.find("x").text)
    playerY = int(playerPosition.find("y").text)

    #SpawnPoints
    spawnPoints = root.find("spawnPoints")
    spawnPointList = []
    for spawnPoint in spawnPoints.iter("spawnPoint"):
        # el id no le doy uso por ahora
        id = spawnPoint.find("id").text
        enemies = spawnPoint.find("enemies")
        enemyList = []
        for enemy in enemies.iter("enemy"):
            enemyId = enemy.find("id").text
            spawnFrecuency = enemy.find("spawnFrecuency").text
            enemyList.append(enemyInSpawnPoint(enemyId,spawnFrecuency))
        x = int(spawnPoint.find("x").text)
        y = int(spawnPoint.find("y").text)
        spawnPointList.append(spawnPointClass(enemyId, enemyList, x, y))

    return sceneryObj, platformList, playerX, playerY, spawnPointList

def main():
    loadLevelData("level1Xml.xml")


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



if __name__ == "__main__":
    main()