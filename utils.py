import random

def reconstruct_path(came_from, current, start):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path


def generate_maze(size, obstacle_density):
    """
    Generate a random maze with given size and obstacle density.

    Args:
        size (int): The size of the maze.
        obstacle_density (float): The density of obstacles in the maze.

    Returns:
        list: A 2D list representing the maze.
    """
    maze = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if random.uniform(0, 1) < obstacle_density:
                maze[i][j] = 1
    return maze
