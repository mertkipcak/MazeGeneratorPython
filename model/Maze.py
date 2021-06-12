import random
import enum


class State(enum.Enum):
    wall = 1
    empty = 2
    solution = 3
    discovered = 4


class Maze:
    """
    initializer for the maze class, width and height must be odd.
    """

    def __init__(self, cols, rows):
        if (cols % 2 == 0) or (rows % 2 == 0):
            print("Enter odd numbers as maze dimensions")
            return
        self._cols, self._rows = cols, rows
        self._maze = [[State.empty for _ in range(rows)] for _ in range(cols)]
        self.generate_maze()

    def generate_maze(self):
        for n in range(self._cols):
            self._maze[n][0] = State.wall
            self._maze[n][self._rows - 1] = State.wall
        for n in range(self._rows):
            self._maze[0][n] = State.wall
            self._maze[self._cols - 1][n] = State.wall
        self.recursive_maze(0, 0, self._cols - 1, self._rows - 1)

    # def __init__(self, board):
    #     self._maze = board

    def recursive_maze(self, x1, y1, x2, y2):
        # pick random wall coordinates and place them on the maze (they need to be even)
        wall_x = x1
        wall_y = x2
        while (wall_x == x1) or (wall_x == x2) or (wall_y == y1) or (wall_y == y2):
            wall_x = random.randrange(x1, x2, 2)
            wall_y = random.randrange(y1, y2, 2)
        for n in range(y1, y2):
            self._maze[wall_x][n] = State.wall
        for n in range(x1, x2):
            self._maze[n][wall_y] = State.wall

        # pick 3 random openings from 4 walls created (2 walls intersecting at a point, consider each direction a wall)
        # 0 is North, 1 is West, 2 is South, 3 is East
        no_gap = random.randint(0, 3)
        gaps = [2 * random.randint(y1 / 2, int(wall_y / 2) - 1) + 1,
                2 * random.randint(x1 / 2, int(wall_x / 2) - 1) + 1,
                2 * random.randint(int(wall_y / 2), y2 / 2 - 1) + 1,
                2 * random.randint(int(wall_x / 2), x2 / 2 - 1) + 1]
        for n in range(4):
            if n == no_gap:
                continue
            if n % 2 == 0:
                self._maze[wall_x][gaps[n]] = State.empty
            else:
                self._maze[gaps[n]][wall_y] = State.empty

        # recursively call this function on subareas if they are big enough
        if (wall_x - x1 > 3) and (wall_y - y1 > 3):
            self.recursive_maze(x1, y1, wall_x, wall_y)

        if (x2 - wall_x > 3) and (wall_y - y1 > 3):
            self.recursive_maze(wall_x, y1, x2, wall_y)

        if (wall_x - x1 > 3) and (y2 - wall_y > 3):
            self.recursive_maze(x1, wall_y, wall_x, y2)

        if (x2 - wall_x > 3) and (y2 - wall_y > 3):
            self.recursive_maze(wall_x, wall_y, x2, y2)

    def solve_maze_dfs(self, xs, ys, xf, yf):
        curr = [xs, ys]
        self._maze[xs][ys] = State.discovered
        tile_queue = []
        came_from = [[[0, 0] for _ in range(self._rows)] for _ in range(self._cols)]
        while not ((curr[0] == xf) and (curr[1] == yf)):
            self._maze[curr[0]][curr[1]] = State.discovered
            adjacent = self.get_viable_adjacent(curr)
            for pair in adjacent:
                came_from[pair[0]][pair[1]] = curr
            tile_queue.extend(adjacent)
            if len(tile_queue) != 0:
                curr = tile_queue.pop()
            else:
                print("solution not found")
                return

        solution = [[xf, yf]]
        curr = [xf, yf]
        while not ((curr[0] == xs) and (curr[1] == ys)):
            solution.append(came_from[curr[0]][curr[1]])
            curr = came_from[curr[0]][curr[1]]
        for pair in solution:
            self._maze[pair[0]][pair[1]] = State.solution
        return solution

    def get_viable_adjacent(self, curr):
        ret = []
        if self._maze[curr[0]][curr[1] - 1] == State.empty:
            ret.append([curr[0], curr[1] - 1])
        if self._maze[curr[0] - 1][curr[1]] == State.empty:
            ret.append([curr[0] - 1, curr[1]])
        if self._maze[curr[0]][curr[1] + 1] == State.empty:
            ret.append([curr[0], curr[1] + 1])
        if self._maze[curr[0] + 1][curr[1]] == State.empty:
            ret.append([curr[0] + 1, curr[1]])
        return ret

    def print_maze(self):
        for x in range(0, self._rows):
            for y in range(0, self._cols):
                if self._maze[x][y] == State.wall:
                    print("\033[0m@", end="")
                elif self._maze[x][y] == State.solution:
                    print("\033[92m*", end="")
                elif self._maze[x][y] == State.discovered:
                    print("\033[91m.", end="")
                else:
                    print(" ", end="")
            print("\n", end="")