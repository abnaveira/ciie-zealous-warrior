# -*- coding: utf-8 -*-

# Importar modulos
from director import Director
from phase import PhaseScene


if __name__ == '__main__':

    # Creamos el director
    director = Director()
    # Creamos la escena con el menu
    escena = PhaseScene(director, "level1_CAVE.xml")
    # Le decimos al director que apile esta escena
    director.apilarEscena(escena)
    # Y ejecutamos el juego
    director.ejecutar()
