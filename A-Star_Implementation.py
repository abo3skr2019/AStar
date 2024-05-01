import random
import matplotlib.pyplot as plt

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def visualize_maze(maze, path, expanded_nodes, obstacles):
    """Visualizes the maze and the path"""

    # Create a 2D array to represent the maze
def visualize_maze(maze, path, expanded_nodes, obstacles):
    """Visualizes the maze and the path"""

    # Create a 2D array to represent the maze
    maze_vis = [[0 for _ in range(len(maze[0]))] for _ in range(len(maze))]

    # Mark the expanded nodes on the maze
    for node in expanded_nodes:
        maze_vis[node[0]][node[1]] = 4

    # Mark the obstacles on the maze
    for node in obstacles:
        maze_vis[node[0]][node[1]] = 1

    # Mark the start and end nodes
    maze_vis[path[0][0]][path[0][1]] = 3  # Start node is now green
    maze_vis[path[-1][0]][path[-1][1]] = 2  # End node is now purple

    # Create a color map for the maze
    cmap = plt.cm.colors.ListedColormap(['white', 'black', 'purple', 'green', 'grey'])  # Changed the colors

    # Create a figure and axes
    fig, ax = plt.subplots()

    # Display the maze
    im = ax.imshow(maze_vis, cmap=cmap)

    # Draw the path on top of the maze
    path_x = [node[1] for node in path]
    path_y = [node[0] for node in path]
    ax.plot(path_x, path_y, color='blue', linewidth=2)  # Path is blue

    # Create a colorbar
    cbar = fig.colorbar(im, ax=ax, ticks=[0, 1, 2, 3, 4])

    # Set the colorbar labels
    cbar.ax.set_yticklabels(['Empty', 'Obstacle', 'End', 'Start', 'Expanded'])  # Changed the labels

    # Set the title and labels
    ax.set_title('Maze')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    ax.grid(True, which='both', color='k', linewidth=1)

    x_ticks = [x + 0.5 for x in range(len(maze[0]))]
    y_ticks = [y + 0.5 for y in range(len(maze))]
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)

    # Set the tick labels
    ax.set_xticklabels(range(len(maze[0])))
    ax.set_yticklabels(range(len(maze)))
    ax.invert_yaxis()
    # Set the aspect ratio to be equal so the grid cells are square
    ax.set_aspect('equal')

    # Show the plot
    plt.show()        
def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []
    expanded_nodes = []
    obstacles = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)
        expanded_nodes.append(current_node.position)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1], expanded_nodes, obstacles  # Return reversed path, expanded_nodes, and obstacles
        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                obstacles.append(node_position)
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)
    return path[::-1], expanded_nodes, obstacles



def generate_maze(size, obstacle_density):
    maze = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if random.uniform(0, 1) < obstacle_density:
                maze[i][j] = 1
    return maze

def main():

    maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    start = (0, 0)
    end = (9,9)


    path, expanded_nodes, obstacles = astar(maze, start, end)
    print(path)
    visualize_maze(maze, path, expanded_nodes, obstacles)

if __name__ == '__main__':
    main()