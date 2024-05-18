import cProfile
import time
from A_Star_Implementation import visualize_astar, generate_maze,no_visuals_astar, no_visuals_queueastar
import csv
import random
Random_maze = generate_maze(1000, 0.45)
start = (0, random.randint(0, 999))
end = (random.randint(0, 999), random.randint(0, 999))

def no_visuals_run_and_profile(implementation_type):
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
    used_maze = Random_maze
    used_maze[start[0]][start[1]] = 0
    used_maze[end[0]][end[1]] = 0
    if implementation_type == 'heapq':
        no_visuals_astar(used_maze, start, end)  # Assuming this uses heapq
    else:
        no_visuals_queueastar(used_maze, start, end)  # New function to be implemented

"""
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
        visualize_astar(used_maze, start, end)
"""
def run_multiple_times(n):
    heapq_times = []
    priorityqueue_times = []
    for _ in range(n):
        start_time = time.perf_counter()
        no_visuals_run_and_profile('heapq')
        end_time = time.perf_counter()
        heapq_times.append(end_time - start_time)

        start_time = time.perf_counter()
        no_visuals_run_and_profile('priorityqueue')
        end_time = time.perf_counter()
        priorityqueue_times.append(end_time - start_time)
    return heapq_times, priorityqueue_times

if __name__ == '__main__':
    heapq_times, priorityqueue_times = run_multiple_times(100)

    with open('execution_times.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Run", "Heapq", "PriorityQueue"])
        for i in range(len(heapq_times)):
            writer.writerow([i+1, heapq_times[i], priorityqueue_times[i]])
