# utils.py

import random
import logging

def setup_logging():
    logging.basicConfig(filename='application.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def reconstruct_path(came_from, current, start):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

def generate_maze(size, obstacle_density):
    maze = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if random.uniform(0, 1) < obstacle_density:
                maze[i][j] = 1
    return maze

# Call setup_logging to configure logging when this module is imported
setup_logging()
