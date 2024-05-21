# Import statements remain unchanged
import sys
import random
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer
import heapq
from SettingsMenu import SettingsMenu
from Visualizer import visualize_astar, no_visuals_astar
from functools import partial
from utils import reconstruct_path

class AStarApplication:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.maze = None
        self.start = None
        self.end = None
        self.heuristic = self.octile_distance  # Default heuristic
        self.open_settings_menu()

    def open_settings_menu(self):
        dialog = SettingsMenu()
        dialog.settings_updated.connect(self.handle_updated_settings)
        dialog.exec_()

    def handle_updated_settings(self, settings):
        print("Updated settings:", settings)
        self.maze = settings['maze']
        self.start = settings['start_point']
        self.end = settings['end_point']
        if settings.get('heuristic') == 'euclidean':
            self.heuristic = self.euclidean_distance
        else:
            self.heuristic = self.octile_distance


        if QApplication.instance() is not None:
            visualize_astar(self.maze, self.start, self.end, self.astar,settings)



    def octile_distance(self,start, goal):
        dx = abs(start[0] - goal[0])
        dy = abs(start[1] - goal[1])
        return max(dx, dy) + (1 - 1 / 2) * min(dx, dy)
    


    def euclidean_distance(self,start, goal):
        dx = abs(start[0] - goal[0])
        dy = abs(start[1] - goal[1])
        return (dx**2 + dy**2)**0.5
    
    def process_neighbor(self,matrix, current, neighbor, goal, open_set, came_from, g_score, f_score, rows, cols):
        if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and matrix[neighbor[0]][neighbor[1]] == 0:
            tentative_g_score = g_score[current] + self.heuristic(current, neighbor)
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + self.octile_distance(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))


    def astar(self,matrix, start, goal):
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
