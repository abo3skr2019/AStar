# AStarApplication.py

import sys
import random
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer
import heapq
from SettingsMenu import SettingsMenu
from Visualizer import Visualizer
from utils import reconstruct_path

class AStarApplication:
    def __init__(self, bypass_settings=False, predefined_settings=None):
        """Initialize the AStarApplication."""
        self._initialize_app()
        self._initialize_settings(bypass_settings, predefined_settings)
        print("AStarApplication initialized.")

    def _initialize_app(self):
        """Initialize the application and default values."""
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.maze = None
        self.start = None
        self.end = None
        self.heuristic = self.octile_distance
        self.settings_applied = False
        self.visualizer = None
        self.settings_dialog = None  # Reference to settings dialog

    def _initialize_settings(self, bypass_settings, predefined_settings):
        """Initialize settings based on parameters."""
        self.bypass_settings = bypass_settings  # Store the bypass_settings flag
        if bypass_settings and predefined_settings:
            self.apply_predefined_settings(predefined_settings)
        else:
            self.open_settings_menu()

    def start_visualization(self, settings):
        """Start the visualization."""
        print("Starting visualization")
        self.visualizer = Visualizer(self.maze, self.start, self.end, self.astar, settings, self.bypass_settings)
        self.visualizer.visualization_complete.connect(self.on_visualization_complete)  # Connect signal
        self.visualizer.visualize()

    def open_settings_menu(self):
        """Open the settings menu to configure the application."""
        if self.settings_dialog is not None and self.settings_dialog.isVisible():
            print("Closing existing settings menu.")
            self.settings_dialog.close()
            
        if not self.settings_applied:
            print("Opening settings menu")
            self.settings_dialog = SettingsMenu()
            self.settings_dialog.settings_updated.connect(self.handle_updated_settings)
            self.settings_dialog.menu_closed.connect(self.on_settings_menu_closed)
            self.settings_dialog.exec_()
        else:
            print("Settings already applied, skipping opening settings menu.")

    def handle_updated_settings(self, settings):
        """Handle the updated settings."""
        print("Handling updated settings")
        print("Updated settings:", settings)
        self.maze = settings['maze']
        self.start = settings['start_point']
        self.end = settings['end_point']
        self.heuristic = self.euclidean_distance if settings.get('heuristic') == 'euclidean' else self.octile_distance
        self.settings_applied = True
        print("Settings applied.")
        self.start_visualization(settings)

    def on_visualization_complete(self):
        """Handle the completion of the visualization."""
        print("Visualization complete, reopening settings menu.")
        self.settings_applied = False  # Reset the flag
        self.open_settings_menu()

    def on_settings_menu_closed(self):
        """Handle the settings menu being closed."""
        if not self.settings_applied:
            sys.exit()
        self.settings_dialog = None  # Reset the settings dialog reference

    def octile_distance(self, start, goal):
        """
        Calculate the octile distance heuristic.
        
        Args:
            start (tuple): The start node coordinates.
            goal (tuple): The goal node coordinates.

        Returns:
            float: The octile distance.
        """
        dx = abs(start[0] - goal[0])
        dy = abs(start[1] - goal[1])
        return max(dx, dy) + (1 - 1 / 2) * min(dx, dy)

    def euclidean_distance(self, start, goal):
        """
        Calculate the euclidean distance heuristic.
        
        Args:
            start (tuple): The start node coordinates.
            goal (tuple): The goal node coordinates.

        Returns:
            float: The euclidean distance.
        """
        dx = abs(start[0] - goal[0])
        dy = abs(start[1] - goal[1])
        return (dx**2 + dy**2)**0.5

    def process_neighbor(self, matrix, current, neighbor, goal, open_set, came_from, g_score, f_score, rows, cols):
        """
        Process a neighbor node during A* algorithm.
        
        Args:
            matrix (list): The maze represented as a 2D list.
            current (tuple): The current node.
            neighbor (tuple): The neighbor node.
            goal (tuple): The goal node.
            open_set (list): The priority queue of open nodes.
            came_from (dict): The dictionary mapping nodes to their predecessors.
            g_score (dict): The dictionary mapping nodes to their g-scores.
            f_score (dict): The dictionary mapping nodes to their f-scores.
            rows (int): The number of rows in the maze.
            cols (int): The number of columns in the maze.
        """
        if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and matrix[neighbor[0]][neighbor[1]] == 0:
            tentative_g_score = g_score[current] + self.heuristic(current, neighbor)
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + self.octile_distance(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    def astar(self, matrix, start, goal):
        """
        A* pathfinding algorithm.
        
        Args:
            matrix (list): The maze represented as a 2D list.
            start (tuple): The start node coordinates.
            goal (tuple): The goal node coordinates.

        Yields:
            tuple: The current node, open set, and came_from dictionary at each step.
        """
        rows = len(matrix)
        cols = len(matrix[0])
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        open_set = [(0, start)]
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.octile_distance(start, goal)}

        while open_set:
            current = heapq.heappop(open_set)[1]
            yield current, open_set, came_from

            if current == goal:
                return reconstruct_path(came_from, current, start)

            for dx, dy in directions:
                neighbor = current[0] + dx, current[1] + dy
                self.process_neighbor(matrix, current, neighbor, goal, open_set, came_from, g_score, f_score, rows, cols)

        yield None, None, None

    def apply_predefined_settings(self, settings):
        """
        Apply predefined settings and start visualization.
        
        Args:
            settings (dict): The predefined settings.
        """
        self.handle_updated_settings(settings)

if __name__ == "__main__":
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
        'background_color': '#1E1E1E',
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

    # Set bypass_settings to True to skip the settings menu and use predefined settings
    bypass_settings = True

    astar_app = AStarApplication(bypass_settings=bypass_settings, predefined_settings=predefined_settings)
    sys.exit(astar_app.app.exec_())
