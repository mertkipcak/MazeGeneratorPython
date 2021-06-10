import random


class Maze:
    """
    initializer for the maze class, width and height must be odd.
    """

    def __init__(self, cols, rows):
        if (cols % 2 == 0) or (rows % 2 == 0):
            print("Enter odd numbers as maze dimensions")
            return
        self._cols, self._rows = cols, rows
        self._maze = [[False for _ in range(rows)] for _ in range(cols)]
        self.generate_maze()

    def generate_maze(self):
        for n in range(self._cols):
            self._maze[n][0] = True
            self._maze[n][self._rows - 1] = True
        for n in range(self._rows):
            self._maze[0][n] = True
            self._maze[self._cols - 1][n] = True
        self.recursive_maze(0, 0, self._cols - 1, self._rows - 1)
        print("done")

    def recursive_maze(self, x1, y1, x2, y2):
        # pick random wall coordinates and place them on the maze (they need to be even)
        wall_x = x1
        wall_y = x2
        while (wall_x == x1) or (wall_x == x2) or (wall_y == y1) or (wall_y == y2):
            wall_x = random.randrange(x1, x2, 2)
            wall_y = random.randrange(y1, y2, 2)
        for n in range(y1, y2):
            self._maze[wall_x][n] = True
        for n in range(x1, x2):
            self._maze[n][wall_y] = True

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
                self._maze[wall_x][gaps[n]] = False
            else:
                self._maze[gaps[n]][wall_y] = False

        # recursively call this function on subareas if they are big enough
        if (wall_x - x1 > 3) and (wall_y - y1 > 3):
            self.recursive_maze(x1, y1, wall_x, wall_y)

        if (x2 - wall_x > 3) and (wall_y - y1 > 3):
            self.recursive_maze(wall_x, y1, x2, wall_y)

        if (wall_x - x1 > 3) and (y2 - wall_y > 3):
            self.recursive_maze(x1, wall_y, wall_x, y2)

        if (x2 - wall_x > 3) and (y2 - wall_y > 3):
            self.recursive_maze(wall_x, wall_y, x2, y2)

    def print_maze(self):
        for x in self._maze:
            for y in x:
                if y:
                    print("@", end="")
                else:
                    print(" ", end="")
            print("\n", end="")
