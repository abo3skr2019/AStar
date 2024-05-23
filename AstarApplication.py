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
import logging

class AStarApplication:
    def __init__(self, bypass_settings=False, predefined_settings=None):
        logging.debug("Initializing AStarApplication with bypass_settings=%s", bypass_settings)
        self._initialize_app()
        self._initialize_settings(bypass_settings, predefined_settings)
        logging.debug("AStarApplication initialized.")

    def _initialize_app(self):
        logging.debug("Initializing application and default values")
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.maze = None
        self.start = None
        self.end = None
        self.heuristic = self.octile_distance
        self.settings_applied = False
        self.visualizer = None
        self.settings_dialog = None  # Reference to settings dialog

    def _initialize_settings(self, bypass_settings, predefined_settings):
        logging.debug(f"Initializing settings (bypass_settings={bypass_settings})")
        self.bypass_settings = bypass_settings  # Store the bypass_settings flag
        if bypass_settings and predefined_settings:
            self.apply_predefined_settings(predefined_settings)
        else:
            self.open_settings_menu()

    def start_visualization(self, settings):
        logging.debug("Starting visualization")
        self.visualizer = Visualizer(self.maze, self.start, self.end, self.astar, settings, self.bypass_settings)
        self.visualizer.visualization_complete.connect(self.on_visualization_complete)  # Connect signal
        self.visualizer.visualize()

    def open_settings_menu(self):
        logging.debug("Opening settings menu")
        if self.settings_dialog is not None and self.settings_dialog.isVisible():
            logging.debug("Closing existing settings menu.")
            self.settings_dialog.close()
            
        if not self.settings_applied:
            logging.debug("Creating new settings dialog")
            self.settings_dialog = SettingsMenu()
            self.settings_dialog.settings_updated.connect(self.handle_updated_settings)
            self.settings_dialog.menu_closed.connect(self.on_settings_menu_closed)
            self.settings_dialog.exec_()
        else:
            logging.debug("Settings already applied, skipping opening settings menu.")

    def handle_updated_settings(self, settings):
        logging.debug("Handling updated settings")
        logging.debug(f"Updated settings: {settings}")
        self.maze = settings['maze']
        self.start = settings['start_point']
        self.end = settings['end_point']
        self.heuristic = self.euclidean_distance if settings.get('heuristic') == 'euclidean' else self.octile_distance
        self.settings_applied = True
        logging.debug("Settings applied.")
        self.start_visualization(settings)

    def on_visualization_complete(self):
        logging.debug("Visualization complete, reopening settings menu.")
        self.settings_applied = False  # Reset the flag
        self.open_settings_menu()

    def on_settings_menu_closed(self):
        logging.debug("Settings menu closed")
        if not self.settings_applied:
            logging.debug("Settings not applied, exiting application")
            sys.exit()
        self.settings_dialog = None  # Reset the settings dialog reference

    def octile_distance(self, start, goal):
        dx = abs(start[0] - goal[0])
        dy = abs(start[1] - goal[1])
        return max(dx, dy) + (1 - 1 / 2) * min(dx, dy)

    def euclidean_distance(self, start, goal):
        dx = abs(start[0] - goal[0])
        dy = abs(start[1] - goal[1])
        return (dx**2 + dy**2)**0.5

    def process_neighbor(self, matrix, current, neighbor, goal, open_set, came_from, g_score, f_score, rows, cols):
        if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and matrix[neighbor[0]][neighbor[1]] == 0:
            tentative_g_score = g_score[current] + self.heuristic(current, neighbor)
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + self.octile_distance(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    def astar(self, matrix, start, goal):
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
        logging.debug("Applying predefined settings")
        self.handle_updated_settings(settings)
