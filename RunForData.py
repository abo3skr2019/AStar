import cProfile
import time
from A_Star_Implementation import visualize_search, generate_maze,no_visuals_astar
import csv

def no_visuals_run_and_profile():
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
    Random_maze = generate_maze(100, 0.3)
    used_maze = Random_maze
    start = (0, 0)
    end = (80, 80)
    used_maze[start[0]][start[1]] = 0
    used_maze[end[0]][end[1]] = 0
    no_visuals_astar(used_maze, start, end)

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
    Random_maze = generate_maze(100, 0.3)
    used_maze = Random_maze
    start = (0, 0)
    end = (80, 80)
    if used_maze[end[0]][end[1]] == 1 or used_maze[start[0]][start[1]] == 1:
        print("End node is an obstacle or start node is an obstacle.")
    else:
        #cProfile.runctx('visualize_search(used_maze, start, end)', globals(), locals(), 'output.pstats')
        visualize_search(used_maze, start, end)

def run_multiple_times(n):
    no_visuals_times = []
    visuals_times = []
    for _ in range(n):
        start_time = time.perf_counter()
        no_visuals_run_and_profile()
        end_time = time.perf_counter()
        no_visuals_times.append(end_time - start_time)

        start_time = time.perf_counter()
        #run_and_profile()
        end_time = time.perf_counter()
        visuals_times.append(0)
    return no_visuals_times, visuals_times

if __name__ == '__main__':
    no_visuals_times, visuals_times = run_multiple_times(10)

    with open('execution_times.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Run", "No Visuals Time", "Visuals Time"])
        for i in range(len(no_visuals_times)):
            writer.writerow([i+1, no_visuals_times[i], visuals_times[i]])
