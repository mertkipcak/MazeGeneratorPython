# This is a sample Python script.
from Maze import Maze


def print_hi():
    maze = Maze(101, 101)
    maze.print_maze()
    input("press ENTER to solve")

    maze.print_maze(maze.solve_maze_dfs(1, 1, 99, 99))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi()
