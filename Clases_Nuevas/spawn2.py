import random
import copy
from characters import *

MINIMUM_DISTANCE = 250000

class Spawn2():

    def __init__(self, spawnPoint, enemyList):
        self.id = spawnPoint.id
        # Coordinates of the spawn point
        self.x = spawnPoint.x
        self.y = spawnPoint.y
        self.enemyTypes = enemyList


    def spawnEnemy(self, spriteStructure):
        index = random.randint(0, len(self.enemyTypes) - 1)
        enemy = self.getNpcFromName(self.enemyTypes[index])
        enemy.setPosition((self.x, self.y))
        enemy.setScreenPosition(spriteStructure.player.scroll)
        spriteStructure.enemyGroup.add(enemy)

    def isValid(self, spriteStructure):
        distx = self.x - spriteStructure.player.position[0]
        disty = self.y - spriteStructure.player.position[1]
        return (distx * distx + disty * disty) > MINIMUM_DISTANCE

    def getNpcFromName(self, name):
        if name == 'Skeleton':
            return Skeleton()
        elif name == 'Zombie':
            return Zombie()
        elif name == 'BarrelSkeleton':
            return BarrelSkeleton()
        elif name == 'CheetahSkeleton':
            return CheetahSkeleton()
        elif name == 'Zebesian':
            return Zebesian()
        elif name == 'MeltyZombie':
            return MeltyZombie()
        elif name == 'Imp':
            return Imp()
        elif name == 'AxeKnight':
            return AxeKnight()
        else:
            return None