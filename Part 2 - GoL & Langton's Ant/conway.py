"""
The Game of Life (GoL) module named in honour of John Conway

This module defines the classes required for the GoL simulation.

"""

import numpy as np
from scipy import signal, ndimage
import re


def rle_parse(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()
        # construct the pattern lines and skip comments
        pattern_lines = []
        for line in lines:
            line = line.strip()
            if line and (not line.startswith("!") and not line.startswith("#")):
                pattern_lines.append(line)

        header = pattern_lines[0]
        # get the x and y value for width and height
        width = int(re.search(r"x\s*=\s*(\d+)", header).group(1))
        height = int(re.search(r"y\s*=\s*(\d+)", header).group(1))

        data = "".join(pattern_lines[1:]).strip()
        live_cells = []
        r = 0
        c = 0
        run_count = ""
        for char in data:
            if char.isdigit():
                run_count += char
            elif char in "ob$!":
                count = int(run_count) if run_count else 1
                run_count = ""

                if char == "o":
                    for _ in range(count):
                        live_cells.append((r, c))
                        c += 1
                elif char == "b":
                    c += count
                # end of line
                elif char == "$":
                    r += count
                    c = 0
                # end of rle file
                elif char == "!":
                    break

    return (width, height, live_cells)


def parse_pattern(filepath: str, aliveValue, deadValue):
    """
    Write a parser for Run Length Encoded (RLE) or Plaintext (.cells) patterns
    so grids larger than 20x20 can be loaded.

    Args:
        filepath (str): Path to the pattern file.

    Returns:
        tuple: (width, height, list of (r, c) offsets of live cells)
    """

    # check if it is rle file then parse rle file
    if filepath.endswith(".rle"):
        return rle_parse(filepath)

    # open file
    with open(filepath, "r") as f:
        lines = f.readlines()
        # construct the pattern lines
        pattern_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith("!"):
                pattern_lines.append(line)

        # find the withd of the pattern
        max_withd = max(len(line) for line in pattern_lines)

        pattern = []
        i = 0
        for line in pattern_lines:
            row = []
            for char in line:
                # add alive nodes
                if char == "O":
                    row.append(aliveValue)
                else:
                    row.append(deadValue)
            # feel the row if it is empty in at end
            row.extend([deadValue] * (max_withd - len(row)))
            pattern.append(row)
        live_cells = []
        for i in range(len(pattern)):
            for j in range(max_withd):
                if pattern[i][j] == aliveValue:
                    live_cells.append((i, j))

        return (max_withd, len(pattern_lines), live_cells)


class GameOfLife:
    """
    Object for computing Conway's Game of Life (GoL) cellular machine/automata
    """

    def __init__(self, N=256, finite=False, fastMode=True):
        self.grid = np.zeros((N, N), np.uint)
        self.neighborhood = np.ones((3, 3), np.uint)  # 8 connected kernel
        self.neighborhood[1, 1] = 0  # do not count centre pixel
        self.finite = finite
        self.fastMode = fastMode
        self.aliveValue = 1
        self.deadValue = 0
        self.rows = N  # use for slow implementation of evolve
        self.cols = N  # use for slow implementation of evolve

    def getStates(self):
        """
        Returns the current states of the cells
        """
        return self.grid

    def getGrid(self):
        """
        Same as getStates()
        """
        return self.getStates()

    def update_grid_fast(self):
        """
        Use scipy.signal.convolve2d (or similar) to compute neighbor weights
        rapidly for large grids (N > 1024).

        Args:
            grid (np.ndarray): The current 2D grid of states.

        Returns:
            np.ndarray: The next 2D grid of states.
        """

        if self.finite:
            conv_grid = ndimage.convolve(self.grid, self.neighborhood, mode="constant")
        else:
            conv_grid = ndimage.convolve(self.grid, self.neighborhood, mode="wrap")

        # use the gol logic to cacluate next alive cells
        next_board = (
            (self.grid == self.aliveValue)
            & (conv_grid > self.aliveValue)
            & (conv_grid < self.aliveValue * 4)
        ) | ((self.grid == 0) & (conv_grid == 3 * self.aliveValue)).astype(np.uint8)

        self.grid = next_board.astype(self.grid.dtype) * self.aliveValue

    def evolve(self):
        """
        Given the current states of the cells, apply the GoL rules:
        - Any live cell with fewer than two live neighbors dies, as if by underpopulation.
        - Any live cell with two or three live neighbors lives on to the next generation.
        - Any live cell with more than three live neighbors dies, as if by overpopulation.
        - Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
        """
        if self.fastMode:
            self.update_grid_fast()
            return

        new_grid = self.grid.copy()

        for i in range(self.rows):
            for j in range(self.cols):

                alive_neighbors = 0

                for r in range(-1, 2):
                    for c in range(-1, 2):

                        if r == 0 and c == 0:
                            continue  # skip the cell itself

                        ni = i + r
                        nj = j + c

                        if self.finite:
                            # skip neighbors outside the grid
                            if ni < 0 or ni >= self.rows or nj < 0 or nj >= self.cols:
                                continue
                        else:
                            # wrap around (toroidal grid)
                            ni %= self.rows
                            nj %= self.cols

                        if self.grid[ni, nj] == self.aliveValue:
                            alive_neighbors += 1

                # Apply GoL rules
                if self.grid[i, j] == self.aliveValue:
                    if alive_neighbors < 2 or alive_neighbors > 3:
                        new_grid[i, j] = self.deadValue
                    else:
                        new_grid[i, j] = self.aliveValue
                else:
                    if alive_neighbors == 3:
                        new_grid[i, j] = self.aliveValue
                    else:
                        new_grid[i, j] = self.deadValue

        self.grid = new_grid

    def insertBlinker(self, index=(0, 0)):
        """
        Insert a blinker oscillator construct at the index position
        """
        self.grid[index[0], index[1] + 1] = self.aliveValue
        self.grid[index[0] + 1, index[1] + 1] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 1] = self.aliveValue

    def insertGlider(self, index=(0, 0)):
        """
        Insert a glider construct at the index position
        """
        self.grid[index[0], index[1] + 1] = self.aliveValue
        self.grid[index[0] + 1, index[1] + 2] = self.aliveValue
        self.grid[index[0] + 2, index[1]] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 1] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 2] = self.aliveValue

    def insertGliderGun(self, index=(0, 0)):
        r, c = index
        val = self.aliveValue

        # 1. Left Square (Block)
        self.grid[r + 5, c + 1] = val
        self.grid[r + 5, c + 2] = val
        self.grid[r + 6, c + 1] = val
        self.grid[r + 6, c + 2] = val

        # 2. Left "Circle" / Shuttle Part
        self.grid[r + 5, c + 11] = val
        self.grid[r + 6, c + 11] = val
        self.grid[r + 7, c + 11] = val
        self.grid[r + 4, c + 12] = val
        self.grid[r + 8, c + 12] = val
        self.grid[r + 3, c + 13] = val
        self.grid[r + 3, c + 14] = val
        self.grid[r + 9, c + 13] = val
        self.grid[r + 9, c + 14] = val
        self.grid[r + 6, c + 15] = val
        self.grid[r + 4, c + 16] = val
        self.grid[r + 8, c + 16] = val
        self.grid[r + 5, c + 17] = val
        self.grid[r + 6, c + 17] = val
        self.grid[r + 7, c + 17] = val
        self.grid[r + 6, c + 18] = val

        # 3. Right "Circle" / Shuttle Part
        self.grid[r + 3, c + 21] = val
        self.grid[r + 4, c + 21] = val
        self.grid[r + 5, c + 21] = val
        self.grid[r + 3, c + 22] = val
        self.grid[r + 4, c + 22] = val
        self.grid[r + 5, c + 22] = val
        self.grid[r + 2, c + 23] = val
        self.grid[r + 6, c + 23] = val
        self.grid[r + 1, c + 25] = val
        self.grid[r + 2, c + 25] = val
        self.grid[r + 6, c + 25] = val
        self.grid[r + 7, c + 25] = val

        # 4. Right Square (Block)
        self.grid[r + 3, c + 35] = val
        self.grid[r + 4, c + 35] = val
        self.grid[r + 3, c + 36] = val
        self.grid[r + 4, c + 36] = val

    def insertEater(self, index=(0, 0)):
        """Standard eater 1 (destroys gliders)"""
        self.insertFromFile("pat-eater.cells", index=index)

    def insertReflector(self, index=(0, 0), rotate=0):
        """
        Simple 90° reflector (boat-based)
        Works for demonstration wiring.
        """
        self.insertFromFile("pat-reflector.cells", index=index, rotate=rotate)

    def insertBlock(self, index=(0, 0)):
        g = self.grid
        v = self.aliveValue

        r, c = index

        g[r, c] = v
        g[r, c + 1] = v
        g[r + 1, c] = v
        g[r + 1, c + 1] = v

        self.grid = g

    def insertGliderP60(self, index=(0, 0), rotate=0):
        self.insertFromFile("pat-glider gunp60.cells", index=index, rotate=rotate)

    def insertFromFile(self, filename, index=((0, 0)), rotate=0):
        """
        Insert cells from pattern file using parse_pattern
        """

        width, height, live_cells = parse_pattern(
            filename, self.aliveValue, self.deadValue
        )

        # build matrix
        matrix = [[0 for _ in range(width)] for _ in range(height)]

        for r, c in live_cells:
            matrix[r][c] = 1

        # rotate matrix
        def rotate_matrix(mat):
            n = len(mat)
            m = len(mat[0])
            rotated = [[0] * n for _ in range(m)]

            for j in range(n):
                for i in range(m):
                    rotated[i][j] = mat[j][m - 1 - i]

            return rotated

        rotations = (rotate // 90) % 4
        for _ in range(rotations):
            matrix = rotate_matrix(matrix)

        # insert rotated pattern
        for r in range(len(matrix)):
            for c in range(len(matrix[0])):
                if matrix[r][c] == 1:
                    target_r = index[0] + r
                    target_c = index[1] + c

                    if 0 <= target_r < self.rows and 0 <= target_c < self.cols:
                        self.grid[target_r, target_c] = self.aliveValue
