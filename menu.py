import pygame
import sys
import time
import pygame_menu
import constants
import puzzle_logic
import bfs_solver
import puzzle_drawing

pygame.init()
surface = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Puzzle-8")

constants.FONT_TITLE = pygame.font.Font(None, 72)
constants.FONT_MENU = pygame.font.Font(None, 50)
constants.FONT_PUZZLE = pygame.font.Font(None, 60)
constants.FONT_INFO = pygame.font.Font(None, 36)

current_game_state = constants.GAME_STATE_MENU

initial_puzzle_state = None
solution_path = None
start_time = None
elapsed_time = 0
current_algorithm_name = None

solution_states = []
current_solution_step_index = 0
last_step_time = 0
solving_computation_done = False

def start_bfs_action():
    global current_game_state, current_algorithm_name, initial_puzzle_state, solution_path, solution_states, current_solution_step_index, solving_computation_done
    current_game_state = constants.GAME_STATE_SOLVING
    current_algorithm_name = 'Busqueda No-Informada (BFS)'
    initial_puzzle_state = puzzle_logic.generate_solvable_state(num_shuffles=80)
    solution_path = None
    solution_states = []
    current_solution_step_index = 0
    solving_computation_done = False
    print(f"Preparando para resolver con {current_algorithm_name}...")

def start_informed_search_action():
    global current_game_state, current_algorithm_name, initial_puzzle_state, solution_path, solution_states, current_solution_step_index, solving_computation_done
    current_game_state = constants.GAME_STATE_SOLVING
    current_algorithm_name = 'Busqueda Informada (A*)'
    initial_puzzle_state = puzzle_logic.generate_solvable_state(num_shuffles=80)
    solution_path = None
    solution_states = []
    current_solution_step_index = 0
    solving_computation_done = False
    print(f"Preparando para resolver con {current_algorithm_name}...")

def exit_game_action():
    global running
    running = False

menu = pygame_menu.Menu('Puzzle-8', constants.SCREEN_WIDTH * 0.8, constants.SCREEN_HEIGHT * 0.6,
                       theme=pygame_menu.themes.THEME_BLUE)

menu.add.button('Busqueda No-Informada (BFS)', start_bfs_action)
menu.add.button('Busqueda Informada (A*)', start_informed_search_action)
menu.add.button('Salir', exit_game_action)

