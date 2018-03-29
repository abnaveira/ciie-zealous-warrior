# -*- encoding: utf-8 -*-

from characters import *
import random
import time

# -------------------------------------------------
# Class spawn with its methods to create spawn points and to spawn enemies

class Spawn:

    def __init__(self, spawnPoint, enemyList):

        # Coordinates of the spawn point
        self.x = spawnPoint.x
        self.y = spawnPoint.y
        # Frequency to spawn
        self.frequency = random.randint(0, 1000)
        #-------------
        # Use enemyList with the method "getNpcFromName(name)"
        # This way you can transform strings into instances of said enemy
        self.enemyTypes = enemyList
        #-------------
        # List of enemies to spawn
        self.listEnemies = []
        # Time of the last spawn
        self.lastSpawn = 0
        # Add enemies to list
        self.add_enemies(spawnPoint.enemiesNumber)

    # Add enemies to be spawned
    def add_enemies(self, number):
        move = 0
        for i in range(0, number):
            probability = random.randint(0, len(self.enemyTypes) - 1)
            enemy = self.getNpcFromName(self.enemyTypes[probability])
            enemy.setPosition((self.x + move, self.y))
            self.listEnemies.append(enemy)
            #move += 50

    # Spawn an enemy
    def spawn_enemy(self, phase, player):
        enemy = self.listEnemies[0]
        enemy.setScreenPosition(player.scroll)
        phase.enemiesGroup.add(enemy)
        self.listEnemies.remove(enemy)

    # Decide to spawn a new enemy or not
    def spawn(self, phase, player):
        millis = int(round(time.time() * 1000))
        timePassed = millis - self.lastSpawn
        # If list of enemies not empty
        if self.listEnemies:
            if phase.flagRaised:
                if timePassed >= 3000:
                    self.spawn_enemy(phase, player)
                    self.lastSpawn = millis
            else:
                # Always one spawned enemy (at least)
                if self.lastSpawn == 0:
                     # First enemy
                    self.spawn_enemy(phase, player)
                else:
                    if timePassed < 2000:
                        return
                    elif timePassed < 5000:
                        f = random.randint(0, 1000)
                        if f >= self.frequency:
                            self.spawn_enemy(phase, player)
                        else:
                            return
                    else:
                        self.spawn_enemy(phase, player)
                self.lastSpawn = millis

    # Remove the enemies that have not been spawned yet
    def clear(self):
        self.listEnemies = []

    # Return NPC instance from name, or none if it is not recognized
    def getNpcFromName(self, name):
        if name == 'Skeleton':
            return Skeleton()
        elif name == 'Zombie':
            return Zombie()
        elif name == 'BarrelSkeleton':
            return BarrelSkeleton()
        elif name == 'CheetahSkeleton':
            return CheetahSkeleton
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


def getBossFromName(name):
    if name == 'Boss':
        return Boss()
    else:
        return None
