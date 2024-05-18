import sys
import random
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor
import heapq
from queue import PriorityQueue


def is_surrounded(matrix, node):
    rows, cols = len(matrix), len(matrix[0])
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for dx, dy in directions:
        nx, ny = node[0] + dx, node[1] + dy
        if 0 <= nx < rows and 0 <= ny < cols and matrix[nx][ny] == 0:
            return False  # Found a non-obstacle neighbor
    return True  # All neighbors are obstacles

def queueastar(matrix, start, goal):
    rows = len(matrix)
    cols = len(matrix[0])
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: octile_distance(start, goal)}
    open_set_hash = {start}  # This is used to keep track of items in the PriorityQueue

    while not open_set.empty():
        current = open_set.get()[1]
        open_set_hash.remove(current)  # Remove from our tracking set
        yield current, open_set, came_from

        if current == goal:
            return reconstruct_path(came_from, current, start)

        for dx, dy in directions:
            neighbor = current[0] + dx, current[1] + dy
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and matrix[neighbor[0]][neighbor[1]] == 0:
                tentative_g_score = g_score[current] + octile_distance(current, neighbor)
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + octile_distance(neighbor, goal)
                    if neighbor not in open_set_hash:
                        open_set.put((f_score[neighbor], neighbor))
                        open_set_hash.add(neighbor)  # Add to our tracking set

    yield None, None, None

def astar(matrix, start, goal):
    rows = len(matrix)
    cols = len(matrix[0])
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}
    f_score = {start: octile_distance(start, goal)}

    while open_set:
        current = heapq.heappop(open_set)[1]
        yield current, open_set, came_from

        if current == goal:
            return reconstruct_path(came_from, current, start)

        for dx, dy in directions:
            neighbor = current[0] + dx, current[1] + dy
            process_neighbor(matrix, current, neighbor, goal, open_set, came_from, g_score, f_score, rows, cols)

    yield None, None, None

def no_visuals_astar(matrix, start, goal):
    if is_surrounded(matrix, start) or is_surrounded(matrix, goal):
        print("Start or end node is surrounded by obstacles. Exiting.")
        return  # Early exit

    path = None
    for current, open_set, came_from in astar(matrix, start, goal):
        if current is None:
            print("No path found")
            return

        if current == goal:
            path = reconstruct_path(came_from, current, start)
    print("Path found:", path)

def no_visuals_queueastar(matrix, start, goal):
    if is_surrounded(matrix, start) or is_surrounded(matrix, goal):
        print("Start or end node is surrounded by obstacles. Exiting.")
        return  # Early exit

    path = None
    for current, open_set, came_from in queueastar(matrix, start, goal):
        if current is None:
            print("No path found")
            return

        if current == goal:
            path = reconstruct_path(came_from, current, start)
    print("Path found:", path)


def visualize_astar(maze, start, goal):
    if is_surrounded(maze, start) or is_surrounded(maze, goal):
        print("Start or end node is surrounded by obstacles. Exiting.")
        return  # Early exit

    app = QApplication([])
    win = pg.GraphicsLayoutWidget(show=True, title="A* Visualization")
    win.resize(600, 600)
    view = win.addViewBox()
    view.setAspectLocked(True)
    view.enableAutoRange(True)
    
    color_maze = np.array([[0, 0, 0] if cell == 1 else [255, 255, 255] for row in maze for cell in row], dtype=np.ubyte).reshape((len(maze[0]), len(maze), 3)).transpose((1, 0, 2))
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
        
    def astar_visualized(matrix, start, goal):
        for current, open_set, came_from in astar(matrix, start, goal):
            if current is None:
                QMessageBox.warning(None, "Pathfinding Warning", "No path found. The application will close in 2 seconds.")
                QTimer.singleShot(1600, app.exit)  # Close the app after 2 seconds
                return

            if current != goal:
                update_cell(current, [0, 255, 0])  # Green for current path
            else:
                path = reconstruct_path(came_from, current, start)
                draw_path(path)
                print("Path found:", path)
                return
            QApplication.processEvents()
    update_cell(start, [0, 255, 0])
    update_cell(goal, [255, 215, 0])

    astar_visualized(maze, start, goal)
    sys.exit(app.exec_())


def octile_distance(start, goal):
    dx = abs(start[0] - goal[0])
    dy = abs(start[1] - goal[1])
    return max(dx, dy) + (1 - 1 / 2) * min(dx, dy)

def euclidean_distance(start, goal):
    dx = abs(start[0] - goal[0])
    dy = abs(start[1] - goal[1])
    return (dx**2 + dy**2)**0.5

def reconstruct_path(came_from, current, start):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

def process_neighbor(matrix, current, neighbor, goal, open_set, came_from, g_score, f_score, rows, cols):
    if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and matrix[neighbor[0]][neighbor[1]] == 0:
        tentative_g_score = g_score[current] + octile_distance(current, neighbor)
        if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = tentative_g_score + octile_distance(neighbor, goal)
            heapq.heappush(open_set, (f_score[neighbor], neighbor))





def generate_maze(size, obstacle_density):
    maze = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if random.uniform(0, 1) < obstacle_density:
                maze[i][j] = 1
    return maze

def end_obstacle(used_maze, start, end):
    if used_maze[end[0]][end[1]] == 1 or used_maze[start[0]][start[1]] == 1:
        return True
    else:
            return False

if __name__ == '__main__':
        maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]]
        new_maze = generate_maze(100, 0.1)
        used_maze = maze
        start= (0, 0)
        end = (9, 9)
        if end_obstacle(used_maze, start, end):
            
             print("End node is an obstacle or start node is an obstacle.")
        else:
            visualize_astar(used_maze, start, end)
