import logging
from AstarApplication import AStarApplication
import sys

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
    main()
