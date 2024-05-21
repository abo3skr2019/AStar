# main.py
from AstarApplication import AStarApplication
import sys

if __name__ == "__main__":
    print("Running main.py")
    astar_app = AStarApplication()
    sys.exit(astar_app.app.exec_())
