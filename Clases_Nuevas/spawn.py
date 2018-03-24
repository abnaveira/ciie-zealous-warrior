# -*- encoding: utf-8 -*-

from characters import *
import random
import time

# -------------------------------------------------
# Class spawn with its methods to create spawn points and to spawn enemies

class Spawn:

    def __init__(self, spawnPoint):
        # Coordinates of the spawn point
        self.x = spawnPoint.x
        self.y = spawnPoint.y
        # Frequency to spawn
        self.frequency = random.randint(0, 1000)
        # List of enemies to spawn
        self.listEnemies = []

        self.lastSpawn = 0

        # Add enemies to list
        self.add_enemies(spawnPoint.enemies)

    # Add enemies to be spawned
    def add_enemies(self, number):
        move = 0
        for i in range(0, number):
            probability = random.randint(0, 1000)
            """if probability <= 200:
                enemy = Zebesian()
            elif probability <= 400:
                enemy = MeltyZombie()
            elif probability <= 600:
                enemy = Imp()
            elif probability <= 800:
                enemy = Skeleton()
            else:
                enemy = AxeKnight()"""

            enemy = Zebesian() # DESCOMENTAR LO ANTERIOR Y COMENTAR ESTA LINEA PARA QUE SALGAN TODOS LOS TIPOS
            enemy.setPosition((self.x + move, self.y))
            self.listEnemies.append(enemy)
            move += 100

    # Spawn an enemy
    def spawn_enemy(self, phase):
        enemy = self.listEnemies[0]
        phase.enemiesGroup.add(enemy)
        phase.dinamicSpritesGroup.add(enemy)
        self.listEnemies.remove(enemy)

    # Decide to spawn a new enemy or not
    def spawn(self, phase):
        # If list of enemies not empty
        if self.listEnemies:
            millis = int(round(time.time() * 1000))
            # Always one spawned enemy (at least)
            if self.lastSpawn == 0:
                # First enemy
                self.spawn_enemy(phase)
            else:
                timePassed = millis - self.lastSpawn
                if timePassed < 2000:
                    return
                elif timePassed < 5000:
                    f = random.randint(0, 1000)
                    if f >= self.frequency:
                        self.spawn_enemy(phase)
                    else:
                        return
                else:
                    self.spawn_enemy(phase)
            self.lastSpawn = millis

    # Remove the enemies that have not been spawned yet
    def clear(self):
        self.listEnemies = []
