import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor
import sys
from utils import reconstruct_path
def end_is_obstacle(used_maze, start, end):
    if used_maze[end[0]][end[1]] == 1:
        print("End node is an obstacle.")
        return True
    if used_maze[start[0]][start[1]] == 1:
        print("Start node is an obstacle.")
        return True
    else:
            return False

def is_surrounded(matrix, node):
    rows, cols = len(matrix), len(matrix[0])
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for dx, dy in directions:
        nx, ny = node[0] + dx, node[1] + dy
        if 0 <= nx < rows and 0 <= ny < cols and matrix[nx][ny] == 0:
            return False  # Found a non-obstacle neighbor
    return True  # All neighbors are obstacles

def visualize_astar(maze, start, goal,astar_function, settings):
    print("Visualizing A* pathfinding algorithm\n\n")
    print(f"\n\nSettings:{settings}\n Start node:{start}\n End node:{goal} Maze:{maze} \n\n")
    if end_is_obstacle(maze, start, goal):
        print("end or Start node is an obstacle. Exiting.")
        exit()  # Exit the program if the start or end node is an obstacle
    if is_surrounded(maze, start):
        print("Start or end node is surrounded by obstacles. Exiting.")
        exit()
    if is_surrounded(maze, goal):
        print("end node is surrounded by obstacles. Exiting.")
        exit()

    win = pg.GraphicsLayoutWidget(show=True, title="A* Visualization")
    win.resize(600, 600)
    view = win.addViewBox()
    view.setAspectLocked(True)
    view.enableAutoRange(True)
    
    start_color = QColor(settings['start_node_color']).getRgb()[:3]
    end_color = QColor(settings['end_node_color']).getRgb()[:3]
    path_color = QColor(settings['path_color']).getRgb()[:3]
    obstacle_color = QColor(settings['obstacle_color']).getRgb()[:3]
    background_color = QColor(settings['background_color']).getRgb()[:3]

    # Modify color_maze initialization to use obstacle_color and background_color
    color_maze = np.array([obstacle_color if cell == 1 else background_color for row in maze for cell in row], dtype=np.ubyte).reshape((len(maze[0]), len(maze), 3)).transpose((1, 0, 2))
    
    img_item = pg.ImageItem(image=color_maze)
    view.addItem(img_item)

    def update_cell(cell, color):
        color_maze[cell[1], cell[0]] = color
        img_item.setImage(image=color_maze)

    def draw_path(path):
        for i in range(len(path) - 1):
            x = [path[i][0], path[i+1][0]]
            y = [path[i][1], path[i+1][1]]
            line = pg.PlotDataItem(y, x, pen=pg.mkPen('b', width=2))
            view.addItem(line)
            QApplication.processEvents()  # Force the GUI to update after drawing each line
        
    def astar_visualized(matrix, start, goal,astar_function):
        update_cell(start, start_color)
        update_cell(goal, end_color)

        for current, open_set, came_from in astar_function(matrix, start, goal):
            if current is None:
                QMessageBox.warning(None, "Pathfinding Warning", "No path found. The application will close in 2 seconds.")
                #QTimer.singleShot(1600, app.exit)  # Close the app after 2 seconds
                return

            if current != goal:
                update_cell(current, [128, 128, 128])  # Grey for expanded nodes
            else:
                path = reconstruct_path(came_from, current, start)
                draw_path(path)
                print("Path found:", path)
                wait_for_user_action()
                exit()
                return
            if current == start:
                update_cell(start, [0, 255, 0])  # Ensure start node is green

            QApplication.processEvents()

    astar_visualized(maze, start, goal,astar_function)

def wait_for_user_action():
    msgBox = QMessageBox()
    msgBox.setText("The pathfinding visualization is complete.")
    msgBox.setInformativeText("Close this message box to exit the application.")
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec_()

def no_visuals_astar(matrix, start, goal,astar_function,):
    if is_surrounded(matrix, start) or is_surrounded(matrix, goal):
        print("Start or end node is surrounded by obstacles. Exiting.")
        return  # Early exit

    path = None
    for current, open_set, came_from in astar_function(matrix, start, goal):
        if current is None:
            print("No path found")
            return

        if current == goal:
            path = reconstruct_path(came_from, current, start)
    print("Path found:", path)
