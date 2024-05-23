# utils.py

import random
import logging

def setup_logging():
    """
    Configure the logging settings for the application.
    Logs will be written to 'application.log' with a specific format.
    """
    logging.basicConfig(filename='application.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def reconstruct_path(came_from, current, start):
    """
    Reconstructs the path from the start to the current node using the came_from dictionary.
    
    Args:
        came_from (dict): Dictionary containing the previous node for each visited node.
        current (tuple): The current node.
        start (tuple): The start node.
    
    Returns:
        list: The reconstructed path from start to current node.
    """
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

def generate_maze(size, obstacle_density):
    """
    Generates a maze of a given size and obstacle density.
    
    Args:
        size (int): The size of the maze (size x size).
        obstacle_density (float): The density of obstacles in the maze (0 to 1).
    
    Returns:
        list: A 2D list representing the generated maze.
    """
    maze = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if random.uniform(0, 1) < obstacle_density:
                maze[i][j] = 1
    return maze

# Call setup_logging to configure logging when this module is imported
setup_logging()
