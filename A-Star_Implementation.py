import random
import matplotlib.pyplot as plt
import logging
import heapq
import numpy as np

logging.basicConfig(filename='output.log', level=logging.INFO, format='%(message)s')


def octile_distance(start, goal):
    dx = abs(start[0] - goal[0])
    dy = abs(start[1] - goal[1])
    return max(dx, dy) + (1 - 1 / 2) * min(dx, dy)

def euclidean_distance(start, goal):
    dx = abs(start[0] - goal[0])
    dy = abs(start[1] - goal[1])
    return (dx**2 + dy**2)**0.5

def astar(matrix, start, goal):
    rows = len(matrix)
    cols = len(matrix[0])
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}
    f_score = {start: octile_distance(start, goal)}

    while open_set:
        current = heapq.heappop(open_set)[1]
        yield current, open_set, came_from

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for dx, dy in directions:
            neighbor = current[0] + dx, current[1] + dy
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and matrix[neighbor[0]][neighbor[1]] == 0:
                tentative_g_score = g_score[current] + octile_distance(current, neighbor)
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + octile_distance(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    yield None, None, None


        
def create_matrix_vis(matrix):
    return [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]

def mark_expanded_nodes(matrix_vis, came_from):
    for node in came_from.keys():
        matrix_vis[node[0]][node[1]] = 4

def mark_obstacles(matrix, matrix_vis):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 1:
                matrix_vis[i][j] = 1

def mark_start_end_nodes(matrix_vis, start, goal):
    matrix_vis[start[0]][start[1]] = 3  # Start node is now green
    matrix_vis[goal[0]][goal[1]] = 2  # End node is now purple

def draw_current_state(ax, matrix_vis, cmap, path):
    ax.clear()
    ax.imshow(matrix_vis, cmap=cmap)
    if path:
        ax.plot([x[1] for x in path], [x[0] for x in path], color='blue', linewidth=2)  # Path is blue

    # Add grid lines
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
    ax.set_xticks(np.arange(-.5, len(matrix_vis[0]), 1))
    ax.set_yticks(np.arange(-.5, len(matrix_vis), 1))

    # Remove x and y axis numbers
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    plt.pause(0.1)

def get_path(came_from, current, start):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

def visualize_search(matrix, start, goal):
    cmap = plt.cm.colors.ListedColormap(['white', 'black', 'purple', 'green', 'grey'])
    fig, ax = plt.subplots(figsize=(10, 10))  # Increase the size of the plot

    path = None
    matrix_vis = create_matrix_vis(matrix)
    for current, open_set, came_from in astar(matrix, start, goal):
        if current is None:
            print("No path found")
            break

        if current == goal:
            path = get_path(came_from, current, start)

        
        mark_expanded_nodes(matrix_vis, came_from)
        mark_obstacles(matrix, matrix_vis)
        mark_start_end_nodes(matrix_vis, start, goal)
        draw_current_state(ax, matrix_vis, cmap, path)

    plt.show()



def generate_maze(size, obstacle_density):
    maze = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if random.uniform(0, 1) < obstacle_density:
                maze[i][j] = 1
    return maze

def no_visuals_astar(matrix, start, goal):
    path = astar(matrix, start, goal)
    if path is None:
        print("No path found")
    else:
        print("Path found:", path)

if __name__ == '__main__':
        maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]]
        new_maze = generate_maze(100, 0.4)
        used_maze = maze
        start= (0, 0)
        end = (4, 6)
        if used_maze[end[0]][end[1]] == 1 or used_maze[start[0]][start[1]] == 1:
             print("End node is an obstacle or start node is an obstacle.")
        else:
            visualize_search(used_maze, start, end)
