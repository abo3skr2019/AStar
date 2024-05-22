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
    def __init__(self):
        """Initialize the AStarApplication."""
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.maze = None
        self.start = None
        self.end = None
        self.heuristic = self.octile_distance
        self.settings_applied = False
        self.visualizer = None
        self.settings_dialog = None  # Reference to settings dialog
        print("AStarApplication initialized.")
        self.open_settings_menu()

    def start_visualization(self, settings):
        """Start the visualization."""
        print("Starting visualization")
        self.visualizer = Visualizer(self.maze, self.start, self.end, self.astar, settings)
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
        """Calculate the octile distance heuristic."""
        dx = abs(start[0] - goal[0])
        dy = abs(start[1] - goal[1])
        return max(dx, dy) + (1 - 1 / 2) * min(dx, dy)

    def euclidean_distance(self, start, goal):
        """Calculate the euclidean distance heuristic."""
        dx = abs(start[0] - goal[0])
        dy = abs(start[1] - goal[1])
        return (dx**2 + dy**2)**0.5

    def process_neighbor(self, matrix, current, neighbor, goal, open_set, came_from, g_score, f_score, rows, cols):
        """Process a neighbor node during A* algorithm."""
        if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and matrix[neighbor[0]][neighbor[1]] == 0:
            tentative_g_score = g_score[current] + self.heuristic(current, neighbor)
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + self.octile_distance(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    def astar(self, matrix, start, goal):
        """A* pathfinding algorithm."""
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

if __name__ == "__main__":
    print("Initializing A* application")
    astar_app = AStarApplication()
    print("Executing QApplication event loop")
    sys.exit(astar_app.app.exec_())
