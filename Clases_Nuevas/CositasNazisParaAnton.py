"""Con esto, mi clase de xmlLevelParser (que hay que tocar para meterle el directorio
en el que está mi xml) y la clase animationsPygame, ya puedes cargar animaciones
dinámicamente desde fase
"""

from xmlLevelParser import *
from animationsPygame import *

sceneryObj, frontImagesList, frontAnimationsList, backAnimationsList, \
platformList, playerX, playerY, spawnPointList = loadLevelData("level1Example.xml")

# Animations in the front
for frontAnimation in frontAnimationsList:
    for scaleAndPlacement in frontAnimation.scaleAndPlacementList:
        animation = AnimationFromList(frontAnimation.frameList)
        if ((scaleAndPlacement.scaleX != 0) and (scaleAndPlacement.scaleY != 0)):
            animation.scale((scaleAndPlacement.scaleX, scaleAndPlacement.scaleY))
        animation.positionX = scaleAndPlacement.x
        animation.positionY = scaleAndPlacement.y
        animation.play()
        self.animacionesDelante.append(animation)

# Animations in the back
for backAnimation in backAnimationsList:
    for scaleAndPlacement in backAnimation.scaleAndPlacementList:
        animation = AnimationFromList(backAnimation.frameList)
        if ((scaleAndPlacement.scaleX != 0) and (scaleAndPlacement.scaleY != 0)):
            animation.scale((scaleAndPlacement.scaleX, scaleAndPlacement.scaleY))
        animation.positionX = scaleAndPlacement.x
        animation.positionY = scaleAndPlacement.y
        animation.play()
        self.animacionesDetras.append(animation)