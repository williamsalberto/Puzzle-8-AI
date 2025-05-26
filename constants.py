import pygame

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0) 

#Dimensiones de la ventana
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800 

# Fuentes (inicializadas en el archivo principal)
FONT_TITLE = None
FONT_MENU = None
FONT_PUZZLE = None
FONT_INFO = None

#Dimensiones del tablero y fichas
BOARD_SIZE = 3
TILE_SIZE = 150
BOARD_WIDTH = BOARD_SIZE * TILE_SIZE
BOARD_HEIGHT = BOARD_SIZE * TILE_SIZE
#Posicion del tablero en la pantalla
BOARD_POS_X = (SCREEN_WIDTH - BOARD_WIDTH) // 2
BOARD_POS_Y = 200 # Ajustado

#Estado meta del puzzle
GOAL_STATE_TUPLE = ((1, 2, 3), (8, 0, 4), (7, 6, 5))

#Mapa de posicion objetivo para heurísticas
GOAL_POSITIONS = {
    1: (0, 0), 2: (0, 1), 3: (0, 2),
    4: (1, 0), 5: (1, 1), 6: (1, 2),
    7: (2, 0), 8: (2, 1), 0: (2, 2)
}

# Estados del juego
GAME_STATE_MENU = 0
GAME_STATE_SOLVING = 1
GAME_STATE_SHOWING_SOLUTION = 2
GAME_STATE_FINISHED = 3

#Animacion
ANIMATION_DELAY = 0.6 #segundos
