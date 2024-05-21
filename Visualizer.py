import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor
from utils import reconstruct_path

class Visualizer:
    def __init__(self, maze, start, goal, astar_function, settings):
        self.maze = maze
        self.start = start
        self.goal = goal
        self.astar_function = astar_function
        self.settings = settings
        self.win = pg.GraphicsLayoutWidget(show=True, title="A* Visualization")
        self.win.resize(settings['window_width'], settings['window_height'])
        self.view = self.win.addViewBox()
        self.view.setAspectLocked(True)
        self.view.enableAutoRange(True)
        self.color_maze = None

    def end_is_obstacle(self):
        if self.maze[self.goal[0]][self.goal[1]] == 1:
            print("End node is an obstacle.")
            return True
        if self.maze[self.start[0]][self.start[1]] == 1:
            print("Start node is an obstacle.")
            return True
        else:
            return False

    def is_surrounded(self, node):
        rows, cols = len(self.maze), len(self.maze[0])
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dx, dy in directions:
            nx, ny = node[0] + dx, node[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols and self.maze[nx][ny] == 0:
                return False  # Found a non-obstacle neighbor
        return True  # All neighbors are obstacles

    def visualize(self):
        print("Visualizing A* pathfinding algorithm")
        print(f"\nSettings: {self.settings}\nStart node: {self.start}\nEnd node: {self.goal}\nMaze: {self.maze}\n")

        if self.end_is_obstacle():
            print("End or Start node is an obstacle. Exiting.")
            exit()
        if self.is_surrounded(self.start):
            print("Start node is surrounded by obstacles. Exiting.")
            exit()
        if self.is_surrounded(self.goal):
            print("End node is surrounded by obstacles. Exiting.")
            exit()

        start_color = QColor(self.settings['start_node_color']).getRgb()[:3]
        end_color = QColor(self.settings['end_node_color']).getRgb()[:3]
        path_color = QColor(self.settings['path_color']).getRgb()[:3]
        obstacle_color = QColor(self.settings['obstacle_color']).getRgb()[:3]
        background_color = QColor(self.settings['background_color']).getRgb()[:3]

        self.color_maze = np.array([obstacle_color if cell == 1 else background_color for row in self.maze for cell in row], dtype=np.ubyte).reshape((len(self.maze[0]), len(self.maze), 3)).transpose((1, 0, 2))

        img_item = pg.ImageItem(image=self.color_maze)
        self.view.addItem(img_item)

        self.astar_visualized(img_item, start_color, end_color, path_color)

    def update_cell(self, img_item, cell, color):
        self.color_maze[cell[1], cell[0]] = color
        img_item.setImage(image=self.color_maze)

    def draw_path(self, path):
        for i in range(len(path) - 1):
            x = [path[i][0], path[i + 1][0]]
            y = [path[i][1], path[i + 1][1]]
            line = pg.PlotDataItem(y, x, pen=pg.mkPen('b', width=2))
            self.view.addItem(line)
            QApplication.processEvents()  # Force the GUI to update after drawing each line

    def astar_visualized(self, img_item, start_color, end_color, path_color):
        self.update_cell(img_item, self.start, start_color)
        self.update_cell(img_item, self.goal, end_color)

        for current, open_set, came_from in self.astar_function(self.maze, self.start, self.goal):
            if current is None:
                QMessageBox.warning(None, "Pathfinding Warning", "No path found. The application will close in 2 seconds.")
                QTimer.singleShot(1600, QApplication.instance().exit)  # Close the app after 2 seconds
                return

            if current != self.goal:
                self.update_cell(img_item, current, [128, 128, 128])  # Grey for expanded nodes
            else:
                path = reconstruct_path(came_from, current, self.start)
                self.draw_path(path)
                print("Path found:", path)
                self.wait_for_user_action()
                exit()
                return

            if current == self.start:
                self.update_cell(img_item, self.start, [0, 255, 0])  # Ensure start node is green

            QApplication.processEvents()

    def wait_for_user_action(self):
        msgBox = QMessageBox()
        msgBox.setText("The pathfinding visualization is complete.")
        msgBox.setInformativeText("Close this message box to exit the application.")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()
        QApplication.quit()
