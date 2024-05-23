# Visualizer.py

import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QColor
from utils import reconstruct_path
import sys

class Visualizer(QObject):
    visualization_complete = pyqtSignal()  # Signal emitted when visualization is complete

    def __init__(self, maze, start, goal, astar_function, settings, bypass_settings=False):
        """
        Initialize the Visualizer object.
        
        Args:
            maze (list): The maze represented as a 2D list.
            start (tuple): The start node coordinates.
            goal (tuple): The goal node coordinates.
            astar_function (function): The A* algorithm function.
            settings (dict): Settings for the visualization.
            bypass_settings (bool): Flag to bypass settings.
        """
        super().__init__()  # Initialize QObject
        self.maze = maze
        self.start = start
        self.goal = goal
        self.astar_function = astar_function
        self.settings = settings
        self.bypass_settings = bypass_settings  # Store the bypass_settings flag
        self.win = pg.GraphicsLayoutWidget(show=True, title="A* Visualization")
        self.win.resize(settings['window_width'], settings['window_height'])
        self.view = self.win.addViewBox()
        self.view.setAspectLocked(True)
        self.view.enableAutoRange(True)
        self.color_maze = None

    def end_is_obstacle(self):
        """
        Check if the end node is an obstacle.
        
        Returns:
            bool: True if the end or start node is an obstacle, False otherwise.
        """
        if self.maze[self.goal[0]][self.goal[1]] == 1:
            print("End node is an obstacle.")
            return True
        if self.maze[self.start[0]][self.start[1]] == 1:
            print("Start node is an obstacle.")
            return True
        return False

    def is_surrounded(self, node):
        """
        Check if a node is surrounded by obstacles.
        
        Args:
            node (tuple): The node to check.

        Returns:
            bool: True if the node is surrounded, False otherwise.
        """
        rows, cols = len(self.maze), len(self.maze[0])
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dx, dy in directions:
            nx, ny = node[0] + dx, node[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols and self.maze[nx][ny] == 0:
                return False
        return True

    def visualize(self):
        """Visualize the A* pathfinding algorithm."""
        print("Visualizing A* pathfinding algorithm")
        print(f"\nSettings: {self.settings}\nStart node: {self.start}\nEnd node: {self.goal}\nMaze: {self.maze}\n")

        if self.end_is_obstacle() or self.is_surrounded(self.start) or self.is_surrounded(self.goal):
            self.handle_invalid_nodes()
            return

        self.prepare_color_maze()
        img_item = pg.ImageItem(image=self.color_maze)
        self.view.addItem(img_item)

        self.astar_visualized(img_item)

    def handle_invalid_nodes(self):
        """Handle scenarios where start or end nodes are invalid."""
        if self.end_is_obstacle():
            print("End or Start node is an obstacle.")
            self.show_reopen_settings_dialog("End or Start node is an obstacle.")
        elif self.is_surrounded(self.start):
            print("Start node is surrounded by obstacles.")
            self.show_reopen_settings_dialog("Start node is surrounded by obstacles.")
        elif self.is_surrounded(self.goal):
            print("End node is surrounded by obstacles.")
            self.show_reopen_settings_dialog("End node is surrounded by obstacles.")

    def prepare_color_maze(self):
        """Prepare the color maze representation for visualization."""
        self.convert_colors()
        self.color_maze = np.array([self.obstacle_color if cell == 1 else self.background_color for row in self.maze for cell in row], dtype=np.ubyte).reshape((len(self.maze[0]), len(self.maze), 3)).transpose((1, 0, 2))

    def convert_colors(self):
        """Convert color settings from hex to RGB."""
        self.start_color = QColor(self.settings['start_node_color']).getRgb()[:3]
        self.end_color = QColor(self.settings['end_node_color']).getRgb()[:3]
        self.path_color = QColor(self.settings['path_color']).getRgb()[:3]
        self.obstacle_color = QColor(self.settings['obstacle_color']).getRgb()[:3]
        self.background_color = QColor(self.settings['background_color']).getRgb()[:3]
        self.expanded_node_color = QColor(self.settings['expanded_node_color']).getRgb()[:3]

    def update_cell(self, img_item, cell, color):
        """
        Update the color of a cell in the maze.
        
        Args:
            img_item (ImageItem): The image item to update.
            cell (tuple): The cell coordinates.
            color (tuple): The RGB color.
        """
        self.color_maze[cell[1], cell[0]] = color
        img_item.setImage(image=self.color_maze)

    def draw_path(self, path):
        """
        Draw the path on the visualization.
        
        Args:
            path (list): The path to draw.
        """
        for i in range(len(path) - 1):
            x = [path[i][0], path[i + 1][0]]
            y = [path[i][1], path[i + 1][1]]
            line = pg.PlotDataItem(y, x, pen=pg.mkPen('b', width=2))
            self.view.addItem(line)
            QApplication.processEvents()

    def astar_visualized(self, img_item):
        """
        Visualize the A* algorithm step by step.
        
        Args:
            img_item (ImageItem): The image item to update.
        """
        self.update_cell(img_item, self.start, self.start_color)
        self.update_cell(img_item, self.goal, self.end_color)

        for current, open_set, came_from in self.astar_function(self.maze, self.start, self.goal):
            if current is None:
                QMessageBox.warning(None, "Pathfinding Warning", "No path found. The application will close in 2 seconds.")
                QTimer.singleShot(1600, QApplication.instance().exit)
                return

            if current != self.goal:
                self.update_cell(img_item, current, self.expanded_node_color)
            else:
                path = reconstruct_path(came_from, current, self.start)
                self.draw_path(path)
                print("Path found:", path)
                if self.bypass_settings:
                    self.quit_application()
                else:
                    self.wait_for_user_action()
                return

            if current == self.start:
                self.update_cell(img_item, self.start, [0, 255, 0])

            QApplication.processEvents()

    def wait_for_user_action(self):
        """Wait for user action before completing the visualization."""
        msgBox = QMessageBox()
        msgBox.setText("The pathfinding visualization is complete.")
        msgBox.setInformativeText("Click Ok to restart with different parameters, or Cancel to exit.")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        result = msgBox.exec_()
        if result == QMessageBox.Ok:
            self.close_visualizer()  # Close the visualizer window
            self.visualization_complete.emit()  # Emit the signal to reopen the settings menu
        else:
            sys.exit()  # Properly close the application

    def show_reopen_settings_dialog(self, message):
        """
        Show a message box to reopen settings or exit.
        
        Args:
            message (str): The message to display.
        """
        msgBox = QMessageBox()
        msgBox.setText(message)
        msgBox.setInformativeText("Click Ok to reopen the settings menu, or Cancel to exit.")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        result = msgBox.exec_()
        if result == QMessageBox.Ok:
            self.close_visualizer()  # Close the visualizer window
            self.visualization_complete.emit()  # Emit the signal to reopen the settings menu
        else:
            sys.exit()  # Properly close the application

    def close_visualizer(self):
        """Close the visualizer window."""
        self.win.close()

    def quit_application(self):
        """Quit the application."""
        QApplication.instance().exit()
