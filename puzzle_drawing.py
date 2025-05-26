import pygame
import constants
import puzzle_logic #Necesario para find_blank 

# Estas fuentes se inicializarán en el archivo principal y se asignarán a constants
# Se accede a ellas a través de constants

def draw_board(surface, state_tuple):
    state_list = puzzle_logic.tuple_to_list(state_tuple)
    for r in range(constants.BOARD_SIZE):
        for c in range(constants.BOARD_SIZE):
            tile_value = state_list[r][c]
            x = constants.BOARD_POS_X + c * constants.TILE_SIZE
            y = constants.BOARD_POS_Y + r * constants.TILE_SIZE

            # Dibujar el cuadro de la ficha (borde)
            pygame.draw.rect(surface, constants.DARK_GRAY, (x, y, constants.TILE_SIZE, constants.TILE_SIZE), 2)

            # Dibujar el interior de la ficha (si no es la vacía)
            if tile_value != 0:
                pygame.draw.rect(surface, constants.GRAY, (x + 2, y + 2, constants.TILE_SIZE - 4, constants.TILE_SIZE - 4))
                # Dibujar el número en la ficha
                text_surface = constants.FONT_PUZZLE.render(str(tile_value), True, constants.BLACK)
                text_rect = text_surface.get_rect(center=(x + constants.TILE_SIZE // 2, y + constants.TILE_SIZE // 2))
                surface.blit(text_surface, text_rect)
            else:
                 # Dibujar el espacio vacío
                pygame.draw.rect(surface, constants.BLACK, (x + 2, y + 2, constants.TILE_SIZE - 4, constants.TILE_SIZE - 4))

def draw_button(surface, text, x, y, w, h, color, hover_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    button_rect = pygame.Rect(x, y, w, h)

    if button_rect.collidepoint(mouse):
        pygame.draw.rect(surface, hover_color, button_rect)
        if click[0] == 1:
            return True # Indica que el boton fue clickeado
    else:
        pygame.draw.rect(surface, color, button_rect)

    # Dibujar texto centrado en el boton
    text_surface = constants.FONT_MENU.render(text, True, constants.BLACK)
    text_rect = text_surface.get_rect(center=(x + w // 2, y + h // 2))
    surface.blit(text_surface, text_rect)
    return False # Indica que el boton no fue clickeado en este frame

def draw_text(surface, text, font, color, x, y, center=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)
    return text_rect # Devuelve el rectangulo para posible posicionamiento

def format_time(elapsed_time):
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    milliseconds = int((elapsed_time * 1000) % 1000)
    return f"{minutes:02}:{seconds:02}.{milliseconds:03}"

# Función para calcular el siguiente estado dada un estado y un movimiento (para la animación)
def get_next_state_from_move(current_state_tuple, move_name):
    state_list = puzzle_logic.tuple_to_list(current_state_tuple)
    r_blank, c_blank = puzzle_logic.find_blank(state_list)
    new_r, new_c = -1, -1

    # Determinar la nueva posición del 0 basada en el nombre del movimiento
    if move_name == 'arriba': new_r, new_c = r_blank - 1, c_blank
    elif move_name == 'abajo': new_r, new_c = r_blank + 1, c_blank
    elif move_name == 'izq': new_r, new_c = r_blank, c_blank - 1
    elif move_name == 'der': new_r, new_c = r_blank, c_blank + 1

    if 0 <= new_r < constants.BOARD_SIZE and 0 <= new_c < constants.BOARD_SIZE:
         # Intercambiar la casilla vacía (originalmente en r_blank, c_blank)
         # con la casilla vecina que se mueve (en new_r, new_c)
         state_list[r_blank][c_blank], state_list[new_r][new_c] = \
              state_list[new_r][new_c], state_list[r_blank][c_blank]
         return puzzle_logic.list_to_tuple(state_list)
    else:
        # Esto no debería pasar si el camino es válido, pero por seguridad
        print(f"Error: Movimiento '{move_name}' inválido en la animación para el estado {current_state_tuple}.")
        return current_state_tuple # Retorna el estado actual sin cambios
