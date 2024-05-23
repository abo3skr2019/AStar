import logging
from AstarApplication import AStarApplication
import sys
import time
import csv
import pandas as pd
from utils import generate_maze

def run_tests():
    results = []
    for maze_size in range(10, 110, 10):
        for obstacle_density in [i/10 for i in range(0, 11)]:
            exec_times = []
            for _ in range(100):
                predefined_settings = {
                    'window_width': 600,
                    'window_height': 600,
                    'Maze_size': maze_size,
                    'start_point': (0, 0),
                    'end_point': (maze_size-1, maze_size-1),
                    'heuristic': 'octile',
                    'start_node_color': '#00FF00',
                    'end_node_color': '#FFD700',
                    'path_color': '#0000FF',
                    'obstacle_color': '#000000',
                    'background_color': '#ffffff',
                    'expanded_node_color': '#808080',
                    'maze': generate_maze(maze_size, obstacle_density),
                }
                start_time = time.time()
                astar_app = AStarApplication(bypass_settings=True, predefined_settings=predefined_settings)
                astar_app.app.exec_()
                end_time = time.time()
                exec_time = end_time - start_time
                exec_times.append(exec_time)
            avg_exec_time = sum(exec_times) / len(exec_times)
            results.append([maze_size, obstacle_density, avg_exec_time])

    with open('results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Maze Size", "Obstacle Density", "Average Execution Time"])
        writer.writerows(results)

    df = pd.read_csv('results.csv')
    df.to_excel('results.xlsx', index=False)


def main():
    """
    Main function to start the A* application.
    Configures logging, initializes predefined settings, and starts the application.
    """
    logging.basicConfig(filename='application.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.debug("Starting main.py")

    predefined_settings = {
        'window_width': 600,
        'window_height': 600,
        'Maze_size': 10,
        'start_point': (0, 0),
        'end_point': (9, 9),
        'heuristic': 'octile',
        'start_node_color': '#00FF00',
        'end_node_color': '#FFD700',
        'path_color': '#0000FF',
        'obstacle_color': '#000000',
        'background_color': '#ffffff',
        'expanded_node_color': '#808080',
        'maze': [
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
            [0, 1, 1, 1, 0, 1, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 1, 0, 0],
        ],
    }

    bypass_settings = True
    astar_app = AStarApplication(bypass_settings=bypass_settings, predefined_settings=predefined_settings)
    sys.exit(astar_app.app.exec_())

if __name__ == "__main__":
    run_tests()