running = True
clock = pygame.time.Clock()

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if current_game_state in [constants.GAME_STATE_SHOWING_SOLUTION, constants.GAME_STATE_FINISHED]:
                button_w = 250
                button_h = 60
                button_x = (constants.SCREEN_WIDTH - button_w) // 2
                button_y = constants.SCREEN_HEIGHT - 180
                button_rect = pygame.Rect(button_x, button_y, button_w, button_h)
                if button_rect.collidepoint(event.pos):
                    current_game_state = constants.GAME_STATE_MENU
                    initial_puzzle_state = None
                    solution_path = None
                    solution_states = []
                    current_solution_step_index = 0
                    elapsed_time = 0
                    current_algorithm_name = None
                    solving_computation_done = False

    surface.fill(constants.WHITE)

    if current_game_state == constants.GAME_STATE_MENU:
        if not menu.is_enabled():
            menu.enable()
        menu.mainloop(surface, disable_loop=True, events=events)

    elif current_game_state == constants.GAME_STATE_SOLVING:
        if menu.is_enabled():
            menu.disable()

        puzzle_drawing.draw_text(surface, f"{current_algorithm_name}...", constants.FONT_TITLE, constants.BLACK, constants.SCREEN_WIDTH // 2, 80, center=True)

        if initial_puzzle_state:
            puzzle_drawing.draw_board(surface, initial_puzzle_state)

        puzzle_drawing.draw_text(surface, "Calculando...", constants.FONT_INFO, constants.BLACK, constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT - 80, center=True)

        if not solving_computation_done:
            solve_start_time = time.time()

            if current_algorithm_name == 'Busqueda No-Informada (BFS)':
                print("Iniciando calculo de BFS...")
                solution_path, expanded_nodes = bfs_solver.solve_bfs(initial_puzzle_state)
            elif current_algorithm_name == 'Busqueda Informada (A*)':
                print("Iniciando calculo de A*...")
                solution_path, expanded_nodes = puzzle_logic.a_star_search(initial_puzzle_state, constants.GOAL_STATE_TUPLE)
            else:
                print("Error: Algoritmo no reconocido.")
                current_game_state = constants.GAME_STATE_FINISHED
                continue

            elapsed_time = time.time() - solve_start_time
            solving_computation_done = True

            # Mostrar solo el total de nodos expandidos
            print(f"Nodos expandidos: {len(expanded_nodes)}")

            if solution_path is not None:
                print(f"\nSolucion encontrada en {len(solution_path)} pasos.")
                print(f"Tiempo de calculo: {puzzle_drawing.format_time(elapsed_time)}")
                current_animated_state = initial_puzzle_state
                solution_states.append(current_animated_state)
                temp_state_tuple = initial_puzzle_state
                for move in solution_path:
                    temp_state_tuple = puzzle_drawing.get_next_state_from_move(temp_state_tuple, move)
                    solution_states.append(temp_state_tuple)
                current_solution_step_index = 0
                last_step_time = time.time()
                current_game_state = constants.GAME_STATE_SHOWING_SOLUTION
            else:
                print("Error: No se encontró solucion")
                current_game_state = constants.GAME_STATE_FINISHED


    elif current_game_state == constants.GAME_STATE_SHOWING_SOLUTION:
        if menu.is_enabled():
            menu.disable()

        puzzle_drawing.draw_text(surface, f"{current_algorithm_name}", constants.FONT_TITLE, constants.BLACK, constants.SCREEN_WIDTH // 2, 80, center=True)
        puzzle_drawing.draw_text(surface, f"Tiempo: {puzzle_drawing.format_time(elapsed_time)}", constants.FONT_INFO, constants.BLACK, constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT - 100, center=True)
        puzzle_drawing.draw_text(surface, f"Pasos: {len(solution_path) if solution_path else 0}", constants.FONT_INFO, constants.BLACK, constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT - 60, center=True)

        if solution_states:
            puzzle_drawing.draw_board(surface, solution_states[current_solution_step_index])
            if solution_path and current_solution_step_index < len(solution_path):
                step_text = f"Paso {current_solution_step_index + 1} de {len(solution_path)}"
                move_text = f"Mover 0: {solution_path[current_solution_step_index]}"
            elif solution_path and current_solution_step_index == len(solution_path):
                step_text = f"Paso {current_solution_step_index} de {len(solution_path)}"
                move_text = "Resuelto"
            else:
                step_text = "Paso 0"
                move_text = "Estado Inicial"

            puzzle_drawing.draw_text(surface, step_text, constants.FONT_INFO, constants.BLACK, constants.BOARD_POS_X, constants.BOARD_POS_Y - 50)
            puzzle_drawing.draw_text(surface, move_text, constants.FONT_INFO, constants.BLACK, constants.BOARD_POS_X, constants.BOARD_POS_Y - 20)

            current_time = time.time()
            if current_time - last_step_time > constants.ANIMATION_DELAY:
                if current_solution_step_index < len(solution_states) - 1:
                    current_solution_step_index += 1
                    last_step_time = current_time
                else:
                    current_game_state = constants.GAME_STATE_FINISHED

        button_w = 250
        button_h = 60
        button_x = (constants.SCREEN_WIDTH - button_w) // 2
        button_y = constants.SCREEN_HEIGHT - 180

    elif current_game_state == constants.GAME_STATE_FINISHED:
        if menu.is_enabled():
            menu.disable()

        puzzle_drawing.draw_text(surface, "Solución Completa", constants.FONT_TITLE, constants.BLACK, constants.SCREEN_WIDTH // 2, 80, center=True)
        puzzle_drawing.draw_board(surface, constants.GOAL_STATE_TUPLE)
        puzzle_drawing.draw_text(surface, f"Tiempo ({current_algorithm_name}): {puzzle_drawing.format_time(elapsed_time)}", constants.FONT_INFO, constants.BLACK, constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT - 100, center=True)
        puzzle_drawing.draw_text(surface, f"Pasos: {len(solution_path) if solution_path else 0}", constants.FONT_INFO, constants.BLACK, constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT - 60, center=True)

        button_w = 250
        button_h = 60
        button_x = (constants.SCREEN_WIDTH - button_w) // 2
        button_y = constants.SCREEN_HEIGHT - 180

        if current_game_state in [constants.GAME_STATE_SHOWING_SOLUTION, constants.GAME_STATE_FINISHED]:
            button_w = 250
            button_h = 60
            button_x = (constants.SCREEN_WIDTH - button_w) // 2
            button_y = constants.SCREEN_HEIGHT - 180
            puzzle_drawing.draw_button(surface, "Volver al Menu", button_x, button_y, button_w, button_h, constants.BLUE, constants.GREEN)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
