"""
The Game of Life (GoL) module named in honour of John Conway

This module defines the classes required for the GoL simulation.

"""

import numpy as np
from scipy import signal, ndimage


def parse_pattern(filepath, aliveValue, deadValue):
    """
    TODO: [Part 1d - RLE/Plaintext Parser]
    Write a parser for Run Length Encoded (RLE) or Plaintext (.cells) patterns
    so grids larger than 20x20 can be loaded.

    Args:
        filepath (str): Path to the pattern file.

    Returns:
        tuple: (width, height, list of (r, c) offsets of live cells)
    """
    # Student TODO: Implement parser here
    # plain text parser

    with open(filepath, "r") as f:
        lines = f.readlines()

        pattern_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith("!"):
                pattern_lines.append(line)

        max_withd = max(len(line) for line in pattern_lines)

        pattern = []
        i = 0
        for line in pattern_lines:
            row = []
            for char in line:
                if char == "O":
                    row.append(aliveValue)
                else:
                    row.append(deadValue)

            row.extend([deadValue] * (max_withd - len(row)))
            pattern.append(row)
        live_cells = []
        for i in range(len(pattern)):
            for j in range(max_withd):
                if pattern[i][j] == aliveValue:
                    live_cells.append((i, j))

        return (max_withd, len(pattern_lines), live_cells)

    pass


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

    def update_grid_fast(self, grid):
        """
        TODO: [Part 1e - Fast Convolution]
        Use scipy.signal.convolve2d (or similar) to compute neighbor weights
        rapidly for large grids (N > 1024).

        Args:
            grid (np.ndarray): The current 2D grid of states.

        Returns:
            np.ndarray: The next 2D grid of states.
        """
        # Student TODO: Implement fast 2D convolution method
        pass

    def evolve(self):
        """
        Given the current states of the cells, apply the GoL rules:
        - Any live cell with fewer than two live neighbors dies, as if by underpopulation.
        - Any live cell with two or three live neighbors lives on to the next generation.
        - Any live cell with more than three live neighbors dies, as if by overpopulation.
        - Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
        """
        if self.fastMode:
            self.grid = self.update_grid_fast(self.grid)
            return

            # TODO: [Part 1a - Core Rules]
            # Remove the transition logic and implement the 4 standard GoL rules
            # (Underpopulation, Survival, Overpopulation, Reproduction) by iterating
            # through the cells cell-by-cell. Handle self.finite wrapping appropriately.

            # Student TODO: Implement slow update cell-by-cell logic here
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

    def insertFromFile(self, filename, index=((0, 0))):
        """
        Insert cells from pattern file using parse_pattern
        """
        width, height, live_cells = parse_pattern(
            filename, self.aliveValue, self.deadValue
        )
        for r, c in live_cells:
            target_r = index[0] + r
            target_c = index[1] + c
            if 0 <= target_r < self.rows and 0 <= target_c < self.cols:
                self.grid[target_r, target_c] = self.aliveValue
