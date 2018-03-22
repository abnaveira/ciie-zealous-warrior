

# This structure should serve to centralise all sprite groups and pass them as arguments.
class SpriteStructure():

    def __init__(self, player, enemyGroup, platformGroup, projectileGroup, standingGroup, hudGroup):
        self.player = player
        self.enemyGroup = enemyGroup
        self.platformGroup = platformGroup
        self.projectileGroup = projectileGroup
        self.standingGroup = standingGroup
        self.hudGroup = hudGroup