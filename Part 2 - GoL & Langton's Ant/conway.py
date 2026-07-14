# -*- coding: utf-8 -*-
"""
The Game of Life (GoL) module named in honour of John Conway

This module defines the classes required for the GoL simulation.
"""

import numpy as np
from scipy import ndimage
import re


def rle_parse(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()

        pattern_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("!"):
                pattern_lines.append(line)

        if not pattern_lines:
            raise ValueError("Empty or invalid RLE file.")

        header = pattern_lines[0]
        width_match = re.search(r"x\s*=\s*(\d+)", header)
        height_match = re.search(r"y\s*=\s*(\d+)", header)

        if not width_match or not height_match:
            raise ValueError("Invalid RLE header: missing x or y dimensions.")

        width = int(width_match.group(1))
        height = int(height_match.group(1))

        data = "".join(pattern_lines[1:]).replace(" ", "").strip()
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
                elif char == "$":
                    r += count
                    c = 0
                elif char == "!":
                    break

        return (width, height, live_cells)


def parse_pattern(filepath: str, aliveValue, deadValue):
    """
    Parses RLE (.rle) or Plaintext (.cells) files.
    """
    if filepath.endswith(".rle"):
        return rle_parse(filepath)

    with open(filepath, "r") as f:
        lines = f.readlines()

        pattern_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith("!"):
                pattern_lines.append(line)

        if not pattern_lines:
            return (0, 0, [])

        max_width = max(len(line) for line in pattern_lines)
        height = len(pattern_lines)
        live_cells = []

        for r, line in enumerate(pattern_lines):
            for c, char in enumerate(line):
                if char == "O":
                    live_cells.append((r, c))

        return (max_width, height, live_cells)


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
        self.rows = N
        self.cols = N

    def getStates(self):
        return self.grid

    def getGrid(self):
        return self.getStates()

    def update_grid_fast(self):
        if self.finite:
            conv_grid = ndimage.convolve(
                self.grid, self.neighborhood, mode="constant", cval=0
            )
        else:
            conv_grid = ndimage.convolve(self.grid, self.neighborhood, mode="wrap")

        next_board = (
            (self.grid == self.aliveValue) & (conv_grid >= 2) & (conv_grid <= 3)
        ) | ((self.grid == self.deadValue) & (conv_grid == 3))

        self.grid = next_board.astype(self.grid.dtype) * self.aliveValue

    def evolve(self):
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
                            continue

                        ni = i + r
                        nj = j + c

                        if self.finite:
                            if ni < 0 or ni >= self.rows or nj < 0 or nj >= self.cols:
                                continue
                        else:
                            ni %= self.rows
                            nj %= self.cols

                        if self.grid[ni, nj] == self.aliveValue:
                            alive_neighbors += 1

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
        self.grid[index[0], index[1] + 1] = self.aliveValue
        self.grid[index[0] + 1, index[1] + 1] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 1] = self.aliveValue

    def insertGlider(self, index=(0, 0)):
        self.grid[index[0], index[1] + 1] = self.aliveValue
        self.grid[index[0] + 1, index[1] + 2] = self.aliveValue
        self.grid[index[0] + 2, index[1]] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 1] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 2] = self.aliveValue


    def insertGliderGun(self, index=(0, 0)):
        self.grid[index[0] + 1, index[1] + 26] = self.aliveValue

        self.grid[index[0] + 2, index[1] + 24] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 26] = self.aliveValue

        self.grid[index[0] + 3, index[1] + 14] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 15] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 22] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 23] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 36] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 37] = self.aliveValue

        self.grid[index[0] + 4, index[1] + 13] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 17] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 22] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 23] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 36] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 37] = self.aliveValue

        self.grid[index[0] + 5, index[1] + 1 + 1] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 2 + 1] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 12] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 18] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 22] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 23] = self.aliveValue

        self.grid[index[0] + 6, index[1] + 1 + 1] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 2 + 1] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 12] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 16] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 18] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 19] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 24] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 26] = self.aliveValue

        self.grid[index[0] + 7, index[1] + 12] = self.aliveValue
        self.grid[index[0] + 7, index[1] + 18] = self.aliveValue
        self.grid[index[0] + 7, index[1] + 26] = self.aliveValue

        self.grid[index[0] + 8, index[1] + 13] = self.aliveValue
        self.grid[index[0] + 8, index[1] + 17] = self.aliveValue

        self.grid[index[0] + 9, index[1] + 14] = self.aliveValue
        self.grid[index[0] + 9, index[1] + 15] = self.aliveValue

    def insertEater(self, index=(0, 0)):
        self.insertFromFile("pat-eater.cells", index=index)

    def insertReflector(self, index=(0, 0), rotate=0):
        self.insertFromFile("pat-reflector.cells", index=index, rotate=rotate)

    def insertBlock(self, index=(0, 0)):
        r, c = index
        self.grid[r, c] = self.aliveValue
        self.grid[r, c + 1] = self.aliveValue
        self.grid[r + 1, c] = self.aliveValue
        self.grid[r + 1, c + 1] = self.aliveValue

    def insertGliderP60(self, index=(0, 0), rotate=0):
        self.insertFromFile("pat-glider gunp60.cells", index=index, rotate=rotate)

    def insertFromFile(self, filename, index=(0, 0), rotate=0):
        """
        Loads, rotates (by 0, 90, 180, 270 deg clockwise), and inserts a pattern.
        """
        width, height, live_cells = parse_pattern(
            filename, self.aliveValue, self.deadValue
        )

        if not live_cells:
            return

        matrix = [[0 for _ in range(width)] for _ in range(height)]
        for r, c in live_cells:
            matrix[r][c] = 1

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

        for r in range(len(matrix)):
            for c in range(len(matrix[0])):
                if matrix[r][c] == 1:
                    target_r = index[0] + r
                    target_c = index[1] + c
                    if 0 <= target_r < self.rows and 0 <= target_c < self.cols:
                        self.grid[target_r, target_c] = self.aliveValue
