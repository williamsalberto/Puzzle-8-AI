from collections import deque
import puzzle_logic 
import constants    

#Algoritmo BFS (Breadth-First Search)
def solve_bfs(initial_state_tuple):
    goal_state_tuple = constants.GOAL_STATE_TUPLE

    #Si se da el caso de que el inicial == meta
    #Retornamos el tablero 
    if initial_state_tuple == goal_state_tuple:
        return [] 

    queue = deque([(initial_state_tuple, [])]) #Cola: (estado, camino hasta aquí)
    visited = set()
    visited.add(initial_state_tuple)

    #Lista para determinar los nodos de expansion
    nodos_expandidos = []

    while queue:
        current_state_tuple, path = queue.popleft()
        nodos_expandidos.append(current_state_tuple)

        #Generar vecinos y sus movimientos usando la función de puzzle_logic
        for neighbor_state_tuple, move in puzzle_logic.get_neighbors(current_state_tuple):
            if neighbor_state_tuple not in visited:
                visited.add(neighbor_state_tuple)
                #Crea una nueva rama para recorrer
                new_path = path + [move] 
                if neighbor_state_tuple == goal_state_tuple:
                    return new_path, nodos_expandidos #Se llega a la meta
                queue.append((neighbor_state_tuple, new_path))

    return None, nodos_expandidos #No hay solucion
