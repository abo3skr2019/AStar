import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QColor
from utils import reconstruct_path
import logging
import sys


class Visualizer(QObject):
    """
    Class representing the visualizer for the A* algorithm.
    Handles the visualization of the pathfinding process.
    """
    visualization_complete = pyqtSignal()  # Signal emitted when visualization is complete

    def __init__(self, maze, start, goal, astar_function, settings, bypass_settings=False):
        """
        Initializes the visualizer.
        
        Args:
            maze (list): The maze matrix.
            start (tuple): The start point.
            goal (tuple): The goal point.
            astar_function (function): The A* algorithm function.
            settings (dict): Settings for the visualization.
            bypass_settings (bool): Flag to bypass settings menu.
        """
        logging.debug("Initializing Visualizer")
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
        Checks if the end node is an obstacle.
        
        Returns:
            bool: True if the end node is an obstacle, False otherwise.
        """
        if self.maze[self.goal[0]][self.goal[1]] == 1:
            logging.debug("End node is an obstacle.")
            return True
        if self.maze[self.start[0]][self.start[1]] == 1:
            logging.debug("Start node is an obstacle.")
            return True
        return False

    def is_surrounded(self, node):
        """
        Checks if a node is surrounded by obstacles.
        
        Args:
            node (tuple): The node to check.
        
        Returns:
            bool: True if the node is surrounded by obstacles, False otherwise.
        """
        rows, cols = len(self.maze), len(self.maze[0])
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dx, dy in directions:
            nx, ny = node[0] + dx, node[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols and self.maze[nx][ny] == 0:
                return False
        return True

    def visualize(self):
        """
        Starts the visualization of the A* algorithm.
        """
        logging.debug("Starting A* visualization")
        logging.debug(f"\nSettings: {self.settings}\nStart node: {self.start}\nEnd node: {self.goal}\nMaze: {self.maze}\n")

        if self.end_is_obstacle() or self.is_surrounded(self.start) or self.is_surrounded(self.goal):
            self.handle_invalid_nodes()
            return

        self.prepare_color_maze()
        img_item = pg.ImageItem(image=self.color_maze)
        self.view.addItem(img_item)

        self.astar_visualized(img_item)

    def handle_invalid_nodes(self):
        """
        Handles invalid nodes in the maze (e.g., start or end nodes that are obstacles or surrounded).
        """
        logging.debug("Handling invalid nodes")
        if self.end_is_obstacle():
            logging.debug("End or Start node is an obstacle.")
            self.show_reopen_settings_dialog("End or Start node is an obstacle.")
        elif self.is_surrounded(self.start):
            logging.debug("Start node is surrounded by obstacles.")
            self.show_reopen_settings_dialog("Start node is surrounded by obstacles.")
        elif self.is_surrounded(self.goal):
            logging.debug("End node is surrounded by obstacles.")
            self.show_reopen_settings_dialog("End node is surrounded by obstacles.")

    def prepare_color_maze(self):
        """
        Prepares the color representation of the maze for visualization.
        """
        self.convert_colors()
        self.color_maze = np.array([self.obstacle_color if cell == 1 else self.background_color for row in self.maze for cell in row], dtype=np.ubyte).reshape((len(self.maze[0]), len(self.maze), 3)).transpose((1, 0, 2))

    def convert_colors(self):
        """
        Converts color settings to RGB values.
        """
        self.start_color = QColor(self.settings['start_node_color']).getRgb()[:3]
        self.end_color = QColor(self.settings['end_node_color']).getRgb()[:3]
        self.path_color = QColor(self.settings['path_color']).getRgb()[:3]
        self.obstacle_color = QColor(self.settings['obstacle_color']).getRgb()[:3]
        self.background_color = QColor(self.settings['background_color']).getRgb()[:3]
        self.expanded_node_color = QColor(self.settings['expanded_node_color']).getRgb()[:3]

    def update_cell(self, img_item, cell, color):
        """
        Updates the color of a cell in the maze visualization.
        
        Args:
            img_item (pg.ImageItem): The image item representing the maze.
            cell (tuple): The cell to update.
            color (tuple): The RGB color to set.
        """
        self.color_maze[cell[1], cell[0]] = color
        img_item.setImage(image=self.color_maze)

    def draw_path(self, path):
        """
        Draws the path from start to goal in the visualization.
        
        Args:
            path (list): The list of cells representing the path.
        """
        for i in range(len(path) - 1):
            x = [path[i][0], path[i + 1][0]]
            y = [path[i][1], path[i + 1][1]]
            line = pg.PlotDataItem(y, x, pen=pg.mkPen('b', width=2))
            self.view.addItem(line)
            QApplication.processEvents()

    def astar_visualized(self, img_item):
        """
        Visualizes the A* algorithm step by step.
        
        Args:
            img_item (pg.ImageItem): The image item representing the maze.
        """
        self.update_cell(img_item, self.start, self.start_color)
        self.update_cell(img_item, self.goal, self.end_color)

        for current, open_set, came_from in self.astar_function(self.maze, self.start, self.goal):
            if current is None:
                logging.warning("No path found. Closing application.")
                QMessageBox.warning(None, "Pathfinding Warning", "No path found. The application will close in 2 seconds.")
                QTimer.singleShot(1600, QApplication.instance().exit)
                return

            if current != self.goal:
                self.update_cell(img_item, current, self.expanded_node_color)
            else:
                path = reconstruct_path(came_from, current, self.start)
                self.draw_path(path)
                logging.debug(f"Path found: {path}")
                if self.bypass_settings:
                    logging.debug("Bypass settings is True. Quitting application.")
                    self.quit_application()
                else:
                    self.wait_for_user_action()
                return

            if current == self.start:
                self.update_cell(img_item, self.start, [0, 255, 0])

            QApplication.processEvents()

    def wait_for_user_action(self):
        """
        Waits for user action after the visualization is complete.
        """
        logging.debug("Showing message box for user action.")
        if self.bypass_settings:
            logging.debug("Bypass settings is True. Quitting application.")
            return
        logging.debug("Waiting for user action")
        msgBox = QMessageBox()
        msgBox.setText("The pathfinding visualization is complete.")
        msgBox.setInformativeText("Click Ok to restart with different parameters, or Cancel to exit.")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        result = msgBox.exec_()
        logging.debug("Message box result: %s", result)
        if result == QMessageBox.Ok:
            logging.debug("User chose to reopen settings menu.")
            self.close_visualizer()  # Close the visualizer window
            self.visualization_complete.emit()  # Emit the signal to reopen the settings menu
        else:
            logging.debug("User chose to exit the application")
            sys.exit()  # Properly close the application

    def show_reopen_settings_dialog(self, message):
        """
        Shows a dialog to reopen the settings menu if there are invalid nodes.
        
        Args:
            message (str): The message to display in the dialog.
        """
        logging.debug(f"Showing reopen settings dialog: {message}")
        msgBox = QMessageBox()
        msgBox.setText(message)
        msgBox.setInformativeText("Click Ok to reopen the settings menu, or Cancel to exit.")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        result = msgBox.exec_()
        if result == QMessageBox.Ok:
            self.close_visualizer()  # Close the visualizer window
            self.visualization_complete.emit()  # Emit the signal to reopen the settings menu
        else:
            logging.debug("User chose to exit the application")
            sys.exit()  # Properly close the application

    def close_visualizer(self):
        """
        Closes the visualizer window.
        """
        logging.debug("Closing visualizer window")
        self.win.close()

    def quit_application(self):
        """
        Quits the application.
        """
        logging.debug("Quitting application")
        QApplication.instance().exit()
