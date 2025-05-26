import random
import constants 
import heapq

#Función para convertir lista a tupla de tuplas 
def list_to_tuple(state_list):
    return tuple(tuple(row) for row in state_list)

#Funcion para convertir tupla de tuplas a lista 2D
def tuple_to_list(state_tuple):
    return [list(row) for row in state_tuple]

#Funcion para encontrar la posición de la casilla vacía (0)
def find_blank(state):
    # Asume que el estado es una lista de listas
    for r in range(constants.BOARD_SIZE):
        for c in range(constants.BOARD_SIZE):
            if state[r][c] == 0:
                return r, c
    return -1, -1 # No debería pasar en un estado válido

#Funcion para obtener los estados vecinos (movimientos válidos)
#Retorna una lista de (estado_vecino_tuple, nombre_del_movimiento)
def get_neighbors(state_tuple):
    state_list = tuple_to_list(state_tuple)
    r_blank, c_blank = find_blank(state_list)
    neighbors = []

    # Posibles movimientos del espacio vacío: (dr, dc) y el nombre del movimiento del 0
    # El nombre del movimiento es la dirección a la que se mueve el 0
    moves = {
        (-1, 0): 'arriba',
        (1, 0): 'abajo',
        (0, -1): 'izq',
        (0, 1): 'der'
    }

    for (dr, dc), move_name in moves.items():
        new_r, new_c = r_blank + dr, c_blank + dc

        #Verificar si el movimiento es válido (dentro del tablero)
        if 0 <= new_r < constants.BOARD_SIZE and 0 <= new_c < constants.BOARD_SIZE:
            #Crear una copia del estado para modificarla
            new_state_list = [list(row) for row in state_list]
            #Intercambiar la casilla vacía con la casilla vecina
            new_state_list[r_blank][c_blank], new_state_list[new_r][new_c] = \
                new_state_list[new_r][new_c], new_state_list[r_blank][c_blank]
            #Agregar el nuevo estado (como tupla) y el movimiento a la lista de vecinos
            neighbors.append((list_to_tuple(new_state_list), move_name))

    return neighbors

# Función para generar un estado inicial solvable aleatorio
def generate_solvable_state(num_shuffles=80):
    current_state_list = tuple_to_list(constants.GOAL_STATE_TUPLE)
    # Realizar un número de movimientos aleatorios válidos desde el estado objetivo
    r_blank, c_blank = find_blank(current_state_list)

    # Definir movimientos como cambios en la posición del 0
    move_deltas = {
        'arriba': (-1, 0), 'abajo': (1, 0), 'izq': (0, -1), 'der': (0, 1)
    }

    for _ in range(num_shuffles):
        possible_swaps = []
        for move_name, (dr, dc) in move_deltas.items():
            new_r, new_c = r_blank + dr, c_blank + dc
            if 0 <= new_r < constants.BOARD_SIZE and 0 <= new_c < constants.BOARD_SIZE:
                 possible_swaps.append((new_r, new_c)) # La celda vecina con la que el 0 puede intercambiarse

        if possible_swaps:
            target_r, target_c = random.choice(possible_swaps)
            # Realizar el intercambio: 0 se mueve a (target_r, target_c)
            current_state_list[r_blank][c_blank], current_state_list[target_r][target_c] = \
                current_state_list[target_r][target_c], current_state_list[r_blank][c_blank]
            # Actualizar la posición del 0 para el próximo movimiento
            r_blank, c_blank = target_r, target_c

    return list_to_tuple(current_state_list)

# Heurística de distancia de Manhattan para A*
def manhattan_distance_heuristic(state_tuple):
    goal_positions = {}  #Diccionario para mapear valor (fila, columna) en el estado objetivo
    for r in range(constants.BOARD_SIZE):
        for c in range(constants.BOARD_SIZE):
            value = constants.GOAL_STATE_TUPLE[r][c]
            goal_positions[value] = (r, c)

    distance = 0
    for r in range(constants.BOARD_SIZE):
        for c in range(constants.BOARD_SIZE):
            value = state_tuple[r][c]
            if value != 0:  # No se cuenta la distancia del espacio vacío
                goal_r, goal_c = goal_positions[value]
                distance += abs(r - goal_r) + abs(c - goal_c)

    return distance

# Algoritmo A* usando la heuristica de distancia Manhattan
def a_star_search(start_state, goal_state):
    frontier = []  # Cola de prioridad: (f_score, g_score, state, path)
    heapq.heappush(frontier, (manhattan_distance_heuristic(start_state), 0, start_state, []))

    explored = set()
    g_scores = {start_state: 0}
    nodos_expandidos = []

    while frontier:
        f, g, current_state, path = heapq.heappop(frontier)

        if current_state == goal_state:
            return path, nodos_expandidos  # Secuencia de movimientos desde el inicio al objetivo

        if current_state in explored:
            continue
        explored.add(current_state)
        nodos_expandidos.append(current_state)

        for neighbor, move in get_neighbors(current_state):
            tentative_g = g + 1

            if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                g_scores[neighbor] = tentative_g
                h = manhattan_distance_heuristic(neighbor)
                f = tentative_g + h
                heapq.heappush(frontier, (f, tentative_g, neighbor, path + [move]))

    #No hay solucion
    return None, nodos_expandidos  