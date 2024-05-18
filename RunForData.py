import cProfile
import pstats
import csv
from A_Star_Implementation import visualize_search, generate_maze

def write_pstats_to_csv(pstats_file, csv_file):
    p = pstats.Stats(pstats_file)
    p.sort_stats('cumulative')

    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ncalls', 'tottime', 'percall', 'cumtime', 'percall', 'filename:lineno(function)'])

        for stat in p.stats.items():
            func_name = stat[0]
            func_stat = stat[1]
            row = [func_stat[0], func_stat[2], func_stat[2]/func_stat[0], func_stat[3], func_stat[3]/func_stat[0], func_name]
            writer.writerow(row)

def run_and_profile():
    maze = generate_maze(100, 0.4)
    start = (0, 0)
    end = (99, 99)
    if maze[end[0]][end[1]] == 1 or maze[start[0]][start[1]] == 1:
        print("End node is an obstacle or start node is an obstacle.")
        return
    else:
        cProfile.run('visualize_search(maze, start, end)', 'output.pstats')

    write_pstats_to_csv('output.pstats', 'pstats_output.csv')

if __name__ == '__main__':
    run_and_profile()