import cProfile
import time
from A_Star_Implementation import visualize_search, generate_maze,no_visuals_astar

def run_and_profile():
    pregen_maze =[[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                 [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]]
    #Random_maze = generate_maze(100, 0.4)
    used_maze = pregen_maze
    start = (0, 0)
    end = (4, 6)
    no_visuals_astar(used_maze, start, end)

    '''
    if used_maze[end[0]][end[1]] == 1 or used_maze[start[0]][start[1]] == 1:
        print("End node is an obstacle or start node is an obstacle.")
    else:
        cProfile.runctx('no_visuals_astar(used_maze, start, end)', globals(), locals(), 'output.pstats')'''

if __name__ == '__main__':
    start_time = time.perf_counter()
    run_and_profile()
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")